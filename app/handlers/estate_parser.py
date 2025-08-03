import os
from openai import OpenAI
from textwrap import dedent
from dotenv import load_dotenv
import json
import re

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
api_model = os.getenv("OPENAI_API_MODEL")  

# Client 
use_local_model = api_key.startswith("sk-local")
api_base = "http://127.0.0.1:8080/v1" if use_local_model else None #openai models do not require endpoint but locals do
client = OpenAI(api_key=api_key, base_url=api_base)

def text_completion(document_text):
    '''
    This function calls the LLM model to complete the text.
    The response is extracted and formated to extract a desired json structure.

    The prompt was built using the build_prompt function that explicitly asks for an output structure with some specific instructions.
    '''
    response = client.chat.completions.create(
        model=api_model, 
        messages=[
            {"role": "user", "content": build_prompt(document_text)}
        ]
    )
    content = response.choices[0].message.content
 
    # Clean output
    try:
        match = re.search(r"<json>\s*(\{.*?\})\s*</json>", content, re.DOTALL)
        cleaned = match.group(1)
    except:
        return content

    # Dict format
    try:
        parsed = json.loads(cleaned)
        print(parsed)
        return parsed
    except json.JSONDecodeError as e:
        print("Cannot parse json", e)
        return cleaned
    


def build_prompt(doc_text: str):
    return dedent(f"""
        Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.
        
        {{
            "title": string,                // Document title
            "document_date": string,       // Document date in any format
            "client_name": string,         // Name of the principal client
            "governing_law_state": string, // State or region
            "named_agent": string,         // Name of the agent
            "summary": string              // Brief summary of the document
        }}
        
        Please output the extracted information in JSON format. Do not output anything except for the extracted information. Do not add any clarifying information. Do not add any fields that are not in the schema. If the text contains attributes that do not appear in the schema, please ignore them. All output must be in JSON format and follow the schema specified above. Wrap the JSON in <json> tags at end and beginning.
        If any information is missing fill it with an explicit no data found.

        Document:
        \"\"\"
        {doc_text}
        \"\"\"
    """)
