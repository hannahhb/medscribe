import React from 'react';
import '../App.css'; // or a separate NotesSection.css if you prefer

export default function NotesSection({
  preNotes,
  setPreNotes,
  liveNotes,
  setLiveNotes,
  notes,
  handleAddPreNotes,
  handleAddLiveNotes
}) {
  return (
    <div className="notes-section">
      <h2>Doctor's Notes</h2>
      <textarea
        placeholder="Add notes before session..."
        value={preNotes}
        onChange={(e) => setPreNotes(e.target.value)}
        className="textarea"
      />
      <button onClick={handleAddPreNotes}>Add Pre-Session Notes</button>

      <textarea
        placeholder="Add notes during session..."
        value={liveNotes}
        onChange={(e) => setLiveNotes(e.target.value)}
        className="textarea"
      />
      <button onClick={handleAddLiveNotes}>Add Live Notes</button>

      <h3>All Notes</h3>
      <div className="notes-list">
        {notes.map((n, i) => <p key={i}>{n}</p>)}
      </div>
    </div>
  );
}
