import os
from openai import OpenAI
from pydantic import BaseModel
from textwrap import dedent
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Configuración desde .env
api_base = os.getenv("OPENAI_API_BASE_URL")  
api_key = os.getenv("OPENAI_API_KEY")
api_model = os.getenv("OPENAI_API_MODEL")    

# Cliente Azure OpenAI
client = OpenAI(
    base_url= api_base, # "http://<Your api-server IP>:port"
    api_key = api_key
)

class PowerOfAttorneyData(BaseModel):
    title: str
    document_date: str
    client_name: str
    governing_law_state: str
    named_agent: str
    summary: str

def text_completion(document_text):
    response = client.chat.completions.create(
        model=api_model,  # <- IMPORTANTE: usar "deployment_id", no "model"
        messages=[
            {"role": "user", "content": build_prompt(document_text)}
        ]
    )
    content = response.choices[0].message.content
    print(content)
    # Clean output
    match = re.search(r"<json>\s*(\{.*?\})\s*</json>", text, re.DOTALL)
    json_str = match.group(1)
    # Dict format
    try:
        parsed = json.loads(cleaned)
        print(parsed)
        return cleaned
    except json.JSONDecodeError as e:
        print("Error al parsear JSON:", e)

def build_prompt(doc_text: str):
    return dedent(f"""
        Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.
        
        {{
          "title": "...",
          "document_date": "...",
          "client_name": "...",
          "governing_law_state": "...",
          "named_agent": "...",
          "summary": "..."
        }}
        
        Please output the extracted information in JSON format. Do not output anything except for the extracted information. Do not add any clarifying information. Do not add any fields that are not in the schema. If the text contains attributes that do not appear in the schema, please ignore them. All output must be in JSON format and follow the schema specified above. Wrap the JSON in <json> tags.
        
        Document:
        \"\"\"
        {doc_text}
        \"\"\"
    """)
