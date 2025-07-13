# EchoMind Voice AI Agent

EchoMind is a real-time voice AI agent designed to transcribe user speech, classify user intent with confidence scoring, and generate both text and speech responses dynamically. It is built as a full-stack application with a Python FastAPI backend and a React frontend, integrating modern machine learning models and open-source tools.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Architecture & Pipeline](#architecture--pipeline)
- [Key Features](#key-features)
- [Why These Technologies?](#why-these-technologies)
- [What I Learned](#what-i-learned)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Future Improvements](#future-improvements)

---

## Project Overview

EchoMind listens to user audio, transcribes it into text using OpenAI's Whisper model, determines the user's intent with a hybrid approach of pattern matching and transformer-based sentiment analysis, and generates appropriate text and speech responses with fallback handling for uncertain inputs. The system supports an end-to-end pipeline as well as modular API endpoints.

---

## Technologies Used

### Backend
- **FastAPI** — for building a fast, asynchronous, and lightweight API server.
- **OpenAI Whisper (openai-whisper)** — state-of-the-art speech-to-text model for accurate audio transcription.
- **Transformers (Hugging Face)** — for intent classification using a pre-trained DistilBERT sentiment model.
- **Coqui TTS** — for neural text-to-speech synthesis to generate audio responses.
- **Google Cloud Text-to-Speech (optional)** — alternative TTS engine.
- **Python** — main programming language with libraries like `torch`, `torchaudio`, `pydub` for ML and audio processing.
- **UUID, tempfile, os** — for managing temporary audio files and response audio file generation.
- **CORS Middleware** — enables frontend-backend communication in development.

### Frontend
- **React + TypeScript** — interactive UI with strong typing for better maintainability.
- **MediaRecorder API** — browser-native audio recording capability.
- **Axios** — HTTP client to communicate with backend endpoints.
- **Custom Components** — microphone button, transcript display, and response player for smooth user experience.

---

## Architecture & Pipeline

1. **Audio Recording (Frontend):**  
   User clicks a microphone button to record voice input using browser's MediaRecorder API.

2. **Audio Upload:**  
   The recorded audio (WAV) is sent to the FastAPI backend.

3. **Speech-to-Text Transcription:**  
   Whisper model transcribes the audio to text.

4. **Intent Classification:**  
   Hybrid approach using:  
   - Pattern matching for keywords related to intents like `track_package`, `cancel_order`, `greeting`, etc.  
   - Sentiment analysis via a DistilBERT model to score confidence.

5. **Fallback and Response Routing:**  
   Based on intent and confidence score, fallback logic chooses an appropriate response message.

6. **Text-to-Speech (TTS):**  
   Coqui TTS synthesizes the selected response text into an audio file.

7. **Response Delivery:**  
   The backend returns the transcript, intent, confidence, response text, and URL to the audio response.

8. **Frontend Playback:**  
   React displays the transcript and intent analysis, then plays the TTS audio response automatically.

---

## Key Features

- **Hybrid Intent Detection:** Combining simple pattern matching with deep learning confidence scoring for robust intent classification.
- **Confidence-aware Fallbacks:** If confidence is low, fallback responses prompt the user to rephrase or repeat.
- **Full Pipeline Endpoint:** Single API call to process audio through all stages seamlessly.
- **Logging:** All interactions are logged with timestamps for debugging and analytics.
- **Modular API:** Separate endpoints for transcription, classification, and response generation.
- **Cross-Origin Support:** CORS middleware configured for smooth frontend-backend integration during development.
- **Clean UI:** User-friendly React interface with real-time feedback on recording, processing, and response.

---

## Why These Technologies?

- **FastAPI:** Chosen for its speed, async support, and developer-friendly design to build a scalable backend API.
- **Whisper:** OpenAI’s Whisper model offers highly accurate and robust speech recognition out of the box, reducing the need for custom audio processing.
- **Transformers Sentiment Model:** A pre-trained DistilBERT fine-tuned on SST-2 allows fast and reliable confidence scoring for intent classification.
- **Coqui TTS:** Open-source, easy-to-use neural TTS providing natural-sounding speech synthesis without cloud dependencies.
- **React & MediaRecorder:** Modern frontend stack with native audio recording capabilities offers an intuitive and responsive user experience.
- **Logging & UUID:** Ensures traceability and uniqueness of audio response files for debugging and future scalability.

---

## What I Learned

- **End-to-End Speech AI Pipeline:** Integrating speech recognition, NLP intent classification, and TTS synthesis into a single system.
- **Hybrid NLP Approaches:** Effectively combining rule-based pattern matching with deep learning confidence measures.
- **Async API Development:** Building robust asynchronous endpoints with FastAPI and handling file uploads securely.
- **Audio File Management:** Safely handling audio streaming, temporary files, and serving audio content efficiently.
- **React Hooks & MediaRecorder:** Managing state and recording audio inside a React app with user-friendly controls.
- **Error Handling & Fallbacks:** Designing graceful fallbacks to improve user experience under low-confidence or ambiguous inputs.
- **Deployment Considerations:** Managing CORS, file storage, and model loading in production-like settings.

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- FFmpeg installed and properly linked (or bundled in the project)
- (Optional) Google Cloud TTS credentials if using Google TTS alternative

- Ensure you have the Whisper model downloaded or cache it by running the server once.

### Backend Setup
```bash
uvicorn main:app --host 0.0.0.0 --port 8000

### Frontend Setup
cd frontend
npm install
npm run dev
Visit http://localhost:3000 to interact with the app.

--- 

## Usage

- Click the microphone button to start recording your voice.
- Speak a command related to order tracking, cancellations, greetings, or customer support.
- Stop recording; the system will transcribe your speech, classify the intent, and respond with synthesized speech.
- View the transcript, detected intent, and confidence score on the UI.
- Listen to the AI-generated audio response.

---

## Future Improvements

- Fine-tune a dedicated intent classification model instead of using a sentiment analysis proxy.
- Add multi-turn dialog context for better conversational flow.
- Enhance fallback handling with NLP-based clarification questions.
- Deploy TTS and Whisper models on GPU for faster processing.
- Support more languages and accents for transcription and TTS.
- Implement user authentication and personalized responses.
- Add frontend progress indicators and error recovery.

---

