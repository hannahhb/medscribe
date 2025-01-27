PROMPT_TEMPLATE = """
You are a medical scribe assistant. 
Your task is to read a raw transcription from a doctor-patient consultation and the doctor's supplemental notes, then produce a structured summary. 
The summary should be organized by standard clinical headings, and should be coherent and concise.

Transcription:
<<<{transcription}>>>

Doctor's Notes:
<<<{doctor_notes}>>>

Please generate a final consultation note in the following format as a JSON file:

Chief Complaint:
History of Present Illness:
Past Medical History:
Medications:
Social/Family History:
Physical Examination / Findings:
Doctor’s Assessment:
Plan / Recommendations:
Additional Comments:

Make sure to integrate both the transcription and the doctor's notes into one cohesive note.
"""