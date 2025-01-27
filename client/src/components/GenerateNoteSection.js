import React from 'react';

export default function GenerateNoteSection({ isRecording, generateNote }) {
  return (
    <div className="generate-note">
      <button
        onClick={generateNote}
        disabled={isRecording}
      >
        Generate Consultation Note
      </button>
    </div>
  );
}

