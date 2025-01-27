import React from 'react';
import '../App.css'; // or a separate NotesSection.css if you prefer

export default function PatientInfo({ patientName, setPatientName }) {
  return (
    <div className="patient-section">
      <h2>Patient Information</h2>
      <label htmlFor="patientName">Patient Name:</label>
      <input
        type="text"
        id="patientName"
        required
        value={patientName}
        onChange={(e) => setPatientName(e.target.value)}
        style={{ marginLeft: '10px' }}
      />
    </div>
  );
}
