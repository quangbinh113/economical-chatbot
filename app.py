import streamlit as st
import openai
import os
from datetime import datetime
from helper import api
import requests
page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] {{
background-image: url("https://img.freepik.com/free-photo/beige-nude-pink-background-text-space_53876-108333.jpg?w=1380&t=st=1695281200~exp=1695281800~hmac=0dee288b519f53c699ed2c9af1bb2a45a776567b6f8ff2f1eba4c37f3b5c1654");
background-size: cover;
}}

[data-testid="stSidebar"] {{
background-image: url("https://i.pinimg.com/564x/96/d4/a5/96d4a541a4cdeaeac344d82dc4b01ceb.jpg");
background-position: center; 
}}

[data-baseweb="textarea"]{{
border-color: transparent
}}

[class = "stChatFloatingInputContainer css-90vs21 e1d2x3se2"] {{
border-radius: 20px;
margin-bottom: 5px;
height: 100px;
background-color: rgb(0, 0, 0, 0);
}}

[class="css-s1k4sy e1d2x3se4"] {{
align-self:center;
margin-bottom: 20px
}}

</style>
"""
# App title
st.markdown(page_bg_img, unsafe_allow_html=True)
# st.set_page_config(page_title="💬Neurond AI Chatbot")

# Sidebar
with st.sidebar:
    st.title("🔥 Chatbot with LangChain 🔥")
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        gpt_api = st.secrets['OPENAI_API_KEY']
    else:
        gpt_api = st.text_input('Enter GPT API-Key:', type='password')
        if not (gpt_api.startswith('sk-') and len(gpt_api) == 76):
            st.warning('Please enter a valid API key!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    # Model and parameters selection
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a GPT Version', ['GPT-2', 'GPT-3.5 Turbo', 'GPT-4'],
                                          key='selected_model')

    # Choose the corresponding GPT model
    if selected_model == 'GPT-2':
        gpt_model = 'gpt-3.5-turbo'  # Use GPT-3.5 Turbo for GPT-2-like behavior
    elif selected_model == 'GPT-3.5 Turbo':
        gpt_model = 'gpt-3.5-turbo'
    else:
        gpt_model = 'text-davinci-002'  # Replace with GPT-4 model when available

    temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Max Length', min_value=64, max_value=4096, value=512, step=8)

    st.markdown('📖 AI Intern Hà Nội!')

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = gpt_api

# Thêm ảnh logo công ty vào đầu trang
# st.image(r'C:\Users\Admin\Desktop\Project\python-crawler\neurond_chatbot.jpg', use_column_width=True)
# st.image(r'C:\Users\Admin\Desktop\Project\python-crawler\neurond_chatbot.jpg', width=300)
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/d/d9/Neurond.png",
    width=None,  # Manually Adjust the width of the image as per requirement
)

# Store chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         user_input = message["content"]
#         st.markdown(f'👤 You: {user_input}')
#     else:
#         assistant_response = message["content"]
#         st.markdown(f'🤖 Bot: {assistant_response}')

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# Button to clear chat history
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating GPT response
def generate_gpt_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    # Use OpenAI API directly with openai.ChatCompletion
    openai.api_key = gpt_api
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You do not respond as 'User' or pretend to be 'User'."},
            {"role": "system", "content": "You only respond once as 'Assistant'."},
            {"role": "user", "content": f"{prompt_input}"},
        ],
    )

    return response['choices'][0]['message']['content']


# User input field
# if prompt := st.text_input("👤 You:"):
#     st.session_state.messages.append({"role": "user", "content": prompt})

# # Generate a new response when the user inputs a message
# if prompt:
#     user_input = st.session_state.messages[-1]["content"]
#     st.markdown(f'👤 You: {user_input}')
#     response = generate_gpt_response(user_input)
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     st.markdown(f'🤖 Bot: {response}')

if prompt := st.chat_input("What is up?"):
    # print("????????")
    # print(prompt)
    start_time = datetime.now()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # for response in openai.ChatCompletion.create(
        #         model=gpt_model,
        #         messages=[
        #             {"role": m["role"], "content": m["content"]}
        #             for m in st.session_state.messages
        #         ],
        #         stream=True,
        # ):
        #     full_response += response.choices[0].delta.get("content", "")
        #     message_placeholder.markdown(full_response + "▌")

        # message_placeholder.markdown(full_response + "▌")
        full_response += api.get_data_from_api("http://127.0.0.1:8000/ai/get_response", {"question": prompt}).cau_tra_loi
        # Tính thời gian trả lời và in ra màn hình
        end_time = datetime.now()
        response_time = end_time - start_time
        st.markdown(f"🕒 Bot response time: {response_time.total_seconds()} seconds")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
