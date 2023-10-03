from fastapi import APIRouter,UploadFile, File, HTTPException, Query
from flask import Flask, request, send_file
from starlette.responses import FileResponse
from DataLoader.chatdataloader import FileLoader
from fastapi.responses import StreamingResponse
import io

import os
from helper.help import GetRootDir,rootDir

upload_file_router = APIRouter()

upload_dir = os.path.join(rootDir, "file_upload")  # Replace with the actual path to your CSV files

ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.json', '.md', '.zip', '.rar']


@upload_file_router.post('/upload')
async def upload_file(file: UploadFile):
    global upload_dir

    filename = file.filename
    # Xác định loại tệp dựa trên đuôi tệp (file extension)
    file_extension = FileLoader._get_file_extension(filename)

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type {file_extension}")

    saved_filename = os.path.join(upload_dir, f'{file_extension}')

    with open(saved_filename, 'wb') as buffer:
        # Write the uploaded file's contents to the new file
        buffer.write(file.file.read())


    return {"message": "File uploaded successfully"}


@upload_file_router.post('/file-process')
async def file_process(file: UploadFile):
    global upload_dir

    filename = file.filename
    print(filename)

    FileLoader().csv_byte_loader(file.file.read())

    return {"message": "File uploaded successfully"}

# @upload_file.get('/get_csv')
# async def get_csv(ticker: str = Query(..., description="Stock ticker")):
#     global csv_dir
#     # Construct the full path to the CSV file
#     print(f'csv dir : {csv_dir} ')
#     csv_filename = os.path.join(csv_dir, f'{ticker}.csv')

#     print(csv_filename)

#     # Check if the file exists
#     if os.path.exists(csv_filename):
#         # Send the CSV file as a response
#         return FileResponse(csv_filename, media_type='text/csv',
#                             headers={"Content-Disposition": f"attachment; filename={ticker}.csv"})
#     else:
#         return "CSV file not found", 404