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
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.xml import UnstructuredXMLLoader


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

    def embeddings(self, text):
        '''
            embeddings text
        '''
        pass

    def csv_loader(self, csv_file):
        # #check file and load CSV
        # if uploaded_file :
        # #use tempfile because CSVLoader only accepts a file_path
        # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        # tmp_file.write(uploaded_file.getvalue())
        # tmp_file_path = tmp_file.name
        '''
            load và processing CSV by Langchain -> return chain
        '''
        csv_loader = CSVLoader(file_path=csv_file, encoding="utf-8")
        data = csv_loader.load()
        self.csv_data = []
        for document in data:
            # Initialize an empty string to store the combined text
            combined_text = ""
        
            # Loop through the columns in the document
            for column_name, column_value in document.items():
                # Combine the column name and value as text
                combined_text += f"{column_name}: {column_value} "
        
            # Append the combined text to the text_data list
            self.csv_data.append(combined_text.strip())  # Remove trailing space
        
        return self.csv_data

        # embeddings = OpenAIEmbeddings()
        # vectors = FAISS.from_documents(data, embeddings)
        # chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
        #                                                               retriever=vectors.as_retriever())
        # return chain

    def pdf_loader(self, pdf_file):
        '''
            get text of file PDF -> return text
        '''
        pdf_reader = PyPDFLoader(pdf_file) 

        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            self.pdf_data += page.get_text()

        
        return self.pdf_data


    def markdown_loader(self, markdown_file):
        '''
            get text of file markdown -> return text
        '''
        # Sử dụng markdown để đọc dữ liệu từ tệp Markdown
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_text  = file.read()

        markdown_loader = UnstructuredMarkdownLoader()
        self.markdown_data = markdown_loader.load(markdown_text)

        return self.markdown_data
    

    
    def csv_byte_loader(self, csv_byte):
        # #check file and load CSV
        # if uploaded_file :
        # #use tempfile because CSVLoader only accepts a file_path
        # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        # tmp_file.write(uploaded_file.getvalue())
        # tmp_file_path = tmp_file.name
        '''
            load và processing CSV by Langchain -> return chain
        '''
        csv_loader = CSVLoader(file_bytes=csv_byte, encoding="utf-8")
        data = csv_loader.load()
        self.csv_data = []
        for document in data:
            # Initialize an empty string to store the combined text
            combined_text = ""
        
            # Loop through the columns in the document
            for column_name, column_value in document.items():
                # Combine the column name and value as text
                combined_text += f"{column_name}: {column_value} "
        
            # Append the combined text to the text_data list
            self.csv_data.append(combined_text.strip())  # Remove trailing space
        
        return self.csv_data


    def json_loader(self, json_file_path):
        '''
            get list text file Json -> return text
        '''
        loader = JSONLoader(
        file_path=json_file_path,
        jq_schema='.messages[].content',
        text_content=False)

        documents = loader.load()
        text = []
        for document in documents:
            text.append(document.page_content)

        return text

    def directory_loader(self, directory_file):

        '''
            check directory file -> .zip or rar
            unzip and check types of file in direc
        '''
        # Lấy danh sách tệp trong thư mục và đọc nội dung từ mỗi tệp
        file_list = []
        for filename in os.listdir(directory_file):
            file_path = os.path.join(directory_file, filename)
            if os.path.isfile(file_path):
                extension = self._get_file_extension(filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    if extension == '.zip':
                        # Nếu là tệp ZIP, giải nén và đọc nội dung từ các tệp bên trong
                        with zipfile.ZipFile(file_path, 'r') as zip_file:
                            for inner_filename in zip_file.namelist():
                                with zip_file.open(inner_filename) as inner_file:
                                    file_list.append((inner_filename, inner_file.read().decode('utf-8')))
                    elif extension == '.rar':
                        # Nếu là tệp RAR, giải nén và đọc nội dung từ các tệp bên trong
                        with rarfile.RarFile(file_path, 'r') as rar_file:
                            for inner_filename in rar_file.namelist():
                                with rar_file.open(inner_filename) as inner_file:
                                    file_list.append((inner_filename, inner_file.read().decode('utf-8')))
                    else:
                        # Đối với các tệp có đuôi khác, đọc nội dung từ tệp
                        file_list.append((filename, file.read()))
        # return file_list

        for file in file_list:
            if self._get_file_extension(file) == '.csv':
                # return self.csv_loader(file)

                pass
            
            if self._get_file_extension(file) == '.pdf':
                # return self.pdf_loader(file)
                pass
            
            if self._get_file_extension(file) == '.md':
                # return self.markdown_loader(file)
            
                pass
            if self._get_file_extension(file) == '.json':
                # return self.json_loader(file)
                pass
'''
    sửa dictionary_data thành list_file
    for check list_file rồi get text ném vào self.dic_data
'''

    
 
    