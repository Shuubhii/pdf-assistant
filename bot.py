

#Commented out IPython magic to ensure Python compatibility.

#%%writefile app.py
import streamlit as st
import time
import os
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
#from detectron2.config import get_cfg

os.environ["OPENAI_API_KEY"] = st.secrets["API-KEY"]


def pdf_model(pdf_path):
#  cfg = get_cfg()
#  cfg.MODEL.DEVICE = 'cpu'
  loaders = [UnstructuredPDFLoader(pdf_path)]
  index = VectorstoreIndexCreator().from_loaders(loaders)
  return index

text_folder = '/content/48lawsofpower.pdf'
#tindex=pdf_model(text_folder)



st.sidebar.title("PDF-Assistant")
st.sidebar.write("# Welcome to the time machine demo 👋")

st.sidebar.write("""
            Please go ahead and:
             - Upoad some data
             - Start interacting
             """)


 # upload file
file = st.sidebar.file_uploader("Upload your PDF to start Interacting", type="pdf")

def save_temp_file(uploaded_file):
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    return temp_file_path
path=""
index=""
if file:
  st.sidebar.success(f"File uploaded: {file.name}")
  path=save_temp_file(file)
  index=pdf_model(path)

#if st.button("Click for assistance"):
  # Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
#prompt=
if prompt:=st.chat_input("Ask questions?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      full_response = ""
      assistant_response=index.query(str(prompt))

  # Simulate stream of response with milliseconds delay
      for chunk in assistant_response.split():
          full_response += chunk + " "
          time.sleep(0.05)
      # Add a blinking cursor to simulate typing
          message_placeholder.markdown(full_response + "▌")
      message_placeholder.markdown(full_response)

# Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})




#to get the password which is to be used in the localtunnel to access streamlit
# ! wget -q -O - https://loca.lt/mytunnelpassword

# !streamlit run app.py &>/content/logs.txt &
# !npx localtunnel --port 8501
