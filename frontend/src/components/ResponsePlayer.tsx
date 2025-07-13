import React, { useRef, useEffect } from 'react';

interface ResponsePlayerProps {
  responseText: string;
  audioUrl: string;
}

const ResponsePlayer: React.FC<ResponsePlayerProps> = ({ 
  responseText, 
  audioUrl 
}) => {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    // Auto-play the response (note: many browsers require user interaction first)
    if (audioRef.current) {
      audioRef.current.play().catch(err => {
        console.log('Auto-play prevented:', err);
      });
    }
  }, [audioUrl]);

  return (
    <div className="response-player">
      <h3>AI Response:</h3>
      <p className="response-text">"{responseText}"</p>
      
      <audio 
        ref={audioRef}
        controls
        src={`http://localhost:8000${audioUrl}`}
        className="audio-player"
      >
        Your browser does not support audio playback.
      </audio>
    </div>
  );
};

export default ResponsePlayer;