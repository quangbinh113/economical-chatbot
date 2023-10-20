# deploy ảnh html

# import streamlit as st
#
#
# def visualize(path_html):
#     # Load the HTML file
#     with open(r"path_html", "r", encoding="utf-8") as html_file:
#         html_content = html_file.read()
#
#     st.components.v1.html(html_content, height=600)


# test chỉnh giao diện FE


import streamlit as st
import openai
import requests
from requests import Response
import os
from datetime import datetime
from helper import api, help

# background thay thế: https://images.rawpixel.com/image_1000/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0yODEtYWRqLTA1Ni5qcGc.jpg

UPLOAD_API_URL = "http://127.0.0.1:8000/upload/upload_file"

page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] {{
background-image: url("https://img.freepik.com/free-photo/shimmering-gold-stars-watercolor_53876-94598.jpg?w=1380&t=st=1696407133~exp=1696407733~hmac=2198a7a11add8236045fe8c300961a810457b45523a2c24c8d4d7ea7838cbaec");
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
    # st.title("🔥Vietnamese Economical Chatbot🔥")
    st.markdown("<div style='text-align: center;'><strong style='font-size: 25px;'>🔥Vietnamese Economical "
                "Chatbot🔥</strong></div>", unsafe_allow_html=True)
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
    # st.subheader('Models and parameters')
    # st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a GPT Version', ['GPT-2', 'GPT-3.5 Turbo', 'GPT-4'],
                                          key='selected_model')

    # Choose the corresponding GPT model
    if selected_model == 'GPT-2':
        gpt_model = 'gpt-3.5-turbo'  # Use GPT-3.5 Turbo for GPT-2-like behavior
    elif selected_model == 'GPT-3.5 Turbo':
        gpt_model = 'gpt-3.5-turbo'
    else:
        gpt_model = 'text-davinci-002'  # Replace with GPT-4 model when available

    # temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('Max Length', min_value=64, max_value=4096, value=512, step=8)

    st.markdown('📖 AI Intern Hà Nội!')

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = gpt_api

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/d/d9/Neurond.png",
    width=None,  # Manually Adjust the width of the image as per requirement
)

# Store chat messages
if "documents" not in st.session_state.keys():
    st.session_state.documents = None
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


def save_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# def click_upload_file():
#     uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "txt", "json", "pdf", "md", "rar", "zip"])
#     if uploaded_file is not None:
#         st.sidebar.write("You've uploaded a file!")


###
backend_endpoint = "http://127.0.0.1:8000/"
api_get_model_file = f"{backend_endpoint}upload/read_file?file_name="


# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.sidebar.selectbox('Select a file', filenames)
#     # return os.path.join(folder_path, selected_filename)
#     return os.path.basename(selected_filename)


# file_in_folder = st.sidebar.button("Select file in folder")
# if "file_in_folder_state" not in st.session_state:
#     st.session_state.file_in_folder_state = False

# if file_in_folder or st.session_state.file_in_folder_state:
#     st.session_state.file_in_folder_state = True

#     folder_path = 'file_upload'
#     selected_filename = file_selector(folder_path)
#     # print(selected_filename)
#     st.sidebar.write('You selected `%s`' % selected_filename)
#     documents_read_file = api.read_file(api_get_model_file + selected_filename)
#     print(documents_read_file)
# print(documents_read_file)
# Button to clear chat history
# st.sidebar.button('Chat Your Own Data', on_click=click_upload_file)

# button upload file



uploadbtn = st.sidebar.button("Chat Your Own Data")

if "uploadbtn_state" not in st.session_state:
    st.session_state.uploadbtn_state = False

if uploadbtn or st.session_state.uploadbtn_state:
    st.session_state.uploadbtn_state = True

    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "txt", "json", "pdf", "md", "rar", "zip"])

    if uploaded_file is not None:
        st.sidebar.write(f"Uploaded file: {uploaded_file.name}")
        st.session_state.documents = uploaded_file.name
    else:
        st.sidebar.write("No file uploaded yet.")
        st.session_state.documents = None

    if uploaded_file is not None:
        # st.sidebar.write("Uploading file to API...")
        document_data = api.upload_file_to_api(UPLOAD_API_URL, uploaded_file)
        

        # if document_data:
        #     print(document_data['filename'])
        # else:
        #     print(document_data)


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.button('Save Chat History', on_click=save_chat_history)

# SAVE_API_URL = "http://127.0.0.1:8000/ai/history/automaticQA"

# api_check_thread = "http://127.0.0.1:8000/ai/thread/get_thread"


# def get_thread(url):
#     respone = api.check_thread(url)
#     # print(respone)
#     return respone


# list_thread = get_thread(api_check_thread)

# for item in list_thread:
#     if "topic" not in item:
#         api_create_thread = "http://127.0.0.1:8000/ai/thread/automatic"
#         api.create_thread(api_create_thread)

if prompt := st.chat_input("What is up?"):
    start_time = datetime.now()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = '' 
        res = requests.post("http://127.0.0.1:8000/ai/get_response", json = {"question": prompt,"documents":st.session_state.documents},stream=True)
        for response in res:
            full_response += response.decode('utf8')
            message_placeholder.markdown(full_response + "▌")
        end_time = datetime.now()
        response_time = end_time - start_time
        st.markdown(f"🕒 Bot response time: {response_time.total_seconds()} seconds")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # full_response = "......test......"
    # html_path = r"C:\Users\Admin\Desktop\Project\Inter_AI_2023\prj-economical-chatbot\visualize_html" \
    #             r"\stock_visualization.html"

    # api.save_data_to_db(question=prompt, full_response=full_response, path_html=html_path)