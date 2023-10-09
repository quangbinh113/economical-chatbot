from langchain.prompts import ChatPromptTemplate
template_1 = """Bạn là chuyên viên tư vấn tài chính. Hãy tư vấn cho khách hàng bằng những thông tin ở phần nội dung để trả lời câu hỏi ở phía cuối. Thông tin phải là gần đây nhất. Đưa ra câu trả lời kèm theo tóm tắt. Luôn trả lời bằng tiếng Việt.
Nội dung: {context}
Câu hỏi: {question}
Câu trả lời bằng Tiếng Việt kèm theo ít nhất 5 nội dung chính:"""
QA_CHAIN_PROMPT_1 = ChatPromptTemplate.from_template(template_1)


template_2 ="""Bạn là chuyên viên tư vấn tài chính. Hãy trả lời câu hỏi sau đây. Thông tin phải là gần đây nhất. Đưa ra câu trả lời xác thực kèm theo tóm tắt. Luôn trả lời bằng tiếng Việt.
Câu hỏi: {question}
Câu trả lời bằng Tiếng Việt kèm theo ít nhất 5 nội dung chính:"""
QA_CHAIN_PROMPT_2 = ChatPromptTemplate.from_template(template_2)

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


# template_4 ="""Bạn là chuyên viên tư vấn tài chính. Hãy trả lời câu hỏi sau đây. Thông tin phải là gần đây nhất. Đưa ra câu trả lời xác thực kèm theo tóm tắt. Luôn trả lời bằng tiếng Việt.
# Nội dung: {context}
# Câu hỏi: {question}
# Câu trả lời bằng Tiếng Việt kèm theo ít nhất 5 nội dung chính:"""
# QA_CHAIN_PROMPT_4 = ChatPromptTemplate.from_template(template_4)

