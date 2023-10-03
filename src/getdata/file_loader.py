import os
import pickle
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import JSONLoader
from pathlib import Path
import json
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.xml import UnstructuredXMLLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader 
from langchain.document_loaders.text import TextLoader
import zipfile
import rarfile
# sys.path.append(r"C:\Users\binh.truong\Code\economical-chatbot")

from utils.set_logger import set_logger

logger = set_logger('file_loader.log')

class FileLoader:
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

        # csv_loader = CSVLoader(file_path=csv_file, encoding="utf-8")
        # data = csv_loader.load()
        # self.csv_data = []
        # for document in data:
        #     # Initialize an empty string to store the combined text
        #     combined_text = ""
        
        #     # Loop through the columns in the document
        #     for column_name, column_value in document.items():
        #         # Combine the column name and value as text
        #         combined_text += f"{column_name}: {column_value} "
        
        #     # Append the combined text to the text_data list
        #     self.csv_data.append(combined_text.strip())  # Remove trailing space
        
        # return self.csv_data

    def pdf_loader(self, pdf_file):
        '''
            get text of file PDF -> return documents
        '''
        loader = UnstructuredPDFLoader(pdf_file)  
        self.pdf_data = loader.load()

        # loader = PyPDFLoader(pdf_file)
        # text = ""
        # for page in loader.load_and_split():
        #     text += page.page_content
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
        loader = JSONLoader(
        file_path=json_file_path,
        jq_schema='.messages[].content',
        text_content=False)

        self.json_data = loader.load()

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

        def load_archive_contents(archive_file_path):
            """
            Load the contents of an archive file (either .zip or .rar).

            Args:
                archive_file_path (str): The path to the archive file.

            Returns:
                List[str]: A list of file contents from the archive.
            """
            try:
                archive_documents = []

                if archive_file_path.endswith('.zip'):
                    # Handle .zip files
                    with zipfile.ZipFile(archive_file_path, 'r') as zip_file:
                        for inner_filename in zip_file.namelist():
                            doc = process_directory(inner_filename)
                            # with zip_file.open(inner_filename) as inner_file:
                            #     # Read and decode the content as utf-8
                            #     content = inner_file.read().decode('utf-8')
                            archive_documents.append(doc)

                elif archive_file_path.endswith('.rar'):
                    # Handle .rar files
                    with rarfile.RarFile(archive_file_path, 'r') as rar_file:
                        for inner_filename in rar_file.namelist():
                            doc = process_directory(inner_filename)
                            # with rar_file.open(inner_filename) as inner_file:
                            #     # Read and decode the content as utf-8
                            #     content = inner_file.read().decode('utf-8')
                            archive_documents.append(doc)

                return archive_documents
            
            except Exception as e:
                print(f"Error loading contents from {archive_file_path}: {e}")
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

            # # Create DirectoryLoader instances for each file type
            # pdf_loader = create_directory_loader('.pdf', '/path/to/your/directory')
            # xml_loader = create_directory_loader('.xml', '/path/to/your/directory')
            # csv_loader = create_directory_loader('.csv', '/path/to/your/directory')
            # json_loader = create_directory_loader('.json', '/path/to/your/directory')
            # md_loader = create_directory_loader('.md', '/path/to/your/directory')
            # txt_loader = create_directory_loader('.txt', '/path/to/your/directory')

            # # Load the files
            # pdf_documents = pdf_loader.load()
            # xml_documents = xml_loader.load()
            # csv_documents = csv_loader.load()
            # json_documents = json_loader.load()
            # md_documents = md_loader.load()
            # txt_documents = txt_loader.load()


        
            


# def test_func():
#     a = "123123123"
#     logger.info("test_func")
#     logger.info("aasdfasdfasdf {}".format(a))
    
 
# if __name__ == "__main__":
#     test_func()
#     logger.info('hello world')
#     loader = FileLoader()
    
#     print(loader.csv_loader(r'C:\Users\binh.truong\Code\stock_data.csv'))