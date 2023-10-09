from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import time
from langchain.docstore.document import Document
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Union
from langchain.text_splitter import RecursiveCharacterTextSplitter

DB_PATH = 'src/model/chroma'

class BaseChroma:
    def __init__(self,config):
        self.config = config
        
        self.embedding = HuggingFaceEmbeddings(
        model_name=config.embedding,
        cache_folder="cache",
        # model_kwargs={"device": "cpu"},
        )

        self.chroma = None
    
    def save_chroma(self,chunks:list[Union[str,Document]])->None:
        pass

    def get_query_and_chunk(
        self, query: str, similarity_function: str = "max_marginal_relevance_search"
    ) -> tuple[str, list[Union[str,Document]]]:
        """
        Return the query and the k-most similar contents
        Args:
            query(str:None): The query that the user asked the chatbot
            similarity_function(str: 'max_marginal_relevance_search'): The type of similarity function use
        return:
            query(str)
            contents(list[str])
        """
        start = time.time()
        if similarity_function == "max_marginal_relevance_search":
            similar_chunks = self.chroma.max_marginal_relevance_search(
                query, k=self.config.number_of_chunk
            )

        elif similarity_function == "similarity":
            similar_chunks = self.chroma.similarity(
                query, k=self.config.number_of_chunk
            )

        contents = [content.page_content for content in similar_chunks]
        print(f"Search chunks in: {time.time() - start}")
        return query, contents

class CrawlChroma(BaseChroma):
    def __init__(self,config):
        super().__init__(config)
        self.chroma = None
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap
        )

    
    def split_context(self, query: str, documents : list[str]) -> list[str]:
        """
        Split documents into chunks
        Args:
            query(str:None): question need to be answered
            content(list[str]:None): list of documents
        Return:
            list of chunks (list[str])
        """
        start = time.time()

        chunks = []

        for document in documents:
            chunks +=self.splitter.split_text(document)

        if len(chunks) <= 10:
            print(f"Splitting in: {time.time()-start}")
            return chunks
        
        tf_idf = TfidfVectorizer()
        tf_idf.fit(chunks + [query])
        embedded_query = tf_idf.transform([query])

        similarity = []
        chunks = np.array(chunks)
        for chunk in chunks:
            similarity.append(
                cosine_similarity(tf_idf.transform([chunk]), embedded_query)
            )

        chunks = chunks[np.array(similarity).argsort()[-10:]]
        print(f"Splitting in: {time.time()-start}")

        return [item.squeeze()[()] for item in chunks]
    
    def save_chroma(self, chunks: list[str]) -> None:
        """
        Add chunks to vector store
        Args:
            chunks(list[str]:None): a list of chunks of the crawled text
        Result:
            None
        """
        start = time.time()
        if self.chroma:
            self.chroma.delete_collection()   
        self.chroma = Chroma.from_texts(chunks, embedding=self.embedding, collection_name = 'crawl_data')
        print(f"Create chroma in: {time.time() - start}")
        return

class DocumentChroma(BaseChroma):
    def __init__(self,config):
        super().__init__(config)
        self.chroma = Chroma(persist_directory=DB_PATH,embedding_function = self.embedding,collection_name = 'document_data')
    
    def save_chroma(self, chunks: list[Document]) -> None:
        self.chroma.add_documents(chunks)
    