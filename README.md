# Human Emulator

Human Emulator is a Python desktop automation prototype that turns a plain-English task into real mouse and keyboard actions on your computer.

It currently supports two ways to provide a task:

- typed input from the terminal
- voice input through your microphone, transcribed with Hugging Face speech recognition

## AI-Assisted Development

This project was built with AI-assisted coding support.

- I used AI help while implementing and debugging parts of the project.
- AI assistance was especially used around the voice-input and transcription flow.
- AI assistance was also used to help revise parts of this README.

The project idea, testing, and final decisions still came from me, but some coding and documentation work was AI-assisted.

## How It Works

The current loop looks like this:

1. Ask the user for a task by text or voice.
2. If voice mode is chosen, record audio, play it back, and transcribe it into text.
3. Capture the current desktop screenshot.
4. Send the screenshot and task to an LLM.
5. Receive a JSON action plan.
6. Execute the plan with `pyautogui`.
7. Re-check the result and retry with feedback if needed.

## Features

- Typed terminal input for quick testing
- Voice task input with microphone recording
- Playback of the captured voice recording before transcription
- Speech-to-text transcription using `openai/whisper-large-v3`
- Screenshot capture with `mss`
- LLM-based action-plan generation from screenshots and task text
- JSON action plans with mouse and keyboard steps
- Retry flow with verification prompts
- Local caching of the latest task and model output
- Basic unit tests for parsing and retry behavior

## Safety

This project controls your real desktop session.

- Run it only when you can watch it.
- Close sensitive windows before starting.
- Do not touch the keyboard or mouse during live automation.
- PyAutoGUI fail-safe is enabled, so moving the pointer to a screen corner should stop execution.

## Tech Stack

- Python 3.10+
- `pyautogui`
- `huggingface_hub`
- `mss`
- `numpy`
- `Pillow`
- `python-dotenv`
- `sounddevice`

## Project Structure

- `main.py` - entry point, task collection, and run orchestration
- `voice_input.py` - microphone recording, playback, temp WAV export, and speech-to-text
- `reasoning.py` - prompt building, model calls, parsing, and verification prompts
- `automate.py` - action execution and retry handling
- `screenCapture.py` - screenshot capture
- `memory.py` - lightweight task/output caching
- `tests/test_core.py` - unit tests for core logic

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

When the app starts, you will be prompted with:

```text
Press Enter to type your task or type 'voice' to speak it:
```

### Typed Input

Press `Enter` and then type a task such as:

- `open chrome`
- `open vscode`
- `open calculator`
- `open chrome and search for weather`

### Voice Input

Type `voice`, then choose how long the app should listen:

```text
How many seconds should I listen? (default 6):
```

The current voice flow is:

1. Record from the default microphone.
2. Play the recording back through the default speaker.
3. Save the recording to a temporary `.wav` file.
4. Send the audio to Hugging Face ASR using the `hf-inference` provider.
5. Return the transcript as the task text.

Voice mode currently uses:

- sample rate: `16000`
- channels: `1` (mono)
- sample format: `int16`
- model: `openai/whisper-large-v3`

## Environment Notes

- `API_KEY` must be available before voice input or model calls will work.
- Voice mode needs a working microphone.
- Playback needs a working default speaker or headphone output.
- The speech-to-text request depends on network access and Hugging Face provider availability.

## Action Plan Format

The executor expects a JSON array like this:

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
- Accuracy depends heavily on screenshot interpretation.
- A bad plan can still click the wrong place.
- The app depends on external AI services for planning, verification, and voice transcription.
- Voice transcription depends on external inference availability.
- End-to-end live automation is much less predictable than the unit tests.
- This is still a prototype, not a hardened desktop agent.
