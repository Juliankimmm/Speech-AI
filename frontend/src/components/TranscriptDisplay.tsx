import React from 'react';

interface TranscriptDisplayProps {
  transcript: string;
  intent: string;
  confidence: number;
}

const TranscriptDisplay: React.FC<TranscriptDisplayProps> = ({ 
  transcript, 
  intent, 
  confidence 
}) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50'; // Green
    if (confidence >= 0.6) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  return (
    <div className="transcript-display">
      <h3>What you said:</h3>
      <p className="transcript">"{transcript}"</p>
      
      <div className="analysis">
        <h4>Analysis:</h4>
        <p><strong>Intent:</strong> {intent}</p>
        <p>
          <strong>Confidence:</strong> 
          <span 
            style={{ 
              color: getConfidenceColor(confidence),
              fontWeight: 'bold',
              marginLeft: '5px'
            }}
          >
            {(confidence * 100).toFixed(1)}%
          </span>
        </p>
      </div>
    </div>
  );
};

export default TranscriptDisplay;