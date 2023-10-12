
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())
print(os.environ["OPENAI_API_KEY"])