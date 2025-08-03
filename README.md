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



