import streamlit as st
import openai
import os
import api
from style import page_bg_img
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

UPLOAD_API_URL=os.getenv("UPLOAD_API_URL")
SAVE_API_URL =os.getenv("SAVE_API_URL")
api_check_thread = os.getenv("api_check_thread")
folder_path = os.getenv("folder_path")
html_path = os.getenv("html_path")
backend_endpoint = os.getenv("backend_endpoint")
print('backend_endpoint: ', backend_endpoint)


# TODO: background thay thế: https://images.rawpixel.com/image_1000/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0yODEtYWRqLTA1Ni5qcGc.jpg
# App title
st.markdown(page_bg_img, unsafe_allow_html=True)
# st.set_page_config(page_title="💬Neurond AI Chatbot")

# Sidebar
with st.sidebar:
    # st.title("🔥Vietnamese Economical Chatbot🔥")
    st.markdown("<div style='text-align: center;'><strong style='font-size: 25px;'>🔥Vietnamese Economical "
                "Chatbot</strong></div>", unsafe_allow_html=True)
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
    selected_model = st.sidebar.selectbox('Choose a GPT Version', ['GPT-2', 'GPT-3.5 Turbo', 'GPT-4'],
                                          key='selected_model')

    # Choose the corresponding GPT model
    if selected_model == 'GPT-3.5':
        gpt_model = 'gpt-3.5-turbo'
    elif selected_model == 'GPT-3.5 Turbo 0613':
        gpt_model = 'gpt-3.5-turbo-0613'
    else:
        gpt_model = 'text-davinci-002'  # Replace with GPT-4 model when available
    st.markdown('📖 AI Intern Hà Nội!')

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = gpt_api

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/d/d9/Neurond.png",
    width=None
)

# Store chat messages
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


api_get_model_file = f"{backend_endpoint}/upload/read_file?file_name="


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    # return os.path.join(folder_path, selected_filename)
    return os.path.basename(selected_filename)


file_in_folder = st.sidebar.button("Select file in folder")
if "file_in_folder_state" not in st.session_state:
    st.session_state.file_in_folder_state = False

if file_in_folder or st.session_state.file_in_folder_state:
    st.session_state.file_in_folder_state = True
    selected_filename = file_selector(folder_path)
    st.sidebar.write('You selected `%s`' % selected_filename)
    documents_read_file = api.read_file(api_get_model_file + selected_filename)

# button upload file
uploadbtn = st.sidebar.button("Chat Your Own Data")

if "uploadbtn_state" not in st.session_state:
    st.session_state.uploadbtn_state = False

if uploadbtn or st.session_state.uploadbtn_state:
    st.session_state.uploadbtn_state = True

    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "txt", "json", "pdf", "md", "rar", "zip"])
    if uploaded_file is not None:
        st.sidebar.write("Uploading file to API...")
        document_data = api.upload_file_to_api(UPLOAD_API_URL, uploaded_file)

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.button('Save Chat History', on_click=save_chat_history)


# Function for generating GPT response
def generate_gpt_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only " \
                      "respond once as 'Assistant'."
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

def get_thread(url):
    respone = api.check_thread(url)
    # print(respone)
    return respone


list_thread = get_thread(api_check_thread)

if not list_thread:
    list_thread = []

for item in list_thread:
    if "topic" not in item:
        api_create_thread = "http://127.0.0.1:8000/ai/thread/automatic"
        api.create_thread(api_create_thread)

if prompt := st.chat_input("What is up?"):
    start_time = datetime.now()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response_url = "{}/ai/get_response".format(backend_endpoint)
        # print('response_url: ', response_url)
    
        # full_response += api.get_data_from_api(response_url,
        #                                        {"question": prompt})
        
        print('full_response: ', api.get_data_from_api(response_url,
                                               {"question": prompt}))
        # Tính thời gian trả lời và in ra màn hình
        end_time = datetime.now()
        response_time = end_time - start_time
        st.markdown(f"🕒 Bot response time: {response_time.total_seconds()} seconds")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # full_response = "......test......"

    # api.save_data_to_db(question=prompt, full_response=full_response, path_html=html_path)