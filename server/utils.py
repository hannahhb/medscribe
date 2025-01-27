import whisper  
import base64
import os

# Load Whisper Model
model = whisper.load_model("tiny")  # or "base", etc.

# Utility Functions
def decode_audio(audio_base64):
    """Decode base64-encoded audio data and save to a temporary file."""
    if ',' in audio_base64:
        audio_base64 = audio_base64.split(',')[1]
    audio_bytes = base64.b64decode(audio_base64)
    temp_audio_file = 'temp_audio.webm'
    with open(temp_audio_file, 'wb') as f:
        f.write(audio_bytes)
    return temp_audio_file

def transcribe_audio_file(temp_audio_file):
    """Transcribe the audio file using Whisper."""
    try:
        result = model.transcribe(temp_audio_file)
        transcription_text = result["text"]
    except Exception as e:
        transcription_text = f"[Transcription failed: {e}]"
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
    return transcription_text

def get_or_create_patient(patient_name, Patient, db):
    """Retrieve an existing patient or create a new one."""
    patient = Patient.query.filter_by(patient_name=patient_name).first()
    if not patient:
        patient = Patient(patient_name=patient_name)
        db.session.add(patient)
        db.session.flush()  # Flush to generate patient.id for FK reference
    if patient.consultation_count is None:
        patient.consultation_count = 0
    return patient

def save_consultation(patient, consultation_note, Consultation, db):
    """Save the consultation to the database."""
    patient.consultation_count += 1
    new_record = Consultation(patient_id=patient.id, consultation_note=consultation_note)
    db.session.add(new_record)
    db.session.commit()