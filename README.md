# medscribe: Scribe for Patient Appointments

## Project Overview
**Scribe for Patient Appointments** is a Flask-based web application designed to transcribe audio recordings of patient consultations using OpenAI's Whisper model. It stores transcription results alongside additional consultation notes in a SQLite database, making it easier⏰ for healthcare providers to manage and review patient consultations😷. Tested on MacBook Pro M3 Chip  

## Features
- Audio transcription of patient appointments using Whisper. 🤫
- Note generation from transcript and consult notes in structured format using Mistral served locally with llama-cpp-python.

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm 

### Installation

**Clone the repository**
   ```bash
   git clone https://github.com/hannahhb/medscribe.git
   cd medscribe
   ```
**Setup and activate python environment**
 ```bash
 conda create -n medscribe python=3.12 anaconda
 conda activate medscribe 
```
**Install requirements for python**
```bash
pip install -r requirements.txt
```
Make sure to install the LLM GGUF Optimised model and place it in a new directory models/ \
You can pick any GGUF and change path in server/llm_local.py
Initially I've used [Ministral-8B-Instruct-2410-GGUF](https://huggingface.co/bartowski/Ministral-8B-Instruct-2410-GGUF) for testing.

### Running the backend

Run the backend using Python:
```bash
python server/app.py
```

### Running the frontend
Go to client/ and install 
```bash
cd client
npm install
```

Run the frontend using npm:
```bash
npm start
```
Then you can navidagate to http://localhost:3000/ to use the website :)

***And now you're ready to go!*** \
<img width="723" alt="image" src="https://github.com/user-attachments/assets/4e37503d-2212-4bc7-8169-37fc92d89ecb" />





