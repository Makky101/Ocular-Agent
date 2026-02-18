from screenCapture import screenCapture
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from memory import task_cache_write, task_cache_read
import os
import json
import re

# Load .env values once at import so API_KEY is available.
load_dotenv()

"""Reasoning layer.

This module:
1) captures the current screen,
2) prompts an LLM to produce an action-plan JSON,
3) sanitizes/parses the response,
4) stores and reuses latest task/output for basic verification.
"""


# Prompt builder
def prompt(task,OS=None,LLM_response=None,default=None):
    """Create prompt text for either task execution or result verification.

    Args:
      task: Natural-language task requested by the user.
      OS: Optional operating system hint.
      LLM_response: Prior model output to verify when in checking mode.
      default: When True, builds the main action-planning prompt.
    """
    if default:
      msg = f"""You are a **Technical Operator AI** that automates computer tasks by analyzing screenshots and generating precise action sequences.

      **CURRENT TASK:** {task}

      ---

      ## YOUR OBJECTIVE:
      Analyze the provided screenshot and generate a **complete step-by-step action plan** to accomplish the task. This plan will be executed all at once, so it must be thorough and account for typical system response times.

      ---

      ## SCREENSHOT ANALYSIS CHECKLIST:
      Before creating your plan, identify:
      - ✓ All visible UI elements (buttons, fields, icons, menus, links)
      - ✓ Exact pixel coordinates for interactive elements
      - ✓ Current state of the interface (what's already open, selected, focused)
      - ✓ Any elements that may need time to load after actions

      **CRITICAL:** Base your plan ENTIRELY on what you can see in the screenshot. Do not assume elements exist if they're not visible.

      ---

      ## AVAILABLE ACTIONS:

      | Action | Purpose | Required Fields |
      |--------|---------|----------------|
      | `moveto` | Move mouse cursor | `co-ord` {{x, y}} |
      | `click` | Left click (current position or specified coords) | `co-ord` {{x, y}} (optional if already at position) |
      | `rightclick` | Right click | `co-ord` {{x, y}} |
      | `doubleclick` | Double click | `co-ord` {{x, y}} |
      | `dragto` | Click and drag to destination | `co-ord` {{x, y}} |
      | `type` | Type text into focused field | `text` |
      | `press` | Press special key | `key` (enter, backspace, space, tab, esc, delete, etc.) |
      | `wait` | Pause execution | `duration` (seconds) |

      ---

      ## OUTPUT FORMAT:

      Return **ONLY** valid JSON (no markdown code blocks, no explanations, no preamble):
      ```json
      [
        {{
          "id": 1,
          "step": "Click the search bar",
          "action": [
            {{
              "keyword": "moveto",
              "co-ord": {{"x": 500, "y": 150}}
            }},
            {{
              "keyword": "click"
            }}
          ]
        }},
        {{
          "id": 2,
          "step": "Type search query and submit",
          "action": [
            {{
              "keyword": "type",
              "text": "example query"
            }},
            {{
              "keyword": "press",
              "key": "enter"
            }},
            {{
              "keyword": "wait",
              "duration": 2
            }}
          ]
        }},
        {{
          "id": 3,
          "step": "Drag file to destination folder",
          "action": [
            {{
              "keyword": "moveto",
              "co-ord": {{"x": 100, "y": 200}}
            }},
            {{
              "keyword": "dragto",
              "co-ord": {{"x": 300, "y": 400}}
            }}
          ]
        }}
      ]
      ```

      ---

      ## CRITICAL RULES:

      ### Structure:
      - Return ONLY the JSON array (no markdown, no text before/after)
      - Use double quotes for all strings
      - `id` must be sequential (1, 2, 3...)
      - Each `step` must have at least one `action`

      ### Co-ordinates:
      - Must be actual pixel positions from screenshot analysis
      - Use integers only (no decimals)
      - Format: `{{"x": 243, "y": 456}}`

      ### Action Sequencing:
      - **Always** `moveto` before `click`/`rightclick`/`doubleclick` (unless clicking at current position)
      - **Always** `moveto` to starting position before `dragto`
      - Add `wait` actions after operations that trigger loading/transitions
      - Group related actions in the same step (e.g., type + press enter)

      ### Best Practices:
      - Think like a careful human user (not too fast, not too slow)
      - Include 1-3 second waits after clicks that load new content
      - Be precise with coordinates (center of buttons, not edges)
      - For typing, ensure the field is clicked/focused first

      ---

      ## EXAMPLE REASONING PROCESS:

      **Task:** "Open Google Chrome and search for weather"

      **Analysis:**
      1. Locate Chrome icon → co-ords (100, 500)
      2. After Chrome opens, wait for it to load → 2 seconds
      3. Locate search/address bar → co-ords (600, 100)
      4. Type query → "weather"
      5. Submit search → press enter

      **Output:** (JSON array following format above)

      ---

      Now analyze the screenshot and generate your complete JSON action plan for: **{task}**
      """
    else:
      msg = f'''You are a task verification assistant. You will be given:
        1. An original task/instruction
        2. The output produced by an LLM attempting to complete that task
        3. A screenshot showing the actual result

        Your job is to evaluate whether the LLM successfully completed the task as specified.

        Evaluation criteria:
        - Did the LLM address all parts of the task?
        - Is the output in the correct format requested?
        - Does the output meet the quality standards implied by the task?
        - Did the LLM follow any specific constraints or requirements?
        - A screenshot will be provided, does the visual output match what was requested?

        If the task was NOT completed successfully, respond with only the word: edit

        ---

        ORIGINAL TASK:
        {task}

        LLM OUTPUT:
        {LLM_response}
        '''
    return msg


