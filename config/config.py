# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    chunk_size: int
    chunk_overlap: int
    embedding:str
    similarity_function:str
    number_of_chunk: int

config = Config(
    chunk_size = 1000,
    chunk_overlap=0,
    embedding = "keepitreal/vietnamese-sbert",
    similarity_function = "max_marginal_relevance_search",
    number_of_chunk = 3
)
#  {

#     "chunk_content":{
#                  "chunk_size":1000,
#              "chunk_overlap":0
#          },
#          "embedding":"keepitreal/vietnamese-sbert",
#          "similarity_function":"max_marginal_relevance_search"
#      }
# print(config)
