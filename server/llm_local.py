from llama_cpp import Llama
import pandas as pd
from pathlib import Path
from note import *

import json
example = pd.read_json("prompts/example.json")
transciption = example["examples"][0]["transcription"] 
notes = example["examples"][0]["doctor_notes"] 
def generate_note(TRANSCRIPTION_TEXT=transciption, DOCTOR_NOTES=notes):

    
    
    formatted_prompt = PROMPT_TEMPLATE.format(
        transcription=TRANSCRIPTION_TEXT.strip(),
        doctor_notes=DOCTOR_NOTES.strip()
    )

    llm = Llama(
        model_path="./models/Ministral-8B-Instruct-2410-Q5_K_S.gguf",
        n_gpu_layers=-1, # Uncomment to use GPU acceleration
        seed=1337, # Uncomment to set a specific seed
        n_ctx=2048, # Uncomment to increase the context window
        verbose=False
    )
    output = llm(
        formatted_prompt, # Prompt
        max_tokens=1024,
        # Generate up to 32 tokens, set to None to generate up to the end of the context window
        #   stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
        # echo=True # Echo the prompt back in the output
    ) # Generate a completion, can also call create_completion

    return(output['choices'][0]['text'])

# print(generate_note())