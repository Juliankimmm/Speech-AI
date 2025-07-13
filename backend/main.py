from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import tempfile
import uuid
from datetime import datetime
import json

from whisper_utils import transcribe_audio
from intent_model import get_intent
from tts_engine import generate_speech
from fallback_logic import route_intent

app = FastAPI(title="EchoMind Voice AI Agent")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def log_interaction(data: dict):
    """Log all interactions for debugging and analysis"""
    timestamp = datetime.now().isoformat()
    log_entry = {"timestamp": timestamp, **data}
    
    with open("logs/interactions.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile = File(...)):
    """Transcribe audio file to text"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            content = await audio.read()
            tmp_file.write(content)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            tmp_file_path = tmp_file.name

        print(f"Saved audio to: {tmp_file_path} | Size: {len(content)} bytes")

        transcript = transcribe_audio(tmp_file_path)
        os.unlink(tmp_file_path)

        log_interaction({"action": "transcribe", "result": transcript})
        return {"transcript": transcript}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/classify")
async def classify_intent(data: dict):
    """Classify intent from text"""
    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        intent, confidence = get_intent(text)

        log_interaction({
            "action": "classify",
            "text": text,
            "intent": intent,
            "confidence": confidence
        })

        return {
            "intent": intent,
            "confidence": confidence,
            "text": text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/respond")
async def generate_response(data: dict):
    """Generate TTS response based on intent"""
    try:
        intent = data.get("intent", "")
        confidence = data.get("confidence", 0.0)

        response_text = route_intent(intent, confidence)

        audio_filename = f"response_{uuid.uuid4()}.wav"
        audio_path = os.path.join("logs", audio_filename)
        generate_speech(response_text, audio_path)

        log_interaction({
            "action": "respond",
            "intent": intent,
            "confidence": confidence,
            "response_text": response_text,
            "audio_file": audio_filename
        })

        return {
            "response_text": response_text,
            "audio_url": f"/audio/{audio_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")

@app.post("/full_pipeline")
async def full_pipeline(audio: UploadFile = File(...)):
    """Complete pipeline: audio -> transcript -> intent -> response"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            content = await audio.read()
            tmp_file.write(content)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            tmp_file_path = tmp_file.name

        print(f"Received audio at {tmp_file_path} | Size: {len(content)} bytes")

        # Step 1: Transcribe
        transcript = transcribe_audio(tmp_file_path)
        os.unlink(tmp_file_path)

        # Step 2: Classify intent
        intent, confidence = get_intent(transcript)

        # Step 3: Generate response
        response_text = route_intent(intent, confidence)

        # Step 4: Generate speech
        audio_filename = f"response_{uuid.uuid4()}.wav"
        audio_path = os.path.join("logs", audio_filename)
        generate_speech(response_text, audio_path)

        log_interaction({
            "action": "full_pipeline",
            "transcript": transcript,
            "intent": intent,
            "confidence": confidence,
            "response_text": response_text,
            "audio_file": audio_filename
        })

        return {
            "transcript": transcript,
            "intent": intent,
            "confidence": confidence,
            "response_text": response_text,
            "audio_url": f"/audio/{audio_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files"""
    audio_path = os.path.join("logs", filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/wav")
    else:
        raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
