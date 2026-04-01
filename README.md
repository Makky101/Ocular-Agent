# Human Emulator

Human Emulator is a Python desktop automation prototype that turns a natural-language instruction into real mouse and keyboard actions on your computer.

The project is built around a simple loop:
1. Capture the current desktop screenshot.
2. Send the screenshot and task to an LLM.
3. Receive a JSON action plan.
4. Execute the plan with `pyautogui`.
5. Verify each step and retry with feedback if needed.

## Safety

This project controls your real desktop session.

- Run it only when you can watch what it is doing.
- Close sensitive apps and documents first.
- Do not touch your keyboard or mouse while a live run is in progress.
- PyAutoGUI fail-safe is enabled, so moving the cursor to a screen corner should abort execution.

## Features

- Natural-language task input from the terminal
- Live screenshot capture with `mss`
- Multimodal planning using a Hugging Face hosted model
- JSON action plans with mouse and keyboard steps
- Step verification with retry support
- Local task/output caching
- Basic unit tests for parsing, validation, and retry flow

## Tech Stack

- Python 3.10+
- `pyautogui`
- `huggingface_hub`
- `mss`
- `numpy`
- `Pillow`
- `python-dotenv`

## Project Structure

- `main.py` - entry point that collects the task and starts the run
- `reasoning.py` - prompt building, model calls, parsing, and verification prompts
- `automate.py` - executes action plans and handles retry logic
- `screenCapture.py` - captures the primary monitor as PNG bytes
- `memory.py` - stores the latest task and model output locally
- `tests/test_core.py` - unit tests for core non-desktop logic

## Setup

```bash
git clone https://github.com/Makky101/Human-Emulator.git
cd Human-Emulator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
API_KEY=your_huggingface_token_here
```

## Run

```bash
python main.py
```

Example prompts:

- `open chrome`
- `open vscode`
- `open calculator`
- `open chrome and search for weather`

## Action Plan Format

The executor expects a JSON array of steps like this:

```json
[
  {
    "id": 1,
    "step": "Click search bar",
    "action": [
      { "keyword": "moveto", "co-ord": { "x": 500, "y": 150 } },
      { "keyword": "click" }
    ]
  }
]
```

Supported action keywords:

- `moveto`
- `click`
- `doubleclick`
- `rightclick`
- `dragto`
- `type`
- `press`
- `hotkey`
- `wait`

## Verification Format

Step verification currently expects JSON shaped like:

```json
{
  "status": "ok",
  "reason": ""
}
```

If verification returns `"fail"`, the system asks the planner for a new plan and retries.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

Current tests cover:

- plan validation
- JSON cleanup and parsing
- retry flow without triggering real desktop actions

## Known Limitations

- It uses your active desktop directly and is not sandboxed.
- Accuracy depends heavily on the model understanding the screenshot.
- A bad plan can still click the wrong thing.
- The project is still a prototype, not a hardened desktop agent.
- End-to-end live automation is much less predictable than the unit tests.
