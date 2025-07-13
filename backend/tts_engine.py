import os
import subprocess
from TTS.api import TTS

# Initialize TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def generate_speech(text: str, output_path: str) -> bool:
    """
    Generate speech from text using Coqui TTS
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate speech
        tts.tts_to_file(text=text, file_path=output_path)
        
        return os.path.exists(output_path)
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def generate_speech_google(text: str, output_path: str) -> bool:
    """
    Alternative: Generate speech using Google TTS (requires google-cloud-texttospeech)
    """
    try:
        from google.cloud import texttospeech
        
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        
        return True
    
    except Exception as e:
        print(f"Error with Google TTS: {e}")
        return False