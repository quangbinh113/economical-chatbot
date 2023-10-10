from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationTokenBufferMemory
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from src.prompt.prompt import QA_CHAIN_PROMPT_1, QA_CHAIN_PROMPT_2,QA_CHAIN_PROMPT_3
from src.model.base_chroma import DocumentChroma, CrawlChroma
import openai
from dotenv import load_dotenv, find_dotenv
import os
import asyncio
import time

# import asyncio
# from typing import AsyncIterable

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
        self.callback = AsyncIteratorCallbackHandler()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            verbose=False,
            streaming=True,
            callbacks=[self.callback],
        )
    
        self.memory = ConversationTokenBufferMemory(llm=self.llm,max_token_limit=1500)
        self.chain = ConversationChain(llm=self.llm, 
                                       memory=self.memory, 
                                       verbose=True,
                                       )

    def get_message(self, query: str, crawl_data:list[str] = None, documents:list[Document] = None):
        if len(crawl_data) > 0:
            self.chroma = CrawlChroma(self.config)
            chunks = self.chroma.split_context(query,crawl_data)
        
            # if len(chunks) > 0:
            self.chroma.save_chroma(chunks)
            query, contents = self.chroma.get_query_and_chunk(query)
            contents = "\n".join(contents)
            message = QA_CHAIN_PROMPT_1.format_messages(
                question=query, context=contents
            )            
        else:    
            message = QA_CHAIN_PROMPT_2.format_messages(question=query)

        if documents:
            self.chroma = DocumentChroma(self.config)

            self.chroma.save_chroma(documents)
    
            query, contents = self.chroma.get_query_and_chunk(query)
            contents = "\n".join(contents)
            message = QA_CHAIN_PROMPT_1.format_messages(
                question=query, context=contents
            )
        return message

    async def ask_gpt(self, query: str, crawl_data:list[str] = None, documents:list[Document] = None):
        """
        Return the answer from the chatGPT
        Args:
            query(str:None): The query that the user asked the chatbot
            crawl_data(list[str]:None): list of documentations' local paths
        return:
            answer(str)
        """
        message = ' '
        message = self.get_message(query,crawl_data,documents) 

        task = asyncio.create_task(
            self.chain.arun(input=message[0].content)
        )
        
        try:
            async for token in self.callback.aiter():
                yield token
        except Exception as e:
            print(f"Caught exception: {e}")
    
        await task
