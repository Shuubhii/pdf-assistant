import streamlit as st
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
import time
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = st.secrets["API-KEY"]


def pdf_model(pdfreader):
  raw_text = ''
  for i, page in enumerate(pdfreader.pages):
      content = page.extract_text()
      if content:
          raw_text += content

  text_splitter = CharacterTextSplitter(
                  separator = "\n",
                  chunk_size = 800,
                  chunk_overlap  = 200,
                  length_function = len,
                  )
  texts = text_splitter.split_text(raw_text) 

  embeddings = OpenAIEmbeddings()  

  document_search = FAISS.from_texts(texts, embeddings)  

  chain = load_qa_chain(OpenAI(), chain_type="stuff") 
  return chain,document_search


st.sidebar.title("PDF-Assistant")
st.sidebar.write("# :blue[Welcome to the demo] 👋")

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
      
if file:
  st.sidebar.success(f"File uploaded: {file.name}")
  path=save_temp_file(file)
  pdfreader=PdfReader(path)
  c,d=pdf_model(pdfreader)

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
      docs = d.similarity_search(str(prompt))
      assistant_response=c.run(input_documents=docs, question=str(prompt))
      

  # Simulate stream of response with milliseconds delay
      for chunk in assistant_response.split():
          full_response += chunk + " "
          time.sleep(0.05)
      # Add a blinking cursor to simulate typing
          message_placeholder.markdown(full_response + "▌")
      message_placeholder.markdown(full_response)

# Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
