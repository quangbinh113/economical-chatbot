from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationTokenBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from src.prompt.prompt import QA_CHAIN_PROMPT_1, QA_CHAIN_PROMPT_2,QA_CHAIN_PROMPT_3

import openai
from dotenv import load_dotenv, find_dotenv
import os
import time

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


class HandleQA:
    def __init__(self, config):
        self.config = config
        self.embedding = HuggingFaceEmbeddings(
            model_name=config.embedding,
            cache_folder="cache",
            # model_kwargs={"device": "cpu"},
        )
        self.chroma = None
        # self.llm = ChatOpenAI(
        #     model_name="gpt-3.5-turbo",
        #     temperature=0,
        #     verbose=True,
        #     streaming=True,
        #     callback_manager=([StreamingStdOutCallbackHandler()]),
        # )
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k-0613",
            temperature=0,
            verbose=False,
        )
        self.memory = ConversationTokenBufferMemory(llm=self.llm,max_token_limit=1500)
        self.chain = ConversationChain(llm=self.llm, 
                                       memory=self.memory, 
                                       verbose=True,
                                       )
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
  
    def store_db(self, chunks: list[str]) -> None:
        """
        Add chunks to vector store
        Args:
            chunks(list[str]:None): a list of chunks of the crawled text
        Result:
            None
        """
        start = time.time()
        if self.chroma:
            ids = self.chroma.get()["ids"]
            self.chroma.delete(ids=ids)
        self.chroma = Chroma.from_texts(chunks, embedding=self.embedding)
        print(f"Create chroma in: {time.time() - start}")
        return

    def get_query_and_chunk(
        self, query: str, similarity_function: str = "max_marginal_relevance_search"
    ) -> tuple[str, list[str]]:
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

    def ask_gpt(self, query, files):
        """
        Return the answer from the chatGPT
        Args:
            query(str:None): The query that the user asked the chatbot
            files(list[str]:None): list of documentations' local paths
        return:
            answer(str)
        """
        chunks = self.split_context(query, files)
        if len(chunks) > 0:
            self.store_db(chunks)
            query, contents = self.get_query_and_chunk(query)
            contents = "\n".join(contents)
            message = QA_CHAIN_PROMPT_1.format_messages(
                question=query, context=contents
            )
        else:
            message = QA_CHAIN_PROMPT_2.format_messages(question=query)
        # message = QA_CHAIN_PROMPT_3.format_messages(text = query)
        start = time.time()
        answer = self.chain(message[0].content)
        print(f"answer in: {time.time() - start}")

        return answer["response"]