# Human Emulator

Human Emulator is a Python desktop-automation prototype that converts a natural-language request into real mouse/keyboard actions.

It follows this flow:
1. Capture the current screen.
2. Send screenshot + user task to an LLM.
3. Receive a JSON action plan.
4. Execute that plan with `pyautogui`.

---

## Features

- Natural-language task input from terminal.
- Multimodal planning (text + screenshot).
- Action-plan execution with `moveto`, `click`, `type`, `press`, `wait`, etc.
- Basic file-based memory for latest task/output.
- Simple random-command smoke test script.

---

## Project Structure

- `main.py`  
  Entry point and action executor (`automate`).

- `reasoning.py`  
  Prompt generation, model call, response cleanup/parsing, and verification loop helpers.

- `screenCapture.py`  
  Primary-monitor screenshot capture utility.

- `memory.py`  
  Minimal cache layer for latest model output and instruction.

- `test.py`  
  Runs a random task against `main.py` for a quick smoke check.

- `requirements.txt`  
  Python dependencies.

---

## Requirements

- Python 3.10+
- Windows desktop session (active GUI)
- Hugging Face API key in `.env` as `API_KEY`

---

## Setup

```bash
git clone https://github.com/Makky101/Human-Emulator.git
cd Human-Emulator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in project root:

```env
API_KEY=your_huggingface_token_here
```

---

## Run

```bash
python main.py
```

Example tasks:
- `open chrome`
- `open vscode`
- `open calculator`

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

This runs one randomized command through `main.py`.

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

---

## License

No license file is currently included. Add a `LICENSE` before public distribution.
