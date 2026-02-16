# Human Emulator

Human Emulator is a Python desktop-automation prototype that turns a natural-language task into **real mouse and keyboard actions**.

It works in 4 stages:
1. Capture the current desktop screenshot.
2. Send screenshot + task to an LLM.
3. Receive a JSON action plan.
4. Execute the plan with `pyautogui`.

---

## Safety Notice

This project controls your **actual desktop session**. It can move your mouse, click, type, and press keys.

- Run it only when you can watch what it is doing.
- Close sensitive apps/documents first.
- Keep PyAutoGUI fail-safe enabled (already enabled in `main.py`): move the cursor to a screen corner to trigger a fail-safe exception.

---

## Features

- Natural-language task input from terminal.
- Multimodal planning (text + screenshot).
- Action-plan execution with `moveto`, `click`, `doubleclick`, `rightclick`, `type`, `press`, `wait`, and `dragto`.
- Basic file-based caching for latest task/output.
- Simple random-command smoke test (`test.py`).

---

## Requirements

- Python 3.10+
- Windows desktop session with active GUI
- Internet access for LLM API calls
- Hugging Face API token in `.env` as `API_KEY`

---

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

---

## Run

```bash
python main.py
```

Example prompts:
- `open chrome`
- `open vscode`
- `open calculator`

---

## How It Works (Code Overview)

- `main.py`  
  Entry point and action executor (`automate`).

- `reasoning.py`  
  Prompt builder, LLM call, response cleaning/parsing, and verification helpers.

- `screenCapture.py`  
  Captures primary monitor screenshot for multimodal input.

- `memory.py`  
  Simple cache for latest model output and instruction text.

- `test.py`  
  Randomized smoke test that pipes a generated command into `main.py`.

---

## Action Plan Schema

The executor expects a JSON array of steps:

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

Supported `keyword` values:
- `moveto`
- `click`
- `doubleclick`
- `rightclick`
- `type`
- `press`
- `wait`
- `dragto`

---

## Quick Test

```bash
python test.py
```

This runs one randomized command through `main.py` as a basic smoke check.

---

## Current Limitations

- Runs directly on your active desktop (real cursor/keyboard control).
- Response cleaning is still lightweight; malformed model output can fail parsing.
- Memory is temporary file-based caching, not long-term stateful memory.

---

## Recent Maintenance Update

- Improved code comments and docstrings in core modules:
  - `main.py`
  - `reasoning.py`
  - `screenCapture.py`
  - `memory.py`
