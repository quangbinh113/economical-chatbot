from fastapi import APIRouter, UploadFile, Query
from starlette.responses import FileResponse
from src.getdata.crawler.file_loader import FileLoader
from fastapi.responses import StreamingResponse
import io

import os
from helper.help import  rootDir

upload_file_router = APIRouter()

upload_dir = os.path.join(rootDir, "file_upload")
print(upload_dir)

ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.json', '.md', '.zip', '.rar', '.txt']


@upload_file_router.get('/get_file')
async def get_csv(file_name: str):
    global upload_dir

    _filename = os.path.join(upload_dir, f'{file_name}')
    print(_filename)
    # Check if the file exists
    if os.path.exists(_filename):
        # Send the CSV file as a response
        return FileResponse(_filename, media_type='text/csv',
                            headers={"Content-Disposition": f"attachment; filename={file_name}.csv"})
    else:
        return "CSV file not found", 404


@upload_file_router.post('/upload_file')
async def upload_file(file: UploadFile):
    global upload_dir
    filename = file.filename
    # Xác định loại tệp dựa trên đuôi tệp (file extension)
    repo = FileLoader()
    # file_extension = repo._get_file_extension(filename)
    saved_filename = os.path.join(upload_dir, filename)
    with open(saved_filename, 'wb') as file_upload:
        file_upload.write(file.file.read())

    # documents = repo.load_file(saved_filename)
    
    return {"message": "File uploaded and processed successfully", "filename": filename}


@upload_file_router.get('/read_file')
async def upload_file(file_name: str = Query(description="Skip items")):
    global upload_dir
    repo = FileLoader()
    file_path = os.path.join(upload_dir, file_name)
    # Check if the file exists
    documents = repo.load_file(file_path)
    if os.path.exists(file_path):
        # Return the file as a response
        return documents
    else:
        return {"message": "File not found"}