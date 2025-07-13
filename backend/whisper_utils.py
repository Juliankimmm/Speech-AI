import whisper
import os
import subprocess

# Set the local FFmpeg path (relative to this script)
ffmpeg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ffmpeg", "bin"))
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Load the Whisper model
model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Attempting transcription of: {audio_path}")
        result = model.transcribe(audio_path)
        transcript = result["text"].strip()
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""
