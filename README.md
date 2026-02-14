# Human Emulator

`Human Emulator` is a desktop automation prototype that turns a natural-language task into executable UI actions.

It works by:

1. Capturing your current screen
2. Sending screenshot + task to an LLM
3. Receiving a JSON action plan
4. Executing that plan with `pyautogui`

---

## Current status

- Core loop is functional (`main.py` -> `reasoning.py` -> `automate()`)
- Real mouse/keyboard actions are enabled in `main.py`
- Action plans are generated via Hugging Face Inference API (`InferenceClient`)
- `memory.py` currently stores/retrieves raw AI output in `task.json`

---

## Project structure

- `main.py`  
  Entry point. Reads user task, gets reasoning output, executes UI actions.

- `reasoning.py`  
  Builds prompt, sends screenshot + task to model, cleans/parses JSON response.

- `screenCapture.py`  
  Captures monitor screenshot using `mss`.

- `memory.py`  
  Simple file-based cache helper for task output (`task.json`).

- `test.py`  
  Launches `main.py` with a randomized command for quick smoke testing.

- `requirements.txt`  
  Python dependencies.

---

## Requirements

- Python 3.10+
- Windows desktop environment
- Hugging Face API token (used as `API_KEY`)

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

4. Add environment variable

Create a `.env` file in the project root:

```env
API_KEY=your_huggingface_token_here
```

---

## Usage

Run:

```bash
python main.py
```

Then provide a task, for example:

- `open chrome`
- `open vscode`
- `open calculator`

---

## Action schema expected from model

The executor expects a JSON array like:

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

## Notes / limitations

- Automation runs on your active desktop session; unexpected cursor/keyboard movement can interrupt tasks.
- `clean_data()` in `reasoning.py` is basic and may fail on malformed model responses.
- `reasoning.py` still imports `google.genai`, but current execution path uses `huggingface_hub.InferenceClient`.
- `memory.py` is minimal and not yet a true long-term memory system.

---

## Quick test

```bash
python test.py
```

This runs `main.py` with one random command from a predefined list.

---

## Roadmap

- Add strict response schema validation before automation
- Add retry and fallback behavior when plan generation is invalid
- Improve coordinate robustness (multi-monitor, scaling, app states)
- Add unit/integration tests for parser + executor
- Expand memory layer beyond basic file caching

---

## License

No license file is currently included.
Add a `LICENSE` file before public distribution.
