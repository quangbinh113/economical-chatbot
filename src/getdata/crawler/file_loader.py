import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import JSONLoader
from pathlib import Path
import json
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.xml import UnstructuredXMLLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader 
from langchain.document_loaders.text import TextLoader
import zipfile
import rarfile
import json
from pathlib import Path
from langchain.document_loaders import PyPDFLoader


class FileLoader(object):
    def __init__(self):
        self.csv_data = None
        self.pdf_data = None
        self.markdown_data = None
        self.directory_data = None
        self.json_data = None
        self.text = None

    def _get_file_extension(self, filename):
        '''
            func return .name file
        '''
        return os.path.splitext(filename)[1]    

    def csv_loader(self, csv_file):
        '''
            load và processing CSV by Langchain -> return documents
        '''
        loader = CSVLoader(file_path=csv_file, encoding="utf-8",csv_args={
                'delimiter': ',',})
        self.csv_data = loader.load()

        return self.csv_data

    def pdf_loader(self, pdf_file):
        '''
            get text of file PDF -> return documents
        '''
        loader = PyPDFLoader(pdf_file)  
        self.pdf_data = loader.load()

        return self.pdf_data

    def markdown_loader(self, markdown_file):
        '''
            get text of file markdown -> return documents
        '''
        markdown_loader = UnstructuredMarkdownLoader(markdown_file)
        self.markdown_data = markdown_loader.load()
        return self.markdown_data
    
    def json_loader(self, json_file_path):
        '''
            get list text file Json -> return documents
        '''
        self.json_data = json.loads(Path(json_file_path).read_text())
        return self.json_data

    def directory_loader(self, directory_file):
        '''
            check directory file -> .zip or rar
            unzip and check types of file in direc
        '''
        # Lấy danh sách tệp trong thư mục và đọc nội dung từ mỗi tệp
        loaders = {
            '.pdf': PyMuPDFLoader,
            '.xml': UnstructuredXMLLoader,
            '.csv': CSVLoader,
            '.json': JSONLoader,
            '.md': UnstructuredMarkdownLoader,
            'txt': TextLoader,
        }
        def _load_archive_contents(directory_file):
            """
            Load the contents of an archive file (either .zip or .rar).

            Args:
                archive_file_path (str): The path to the archive file.

            Returns:
                List[str]: A list of file contents from the archive.
            """
            try:
                archive_documents = []
                if directory_file.endswith('.zip'):
                    # Handle .zip files
                    with zipfile.ZipFile(directory_file, 'r') as zip_file:
                        for inner_filename in zip_file.namelist():
                            doc = process_directory(inner_filename)
                            # with zip_file.open(inner_filename) as inner_file:
                            #     # Read and decode the content as utf-8
                            #     content = inner_file.read().decode('utf-8')
                            archive_documents.append(doc)
                elif directory_file.endswith('.rar'):
                    # Handle .rar files
                    with rarfile.RarFile(directory_file, 'r') as rar_file:
                        for inner_filename in rar_file.namelist():
                            doc = process_directory(inner_filename)
                            # with rar_file.open(inner_filename) as inner_file:
                            #     # Read and decode the content as utf-8
                            #     content = inner_file.read().decode('utf-8')
                            archive_documents.append(doc)
                return archive_documents
            except Exception as e:
                print(f"Error loading contents from {directory_file}: {e}")
                return []

        def create_directory_loader(file_type, directory_file):
            return DirectoryLoader(
                path=directory_file,
                glob=f"**/*{file_type}",
                loader_cls=loaders[file_type],
            )

        def process_directory(directory_file):
            documents = {}
            for file_type, loader_cls in loaders.items():
                loader = create_directory_loader(file_type, directory_file, loader_cls)
                documents[file_type] = loader.load()

            return documents
        
        return _load_archive_contents(directory_file)

 
if __name__ == "__main__":
    # load = FileLoader().csv_loader(r'C:\Users\binh.truong\Code\economical-chatbot\file_upload\VIC.csv')
    # load2 = FileLoader().json_loader(r'C:\Users\binh.truong\Code\economical-chatbot\file_upload\tesst.json')
    load3 = FileLoader().pdf_loader(r'C:\Users\binh.truong\Code\economical-chatbot\data\1903.11800v1.pdf') 

    print(load3)