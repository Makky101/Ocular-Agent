from screenCapture import screenCapture
from google import genai
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from memory import caching
import os
import json
import re

load_dotenv()

#prompt
def prompt(task,OS):

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

    return msg

# clean data
def clean_data(ai_output):
  match = re.search(r'```(?:json)?\s*([\s\S*?])\s*```',ai_output)
  if match:
    json_text = match.group(1)
  else:
    match = re.search(r'\[[\s\S]*\]',ai_output)
    json_text = match.group(0) if match else ai_output

  json_text = json_text.strip()
  json_text = re.sub(r',\s*([}\]])', r'\1', json_text)

  try:
    print(json_text)
    return json.loads(json_text)
  except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON from AI: {e}") 

# llm generates a checklist and follows it
def reason(task,OS):
    try:
      client = InferenceClient(token=os.environ.get("API_KEY"))
      response = client.chat_completion(
        model= 'moonshotai/Kimi-K2.5:novita',
        messages=[{
          'role':'user',
          'content':[
            {'type':'text', 'text': prompt(task,OS)},

            {'type': 'image', 
             'image': {'url': f'data:image/png;base64,{screenCapture()}'}
            }
          ]
        }],
        max_tokens=2000
      )
      data = response.choices[0].message.content
      print(data)
      caching(data,'write')
      return clean_data(data)
    except Exception as e:
      print('error at reason --> ',e)
    

