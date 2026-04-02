from pathlib import Path  
import os 
import tempfile  
import wave  
import sounddevice as sd  
from huggingface_hub import InferenceClient  

DEFAULT_DURATION_SECONDS = 6  
DEFAULT_SAMPLE_RATE = 16000  
DEFAULT_ASR_MODEL = "openai/whisper-large-v3"  
DEFAULT_ASR_PROVIDER = "hf-inference"  


# This helper records audio from the user's default microphone.
def _record_microphone(duration, sample_rate):
    """Record mono audio from the default microphone."""

    if duration <= 0:
        raise ValueError("Recording duration must be greater than 0 seconds.")

    # Work out how many total samples we need for the requested duration.
    frame_count = int(duration * sample_rate)

    # Tell the user recording is about to happen.
    print(f"Listening for {duration} seconds...")

    # Record one-channel 16-bit audio from the microphone.
    recording = sd.rec(frame_count, samplerate=sample_rate, channels=1, dtype="int16")

    sd.wait()
    return recording


# This helper plays the recorded audio back so the user can hear what was captured.
def _play_recording(recording, sample_rate):
    """Play the captured recording back through the default speaker."""

    # Tell the user playback is starting.
    print("Playing back your recording...")
    # Send the recorded audio to the default output device.
    sd.play(recording, samplerate=sample_rate)
    # Wait until playback is finished before moving on.
    sd.wait()


# This helper saves the in-memory recording to a temporary WAV file.
def _save_recording(recording, sample_rate):
    """Persist the recording to a temporary WAV file for the ASR request."""

    # Create a temporary file name that ends with .wav and keep it after closing.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        # Wrap the file name in Path so we can use helpful path methods later.
        temp_path = Path(temp_file.name)

    # Open the temporary file in WAV write mode.
    with wave.open(str(temp_path), "wb") as wav_file:
        # Store the audio as mono, meaning one audio channel.
        wav_file.setnchannels(1)

        # Store each audio sample using 2 bytes, which matches int16.
        wav_file.setsampwidth(2)

        # Store the sample rate in the WAV header.
        wav_file.setframerate(sample_rate)

        # Write the raw bytes from the recorded array into the WAV file.
        wav_file.writeframes(recording.tobytes())

    # Return the path to the saved WAV file.
    return temp_path


# This is the main function that records, optionally plays back, transcribes, and cleans up.
def capture_voice_task(
    duration=DEFAULT_DURATION_SECONDS,  # Use the default recording length unless the caller overrides it.
    sample_rate=DEFAULT_SAMPLE_RATE,  # Use the default speech-friendly sample rate unless overridden.
    model=DEFAULT_ASR_MODEL,  # Use the default ASR model unless another one is passed in.
    provider=DEFAULT_ASR_PROVIDER,  # Use the chosen Hugging Face provider instead of auto-routing.
    playback=False,  
):
    """Convert microphone audio into text using Hugging Face automatic speech recognition."""

    # Read the API key from the environment so it is not hardcoded in the file.
    api_key = os.environ.get("API_KEY")

    # Refuse to continue if there is no API key available.
    if not api_key:
        # Raise a helpful message that tells the user exactly what is missing.
        raise RuntimeError("API_KEY is missing. Add it to your .env file before using voice input.")

    # Start with no file path so cleanup code can safely check later whether a file was created.
    audio_path = None

    try:
        # Record audio from the microphone using the requested duration and sample rate.
        recording = _record_microphone(duration, sample_rate)

        # Only play the recording if the caller asked for playback.
        if playback:
            # Play the freshly captured audio through the speaker.
            _play_recording(recording, sample_rate)

        # Save the recording to a temporary WAV file so it can be sent to the ASR model.
        audio_path = _save_recording(recording, sample_rate)

        # Create a Hugging Face client configured with the chosen model, provider, and token.
        client = InferenceClient(model=model, provider=provider, token=api_key)

        # Pass the WAV file path so the client can read the file and infer the audio/wav content type.
        result = client.automatic_speech_recognition(audio=str(audio_path), model=model)

        # Pull the text out of the response and remove extra whitespace around it.
        transcript = result.text.strip()

        # Treat an empty transcript as a failure because we expected text back.
        if not transcript:
            raise RuntimeError("Speech was recorded, but no text was returned.")

        return transcript
    # Catch any exception raised in the process above.
    except Exception as e:
        # Wrap the original error in a voice-specific message while preserving the original cause.
        raise RuntimeError(f"Voice input failed: {e}") from e
    
    # Always run cleanup code, whether the transcription succeeded or failed.
    finally:
        if audio_path and audio_path.exists():
            # Delete the temporary WAV file so the system does not collect leftover recordings.
            audio_path.unlink()
