from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationTokenBufferMemory
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from src.prompt.prompt import QA_CHAIN_PROMPT_1, QA_CHAIN_PROMPT_2,QA_CHAIN_PROMPT_4,QA_CHAIN_PROMPT_3
from src.model.base_chroma import DocumentChroma, CrawlChroma
from src.getdata.crawler.utils import answer_to_json, preprocess_visualize
from src.getdata.crawler.stock_visualizer import StockVisualization

import openai
from dotenv import load_dotenv, find_dotenv
import os
import asyncio
import time

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

        self.llm_plotting = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            verbose=True,
        )

        self.memory = ConversationTokenBufferMemory(llm=self.llm,max_token_limit=1500)
        self.chain = ConversationChain(llm=self.llm, 
                                       memory=self.memory, 
                                       verbose=True,
                                       )
        
        self.current_query = ''
        self.current_answer = ''

    def get_message(self, query: str, crawl_data:list[str] = None, documents:list[Document] = None):
        if documents:
            self.chroma = DocumentChroma(self.config)
            start = time.time()
            # self.chroma.save_chroma(documents)
            # print('save to chroma in:',time.time()-start)
            metadata = documents[0].metadata['source']
            
   
            query, contents = self.chroma.get_query_and_chunk(query,metadata)
            contents = "\n".join(contents)
     
            message = QA_CHAIN_PROMPT_4.format_messages(
                question=query, context=contents
            )

            return message
        
        if crawl_data!=None and len(crawl_data) > 0:
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

        return message

    def reset_callback(self):
        self.callback.done.clear()

    def plot(self,query:str,full_answer:str)->None:
        query_prompt = QA_CHAIN_PROMPT_3.format_messages(
                text=query
            )   
        query = self.llm_plotting(query_prompt)
        data_to_plot = answer_to_json(query.content)
        if not data_to_plot:
            query_prompt = QA_CHAIN_PROMPT_3.format_messages(text=full_answer)   
            full_answer= self.llm_plotting(query_prompt)
            data_to_plot = answer_to_json(full_answer.content)

        if not data_to_plot:
            return

        plot_data = preprocess_visualize(data_to_plot)
        
        if not plot_data:
            return
    
        plotter = StockVisualization(
            symbol = plot_data['stock_code'],
            start_date = plot_data['end_date'],
            end_date = plot_data['start_date']
        )

        plotter.plot_data()


    async def ask_gpt(self, query: str, crawl_data:list[str] = None, documents:list[Document] = None):
        """
        Return the answer from the chatGPT
        Args:
            query(str:None): The query that the user asked the chatbot
            crawl_data(list[str]:None): list of documentations' local paths
        return:
            answer(str)
        """
        self.current_query = query
        message = self.get_message(self.current_query,crawl_data,documents) 
        task = asyncio.create_task(
            self.chain.arun(input=message[0].content)
        )
        
        try:
            async for token in self.callback.aiter():
                self.current_answer += token
                yield token
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            # self.current_query = query
            # self.current_answer = full_answer
            self.callback.done.set()
            # self.plot(self.current_query,self.current_answer)
                
        await task  
        
