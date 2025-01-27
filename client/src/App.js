import React, { useState } from 'react';
import useAudioRecorder from './hooks/useAudioRecorder';
import { blobToBase64 } from './utils/blobToBase64';
import PatientInfo from './components/PatientInfo';
import NotesSection from './components/NotesSection';
import RecordingSection from './components/RecordingSection';
import GenerateNoteSection from './components/GenerateNoteSection';
import './App.css'; 

export default function App() {
  const [patientName, setPatientName] = useState('');
  const [preNotes, setPreNotes] = useState('');
  const [liveNotes, setLiveNotes] = useState('');
  const [notes, setNotes] = useState([]);
  const [generatedNote, setGeneratedNote] = useState('');

  const {
    isRecording,
    startRecording,
    stopRecording,
    getAudioBlob
  } = useAudioRecorder();

  const handleAddPreNotes = () => {
    const text = preNotes.trim();
    if (text) {
      setNotes((old) => [...old, text]);
      setPreNotes('');
    }
  };

  const handleAddLiveNotes = () => {
    const text = liveNotes.trim();
    if (text) {
      setNotes((old) => [...old, text]);
      setLiveNotes('');
    }
  };

  const generateNote = async () => {
    try {
      const audioBlob = getAudioBlob();
      const base64Audio = await blobToBase64(audioBlob);

      const response = await fetch('http://localhost:5001/api/transcribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patientName,
          audio: base64Audio,
          notes
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Transcription error:', errorData);
        alert('An error occurred: ' + (errorData.error || 'Unknown error'));
        return;
      }

      const data = await response.json();
      setGeneratedNote(data.consultationNote || 'No note generated.');
    } catch (error) {
      console.error('Error in fetch:', error);
      alert('An error occurred while sending data to the server.');
    }
  };

  return (
    <div className="container">
      <h1>Consultation Recorder </h1>

      <PatientInfo
        patientName={patientName}
        setPatientName={setPatientName}
      />

      <NotesSection
        preNotes={preNotes}
        setPreNotes={setPreNotes}
        liveNotes={liveNotes}
        setLiveNotes={setLiveNotes}
        notes={notes}
        handleAddPreNotes={handleAddPreNotes}
        handleAddLiveNotes={handleAddLiveNotes}
      />

      <RecordingSection
        isRecording={isRecording}
        startRecording={startRecording}
        stopRecording={stopRecording}
      />

      <GenerateNoteSection
        isRecording={isRecording}
        generateNote={generateNote}
      />

      <div className="output-section">
        <h2>Consultation Note Output</h2>
        <pre className="pre-block">{generatedNote}</pre>
      </div>
    </div>
  );
}
