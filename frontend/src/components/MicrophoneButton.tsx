import React from 'react';

interface MicrophoneButtonProps {
  isRecording: boolean;
  isProcessing: boolean;
  onToggle: () => void;
}

const MicrophoneButton: React.FC<MicrophoneButtonProps> = ({ 
  isRecording, 
  isProcessing, 
  onToggle 
}) => {
  const getButtonText = () => {
    if (isProcessing) return 'Processing...';
    if (isRecording) return 'Recording... (Click to stop)';
    return '🎙️ Click to speak';
  };

  const getButtonClass = () => {
    if (isProcessing) return 'mic-button processing';
    if (isRecording) return 'mic-button recording';
    return 'mic-button';
  };

  return (
    <button 
      className={getButtonClass()}
      onClick={onToggle}
      disabled={isProcessing}
    >
      {getButtonText()}
    </button>
  );
};

export default MicrophoneButton;