import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import FileResponse
from processor import ProcessorFactory
from utils import sanitize_filename, ensure_dirs

UPLOAD_DIR = 'uploads'
RESULT_DIR = 'results'
ensure_dirs(UPLOAD_DIR, RESULT_DIR)

API_KEY = os.getenv('API_KEY','test123')  # simple API key

app = FastAPI(title='Simple OOP File Processor API')

@app.post('/process-file')
async def process_file(file: UploadFile = File(...), x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid API Key')
    filename = sanitize_filename(file.filename)
    input_path = os.path.join(UPLOAD_DIR, filename)
    with open(input_path,'wb') as f:
        f.write(await file.read())
    try:
        processor = ProcessorFactory.get_processor(filename)
        output_path = processor.process(input_path, RESULT_DIR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return FileResponse(output_path, filename=os.path.basename(output_path))
