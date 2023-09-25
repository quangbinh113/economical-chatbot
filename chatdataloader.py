import os
import pandas as pd
import PyPDF2
import markdown
import zipfile
import rarfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI

class ChatDataLoader:
    def __init__(self):
        self.csv_data = None
        self.pdf_data = None
        self.markdown_data = None
        self.directory_data = None
        self.json_data = None
        self.text = None

    def _get_file_extension(self, filename):
        # Hàm này trả về đuôi tệp của tệp với tên filename
        return os.path.splitext(filename)[1]

    def embeddings(self, text):

        pass

    def CsvLoader(self, csv_file_path):
        # Sử dụng pandas để đọc dữ liệu từ tệp CSV
        csv_loader = CSVLoader(file_path=csv_file_path, encoding="utf-8")
        data = csv_loader.load()
        embeddings = OpenAIEmbeddings()
        vectors = FAISS.from_documents(data, embeddings)
        


    def PdfLoader(self, pdf_file_path):
        pdf_reader = PyPDFLoader(pdf_file_path) 

        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.get_text()
        
        # Kết quả là biến text chứa toàn bộ nội dung văn bản từ tệp PDF
        return text


    def MarkDownLoader(self, markdown_file_path):
        # Sử dụng markdown để đọc dữ liệu từ tệp Markdown
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            self.markdown_data = markdown.markdown(file.read())

    def JsonLoader(self, json_file_path):
        pass

    def DirectoryLoader(self, directory_path):
        # Lấy danh sách tệp trong thư mục và đọc nội dung từ mỗi tệp
        self.directory_data = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                extension = self._get_file_extension(filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    if extension == '.zip':
                        # Nếu là tệp ZIP, giải nén và đọc nội dung từ các tệp bên trong
                        with zipfile.ZipFile(file_path, 'r') as zip_file:
                            for inner_filename in zip_file.namelist():
                                with zip_file.open(inner_filename) as inner_file:
                                    self.directory_data.append((inner_filename, inner_file.read().decode('utf-8')))
                    elif extension == '.rar':
                        # Nếu là tệp RAR, giải nén và đọc nội dung từ các tệp bên trong
                        with rarfile.RarFile(file_path, 'r') as rar_file:
                            for inner_filename in rar_file.namelist():
                                with rar_file.open(inner_filename) as inner_file:
                                    self.directory_data.append((inner_filename, inner_file.read().decode('utf-8')))
                    else:
                        # Đối với các tệp có đuôi khác, đọc nội dung từ tệp
                        self.directory_data.append((filename, file.read()))


