# PDF Structured Information Extractor

Extract structured data from PDF documents using OCR and LLM processing.

## Prerequisites
- Python 3.9+
- Tesseract OCR
- (Optional) Llamafile for local LLM
- (Optional) OpenAI API key

## Installation
1. Clone this repo
```bash
git clone [your-repo-url]
cd [repo-name]
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Install tesseract
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install using the .exe
- Use default settings and save in desired path (default: C:/Program Files/Tesseract-OCR/tesseract.exe)

5. Create a .env file in the project root with the following structure:
```text
TESSERACT_PATH = "your_tesseract_path"
OPENAI_API_KEY = "your_api_key_or_sk-local"
OPENAI_API_MODEL = "your_model_name"
```

## Configuration

### Option 1: Local Processing with Llamafile
1. Download a Llama file from https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#other-example-llamafiles.
2. On Windows, rename the file extension from .llama to .exe
3. Run the model server 
```bash
./{NAME OF YOUR FILE.exe} --server
```
4. In another PowerShell window while your llama is runnning (commonly http://127.0.0.1:8080), get your model ID:
```bash
curl http://127.0.0.1:8080/v1/models
```
5. Update your .env file:
```bash
OPENAI_API_KEY = "sk-local"
OPENAI_API_MODEL = "Llama-3.2-3B-Instruct.Q6_K.gguf"  # Your model name from curl
```

### Option 2: OpenAI API Processing
1. Get your API key from https://platform.openai.com
2. Choose your preferred model
3. Update your .env file:
```bash
OPENAI_API_KEY = "your-api-key-here"
OPENAI_API_MODEL = "gpt-4o-mini"  # or your preferred model
```

## Running the Application
Your .env file should look like this example:
```
TESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract.exe"
OPENAI_API_KEY = "######"
OPENAI_API_MODEL = "gpt-4"
```

1. Activate your virtual environment (if not already active):
```bash
.\venv\Scripts\activate
```
2. From the project root directory (containing app/, .env, etc.), run:
```bash
python .\app\main.py
```

## Project Structure
```text
project-root/
│
├── app/                # Application code
├── venv/               # Virtual environment
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## How to use:

After running the app the GUI will pop up:

<img width="1117" height="655" alt="image" src="https://github.com/user-attachments/assets/571da283-9f7d-4412-8e11-a65910f4f5ee" />

1. Select your desired document to analyze using "Select Document" button. In the assets folder of this project the 2 pdfs used as example are given.
2. Select the type of document. Two options are available: Power of Attorney and Tax return.
3. Select "Process file" button and wait.

### Using POA - Tech Task.docx.pdf with local LLM

<img width="1119" height="660" alt="image" src="https://github.com/user-attachments/assets/5a219323-a421-4532-b706-5d42de69d97e" />

### Using POA - Tech Task.docx.pdf with gpt-4o-mini

<img width="1120" height="654" alt="image" src="https://github.com/user-attachments/assets/4572f734-8257-43b0-90ab-97ce0d25bec7" />


### Using tax_return.pdf with tesseract OCR

<img width="1120" height="660" alt="image" src="https://github.com/user-attachments/assets/6cce8e18-010b-4df5-98c9-680ac20ffd3f" />


## Troubleshooting
- Ensure Tesseract path in .env is correct
- Verify your LLM server is running (for local processing)
- Check your API key (for OpenAI processing)
- Make sure all dependencies are installed






