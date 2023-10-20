import hashlib
from typing import Union
from fastapi import UploadFile
import os
from io import BufferedReader, BytesIO
from io import BufferedReader

def calculate_checksum(file:Union[UploadFile,str])->str:
    md5 = hashlib.md5()

    if isinstance(file,str):
        with open(file, "rb") as f:
            while True:
                data = f.read(8192)  # Read the file in 8KB chunks
                if not data:
                    break
                md5.update(data)
    else:
        file_buffer = BytesIO(file.file.read())
        while True:
            # file_contents = file.file
            # file = BufferedReader(file_contents)
            
            data = file_buffer.read(8192)  # Read the file in 8KB chunks
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()

def check_file_exist(file:UploadFile,persistant_folder:str = './file_upload'):
    
    current_checksum = calculate_checksum(file)

    for root, _, files in os.walk(persistant_folder):
        for file_path in files:
            file_checksum = calculate_checksum(os.path.join(root,file_path))
            if file_checksum == current_checksum:
                return file_path
    
    return None

