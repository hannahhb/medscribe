from flask import Flask, render_template, request, jsonify
import os
import base64
import speech_recognition as sr  # optional for real transcription
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    consultation_note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
   
# Add this before the routes to initialize database
with app.app_context():
    db.create_all()
   


@app.route('/')
def index():
    # Renders "templates/index.html"
    return render_template('index.html')


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Expects JSON with:
      - audio: Base64-encoded audio blob
      - notes: List of text notes
    Returns JSON:
      - consultationNote: string
    """
    data = request.json
    patient_name = data.get('patientName')
    audio_base64 = data.get('audio')
    notes = data.get('notes', [])
    if not patient_name or patient_name.strip() == '':
        return jsonify({"error": "Patient name is required"}), 400
    if not audio_base64:
        return jsonify({"error": "No audio data received"}), 400


    # Decode base64 audio
    # Typically looks like "data:audio/webm; codecs=opus;base64,<BASE64_STRING>"
    # We'll split on comma and take the second part
    if ',' in audio_base64:
        audio_base64 = audio_base64.split(',')[1]
    audio_bytes = base64.b64decode(audio_base64)


    # Write to a temporary file
    temp_audio_file = 'temp_audio.wav'
    with open(temp_audio_file, 'wb') as f:
        f.write(audio_bytes)


    # Attempt to transcribe (if speech recognition is installed and working)
    transcription_text = ""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_file) as source:
            audio_data = recognizer.record(source)
            # Use Google Web Speech API by default
            transcription_text = recognizer.recognize_google(audio_data)
    except Exception as e:
        transcription_text = f"[Transcription failed: {e}]"


    # Remove temp file if you want to clean up
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)


    # Combine the transcription + doctor's notes
    combined_notes = "\n".join(notes)


    consultation_note = (
        "---- Consultation Transcript ----\n"
        f"{transcription_text}\n\n"
        "---- Doctor's Notes ----\n"
        f"{combined_notes}\n"
    )
    # Add after creating consultation_note
    new_record = Consultation(
        patient_name=patient_name,
        consultation_note=consultation_note
    )
    db.session.add(new_record)
    db.session.commit()
   
    return jsonify({"consultationNote": consultation_note})


if __name__ == '__main__':
    # Run the Flask app
    # Access this at http://localhost:5000/
    app.run(host='0.0.0.0', port=5001, debug=True)



