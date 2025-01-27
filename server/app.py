import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from llm_local import *
from utils import *
# Flask Setup
app = Flask(__name__)
CORS(app)

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), unique=True, nullable=False)
    consultations = db.relationship('Consultation', backref='patient', lazy=True)
    consultation_count = db.Column(db.Integer, nullable=False, default=0)

class Consultation(db.Model):
    __tablename__ = 'consultation'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    consultation_note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

with app.app_context():
    db.create_all()


# API Endpoint
@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.json
    patient_name = data.get('patientName', '').strip()
    audio_base64 = data.get('audio')
    notes = data.get('notes', [])

    if not patient_name:
        return jsonify({"error": "Patient name is required"}), 400
    if not audio_base64:
        return jsonify({"error": "No audio data received"}), 400

    # Process audio and transcription
    temp_audio_file = decode_audio(audio_base64)
    transcription_text = transcribe_audio_file(temp_audio_file)

    # Generate the consultation note
    combined_notes = "\n".join(notes)
    consultation_note = generate_note(transcription_text, combined_notes)

    # Handle patient and save consultation
    patient = get_or_create_patient(patient_name, Patient, db)
    save_consultation(patient, consultation_note, Consultation, db)

    return jsonify({"consultationNote": consultation_note})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
