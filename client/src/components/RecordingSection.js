import React from 'react';

export default function RecordingSection({
  isRecording,
  startRecording,
  stopRecording
}) {
  return (
    <div className='record-section'>
      <button
        onClick={startRecording}
        disabled={isRecording}
        style={{ marginRight: '10px' }}
      >
        {isRecording ? 'Recording...' : 'Start Recording'}
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Stop Recording
      </button>
    </div>
  );
}

const styles = {
  recordSection: {
    marginBottom: 20,
    background: '#fff',
    padding: 10,
    borderRadius: 8
  },
};
