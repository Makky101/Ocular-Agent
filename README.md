# Human Emulator

Human Emulator is a Python desktop-automation prototype that turns a natural-language task into **real mouse and keyboard actions** on your computer.

It works in 4 stages:
1. Capture the current desktop screenshot.
2. Send screenshot + task to an LLM (Kimi K2.5 via Hugging Face).
3. Receive a JSON action plan.
4. Execute the plan with `pyautogui`, then verify and retry if needed.

---

## Safety Notice

This project controls your **actual desktop session**. It can move your mouse, click, type, and press keys.

- Run it only when you can watch what it is doing.
- Close sensitive apps/documents first.
- PyAutoGUI fail-safe is enabled by default — move your cursor to any screen corner to abort immediately.

---

## Features

- Natural-language task input from terminal.
- Multimodal planning (text + live screenshot sent to LLM).
- Action-plan execution with `moveto`, `click`, `doubleclick`, `rightclick`, `type`, `press`, `hotkey`, `wait`, and `dragto`.
- Post-execution verification — the LLM checks a fresh screenshot and decides if the task succeeded.
- Automatic retry loop (up to 3 attempts) with failure feedback passed back to the planner.
- File-based caching for latest task and model output.

---

## Requirements

- Python 3.10+
- Internet access for LLM API calls
- Hugging Face API token in `.env` as `API_KEY`

---

## Setup

```bash
git clone https://github.com/Makky101/Human-Emulator.git
cd Human-Emulator
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
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

You will be prompted to describe your task in plain English:

```
What task do you want me to perform: open chrome and search for weather
```

Example prompts:
- `open chrome`
- `open vscode`
- `open calculator`
- `open chrome and search for weather`

> **Safety note:** This tool controls your real mouse and keyboard. Save your work and close sensitive windows before running.

---

## How It Works

```
User input
    │
    ▼
Screenshot captured
    │
    ▼
LLM generates JSON action plan
    │
    ▼
Actions executed (mouse + keyboard)
    │
    ▼
LLM verifies result via fresh screenshot
    │
    ├── success → exit
    └── failed  → retry with feedback (up to 3 times)
```

---

## Code Overview

| File | Responsibility |
|---|---|
| `main.py` | Entry point — collects input, wires everything together |
| `reasoning.py` | Prompt building, LLM calls, response parsing, verification |
| `screenCapture.py` | Captures primary monitor and returns PNG bytes |
| `memory.py` | File-based cache for latest task and model output |
| `automate.py` | Executes action plan and manages retry loop |

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

| Keyword | Purpose | Required Fields |
|---|---|---|
| `moveto` | Move mouse cursor | `co-ord` {x, y} |
| `click` | Left click | `co-ord` (optional) |
| `doubleclick` | Double click | `co-ord` (optional) |
| `rightclick` | Right click | `co-ord` (optional) |
| `dragto` | Click and drag | `co-ord` {x, y} |
| `type` | Type text | `text` |
| `press` | Press a key | `key` (e.g. `enter`, `win`) |
| `hotkey` | Key combination | `keys` (e.g. `["ctrl", "l"]`) |
| `wait` | Pause execution | `duration` (seconds) |

---

## Verification Schema

After execution, the verifier returns:

```json
{
  "status": "exit",
  "reason": ""
}
```

- `exit` — task completed successfully, stop.
- `edit` — task failed; `reason` is passed back to the planner for a better attempt.

---

## Known Limitations

- Uses your active desktop directly — not sandboxed.
- Coordinate accuracy depends on the LLM correctly reading the screenshot.
- JSON parsing is lightweight and may struggle with heavily malformed model output.
- Cache is local and temporary — no long-term task memory across sessions.
- Retry loop is capped at 3 attempts.
