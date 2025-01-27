import os
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from llm_local import *

import whisper  

app = Flask(__name__)
CORS(app)

# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    consultation_note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

with app.app_context():
    db.create_all()

# Load a Whisper model once at startup. Options: "tiny", "base", "small", "medium", "large".
model = whisper.load_model("tiny")  # or "base", etc.

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.json
    patient_name = data.get('patientName')
    audio_base64 = data.get('audio')
    notes = data.get('notes', [])

    if not patient_name or patient_name.strip() == '':
        return jsonify({"error": "Patient name is required"}), 400
    if not audio_base64:
        return jsonify({"error": "No audio data received"}), 400

    # Decode base64 audio
    if ',' in audio_base64:
        audio_base64 = audio_base64.split(',')[1]
    audio_bytes = base64.b64decode(audio_base64)

    # Write temp file
    temp_audio_file = 'temp_audio.webm'  # We expect webm from the client
    with open(temp_audio_file, 'wb') as f:
        f.write(audio_bytes)

    # Transcribe with Whisper
    try:
        # Whisper can handle .webm if ffmpeg is installed
        result = model.transcribe(temp_audio_file)
        transcription_text = result["text"]
    except Exception as e:
        transcription_text = f"[Transcription failed: {e}]"

    # Remove temp file
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)

    # Combine transcription + notes
    combined_notes = "\n".join(notes)
    consultation_note = generate_note(transcription_text, combined_notes)

    # Save to DB
    new_record = Consultation(patient_name=patient_name, consultation_note=consultation_note)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"consultationNote": consultation_note})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
