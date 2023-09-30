from fastapi import APIRouter,UploadFile, File, HTTPException, Query
from flask import Flask, request, send_file
from starlette.responses import FileResponse
from chatdataloader import FileLoader
from fastapi.responses import StreamingResponse
import io

import os
from helper.help import GetRootDir,rootDir

upload_file_router = APIRouter()

upload_dir = os.path.join(rootDir, "file_upload")  # Replace with the actual path to your CSV files

ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.json', '.md', '.zip', '.rar']


@upload_file_router.get('/get_model')
async def get_model(model: str = Query(..., description="Stock ticker")):
    # Construct the full path to the model file
    global model_dir
    model_filename = os.path.join(model_dir,
                                  model)  # Replace '.h5' with the appropriate extension (.h5 or .pkl)

    if os.path.exists(model_filename):
        # Read the model file as binary data
        with open(model_filename, 'rb') as model_file:
            model_content = model_file.read()

        # Use StreamingResponse to send the model file as a response
        return StreamingResponse(io.BytesIO(model_content), media_type='application/octet-stream',
                                 headers={
                                     "Content-Disposition": f"attachment; filename={model}"})  # Adjust the filename extension
    else:
        return "Model file not found", 404


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