from langchain.prompts import ChatPromptTemplate
import asyncio
template_3 = """\
Từ đoạn văn bản, hãy trích suất những thông tin sau:

Mã cổ phiếu: Mã cổ phiếu, chứng khoán đã được đề cập tới trong đoạn văn bản\
Câu trả lời: Nếu như tìm thấy thì giá trị là mã cổ phiếu đó, nếu không tìm thấy thì giá trị là None 

Thời gian bắt đầu: Trích xuất thông tin là mốc thời gian bắt đầu giao dịch. Chuyển đổi về định dạng timestamp\
Câu trả lời: Nếu như tìm thấy thì là mốc thời gian cụ thể. Nếu như không tìm thấy thông tin thì để giá trị là None

Thời gian kết thúc: Trích xuất thông tin là mốc thời gian kết thúc giao dịch. Chuyển đổi về định dạng timestamp\
Câu trả lời: Nếu như tìm thấy thì là mốc thời gian cụ thể. Nếu như không tìm thấy thông tin thì để giá trị là None

Khoảng thời gian: Là khoảng thời gian cần trích xuất so với mốc thời gian dao dịch\
Câu trả lời: Nếu như tìm thấy thì là khoảng thời gian đã đề cập ở trên. Nếu như không tìm thấy thì để giá trị là None

Định dạng đầu ra là JSON với những khóa sau:
stock_code
start_date
end_date
time_range

Đoạn văn bản: {text}
"""
QA_CHAIN_PROMPT_3 = ChatPromptTemplate.from_template(template_3)

from src.model.model import HandleQA
from config.config import config
import asyncio

chat = HandleQA(config)

# async def test():
chat.reset_callback()

generator = chat.ask_gpt('Mã chứng khoán VHM từ 8 giờ đến 18 giờ chiều ngày 11/10/2023',crawl_data=[])
# print(type(generator))
# asyncio.run(generator)
async def test():
    async for item in generator:
        print(item)
asyncio.run(test())