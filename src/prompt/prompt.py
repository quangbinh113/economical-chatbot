from langchain.prompts import ChatPromptTemplate
template_1 = """
Bạn là chuyên viên tư vấn tài chính. Hãy tư vấn cho khách hàng bằng những thông tin ở phần nội dung để trả lời câu hỏi ở phía cuối. Thông tin phải là gần đây nhất. Đưa ra câu trả lời xác thực. Luôn trả lời bằng tiếng Việt. Kết thúc câu trả lời bằng "\nCảm ơn vì đã hỏi". 
Nội dung: {context}
Câu hỏi: {question}
Câu trả lời bằng Tiếng Việt:"""

QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(template_1)