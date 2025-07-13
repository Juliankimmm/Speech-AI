import React, { useState, useRef } from 'react';
import MicrophoneButton from './components/MicrophoneButton.tsx';
import TranscriptDisplay from './components/TranscriptDisplay.tsx';
import ResponsePlayer from './components/ResponsePlayer.tsx';
import { processAudio } from './api.ts';
import './App.css';

interface ProcessingResult {
  transcript: string;
  intent: string;
  confidence: number;
  response_text: string;
  audio_url: string;
}

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processRecording(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setError(null);
    } catch (err) {
      setError('Failed to start recording. Please check microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
    }
  };

  const processRecording = async (audioBlob: Blob) => {
    try {
      const result = await processAudio(audioBlob);
      setResult(result);
    } catch (err) {
      setError('Failed to process audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleMicrophoneToggle = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>EchoMind Voice AI Agent</h1>
        <p>Click the microphone to start speaking</p>
        
        <MicrophoneButton 
          isRecording={isRecording}
          isProcessing={isProcessing}
          onToggle={handleMicrophoneToggle}
        />
        
        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}
        
        {result && (
          <div className="results">
            <TranscriptDisplay 
              transcript={result.transcript}
              intent={result.intent}
              confidence={result.confidence}
            />
            
            <ResponsePlayer 
              responseText={result.response_text}
              audioUrl={result.audio_url}
            />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;