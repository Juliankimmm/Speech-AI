import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
});

export interface ProcessingResult {
  transcript: string;
  intent: string;
  confidence: number;
  response_text: string;
  audio_url: string;
}

export const processAudio = async (audioBlob: Blob): Promise<ProcessingResult> => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  try {
    const response = await api.post('/full_pipeline', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error processing audio:', error);
    throw new Error('Failed to process audio');
  }
};

export const transcribeAudio = async (audioBlob: Blob): Promise<{ transcript: string }> => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  const response = await api.post('/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const classifyIntent = async (text: string): Promise<{ intent: string; confidence: number }> => {
  const response = await api.post('/classify', { text });
  return response.data;
};