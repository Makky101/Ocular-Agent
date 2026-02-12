# Human Emulator

An AI-assisted desktop automation prototype that captures your screen, asks Gemini to reason about the current UI, then generates a structured action plan for task execution.

## What this project does

`Human Emulator` is designed to:

- Take a full-screen screenshot of your current desktop state
- Send the screenshot + user task to a Gemini model
- Receive a JSON step-by-step action plan (move, click, type, press, wait, drag)
- Run through the plan using a local automation loop

> **Current status:** the low-level `pyautogui` calls in `main.py` are mostly commented out and replaced with print statements for safe debugging.

---

## Project structure

- `main.py`  
  Entry point. Collects task input, calls reasoning, and runs automation actions.

- `reasoning.py`  
  Builds the LLM prompt, sends screenshot + instructions to Gemini, and parses model output into JSON.

- `screenCapture.py`  
  Captures monitor screenshot using `mss` and returns PNG bytes.

- `memory.py`  
  Placeholder for future caching/memory logic.

- `test.py`  
  Quick local test harness that launches `main.py` and feeds a random command.

- `requirements.txt`  
  Python dependencies.

---

## Requirements

- Python 3.10+
- Windows desktop environment (current implementation tested with Windows-style usage)
- Gemini API key

---

## Setup

1. Clone the repository

```bash
git clone https://github.com/Makky101/Human-Emulator.git
cd Human-Emulator
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add environment variables

Create a `.env` file in the project root:

```env
API_KEY=your_google_gemini_api_key_here
```

---

## Usage

Run the app:

```bash
python main.py
```

Then type a task when prompted, for example:

- `open chrome and search for weather`
- `open vscode`
- `open calculator`

The app will:

1. Capture the screen
2. Generate a JSON automation plan with Gemini
3. Execute (currently print/debug) each action step

---

## How it works (flow)

1. **Input**: User provides a natural language task in `main.py`
2. **Perception**: `screenCapture.py` captures the current screen
3. **Reasoning**: `reasoning.py` sends screenshot + strict prompt to Gemini
4. **Parsing**: AI response is cleaned and parsed into JSON actions
5. **Execution**: `automate()` loops through steps/actions and performs (or logs) commands

---

## JSON action schema (expected)

Each step follows this shape:

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

Supported keywords in executor logic:

- `moveto`
- `click`
- `doubleclick`
- `rightclick`
- `type`
- `press`
- `wait`
- `dragto`

---

## Notes / limitations

- `main.py` currently logs many actions instead of executing them (safe development mode).
- `clean_data()` in `reasoning.py` may need hardening for malformed model outputs.
- `memory.py` is not implemented yet.
- Automation safety features are configured (`pyautogui.FAILSAFE = True`) but should be tested carefully before enabling full control.

---

## Quick test

Run:

```bash
python test.py
```

This starts `main.py` and sends a random command from a predefined list.

---

## Roadmap ideas

- Re-enable and validate real `pyautogui` calls in `main.py`
- Add robust output validation for AI-generated plans
- Add retries/fallbacks for uncertain UI detections
- Implement persistent memory/caching in `memory.py`
- Add structured logging and unit tests

---

## License

No license file is currently included. Add a `LICENSE` file if you plan to distribute this project publicly.
