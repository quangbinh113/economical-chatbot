from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from tqdm import tqdm
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from src.prompt.prompt import QA_CHAIN_PROMPT

import openai
from dotenv import load_dotenv,find_dotenv
import os
import time

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']

class HandleQA():
    def __init__(self,config):
        self.config = config
        self.embedding = HuggingFaceEmbeddings(model_name = config.embedding,cache_folder='cache',model_kwargs = {"device": "cpu"})
        self.chroma = None  
        self.memory = ConversationBufferMemory()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.chain = ConversationChain(
                                        llm=self.llm, 
                                        memory = self.memory,
                                        verbose=False
                                    )

    def split_context(self, files:list[str]) -> list[str]:
        """
        Split documents into chunks
        Args: 
            files(list[str]:None): list of documentations' local paths
        Return:
            list of chunks (list[str])
        """
        start = time.time()
        chunk_size = self.config.chunk_size
        chunk_overlap = self.config.chunk_overlap

        r_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )   
        
        chunks = []

        for file in files:
            with open(file,'r',encoding='utf8') as f:
                content = f.read()
                x = r_splitter.split_text(content)
                chunks += x 
        print(f'Splitting in: {time.time()-start}')
        return chunks
    

    # def split_context(self, dir:str = r'C:\Users\anh.do\Desktop\chatbot\data') -> list[str]:
    #     """
    #     Split documents into chunks
    #     Args: 
    #         dir(str:None): path to the crawled data's directory
    #     Return:
    #         list of chunks (list[str])
    #     """
    #     chunk_size = self.config.chunk_size
    #     chunk_overlap = self.config.chunk_overlap

    #     r_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=chunk_size,
    #         chunk_overlap=chunk_overlap
    #     )   
    #     chunks = []

    #     loader = DirectoryLoader(
    #             dir, 
    #             glob="/*.txt", 
    #             show_progress=True,
    #             # use_multithreading=True, 
    #             loader_cls=TextLoader)

    #     docs = loader.load()
        
    #     # for file in files:
    #     #     with open(file,'r',encoding='utf8') as f:
    #     #         content = f.read()
    #     #         x = r_splitter.split_text(content)
    #     #         chunks += x 
                
    #     return docs

    def store_db(self,chunks:list[str])->None:
        """
        Add chunks to vector store
        Args:
            chunks(list[str]:None): a list of chunks of the crawled text
        Result:
            None
        """
        start = time.time()
        if self.chroma:
            ids = self.chroma.get()['ids']
            self.chroma.delete(ids = ids)
        self.chroma = Chroma.from_texts(chunks,embedding = self.embedding)
        print(f'Create chroma in: {time.time() - start}')
        return 
        
    def get_query_and_chunk(self,query:str,similarity_function:str = 'max_marginal_relevance_search')->tuple[str,list[str]]:
        '''
        Return the query and the k-most similar contents
        Args:
            query(str:None): The query that the user asked the chatbot
            similarity_function(str: 'max_marginal_relevance_search'): The type of similarity function use
        return:
            query(str)
            contents(list[str])
        '''
        start = time.time()
        if similarity_function == 'max_marginal_relevance_search':
            similar_chunks = self.chroma.max_marginal_relevance_search(query,k = self.config.number_of_chunk)
    
        elif similarity_function == 'similarity':
            similar_chunks = self.chroma.similarity(query,k = self.config.number_of_chunk)
        
        contents = [content.page_content for content in similar_chunks]
        print(f'Search chunks in: {time.time() - start}')
        return query,contents
    
    def ask_gpt(self,query,files):
        '''
        Return the answer from the chatGPT
        Args:
            query(str:None): The query that the user asked the chatbot
            files(list[str]:None): list of documentations' local paths
        return:
            answer(str)
        '''
        chunks = self.split_context(files)
        self.store_db(chunks)

        query,contents = self.get_query_and_chunk(query)
        contents = '\n'.join(contents)
        
        message = QA_CHAIN_PROMPT.format_messages(question = query,context = contents)
        start = time.time()
        answer = self.chain(message[0].content)
        print(f'answer in: {time.time() - start}')

        return answer['response']