# Clean and parse model output into Python JSON.
def clean_data(ai_output):
  """Extract the first JSON array-like payload from model text output.

  The model is expected to return plain JSON, but this helper tolerates
  occasional code fences or trailing commas.
  """
  match = re.search(r'```(?:json)?\s*([\s\S*?])\s*```',ai_output)
  if match:
    json_text = match.group(1)
  else:
    match = re.search(r'\[[\s\S]*\]',ai_output)
    json_text = match.group() if match else ai_output

  json_text = json_text.strip()
  json_text = re.sub(r',\s*([}\]])', r'\1', json_text)
  
  try:
    return json.loads(json_text)
  
  except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON from AI: {e}") 


# LLM generates a checklist and follows it.
def reason(task,default=None,LLMR=None,OS=None):
  """Request an action plan (or verification) from the configured LLM."""
  try:
    # Initialize Hugging Face inference client using API key from env.
    client = InferenceClient(token=os.environ.get("API_KEY"))

    # Send multimodal request: prompt text + current screenshot.
    response = client.chat_completion(
      model= 'moonshotai/Kimi-K2.5:novita',
      messages=[{
        'role':'user',
        'content':[
          {'type':'text', 'text': prompt(task,default=default,OS=OS,LLM_response=LLMR)},

          {'type': 'image', 
            'image': {'url': f'data:image/png;base64,{screenCapture()}'}
          }
        ]
      }],
      max_tokens=2000
    )
    data = response.choices[0].message.content

    # Verification mode expects plain text status (e.g., 'edit').
    if not default:
      return str(data).strip()

    parsed = clean_data(data)

    # Persist cache only for task-generation flow.
    task_cache_write(task, data)
    return parsed
  except Exception as e:
    print('error at reason --> ',e)


# Error checking to ensure the task has been completed.
def error_checking():
  """Run the lightweight verifier prompt against cached task + output."""
  try:
    cached_data = task_cache_read()
    if not cached_data:
      return 'exit'

    task, data = cached_data
    result = reason(task, default=False, LLMR=data)

    # Normalise verifier result to a simple status string.
    status = str(result).strip().lower()
    return status if status else 'exit'
  except Exception as e:
    print('error at error_checking ->', e)
    return 'exit'
