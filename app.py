"""
main module PDF_READER_CHATBOT
"""
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import CSS, BOT_TEMPLATE, USER_TEMPLATE
from langchain.llms import HuggingFaceHub
def get_pdf_text(pdf_docs)-> str:
    """
    get_pdf_text module read pdf document page by page.

    Parameters
    ----------
    pdf_docs
        pdf document.
    
    Return
    ------
    text: str
        pdf document text.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
def get_text_chunks(text: str)-> str:
    """
    get_text_chunks method take chunks of document text.

    Parameters
    ----------
    text: str
        pdf document text data.
    
    Return
    ------
    chunks: str
        piece of the pdf document.
    """
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks
def get_vectorstore(text_chunks: str):
    """
    get_vectorstore create the vector of the chunk of data.

    Parameters
    ----------
    text_chunks: str
        piece of the pdf document.
    
    Return
    ------
    vectorstore: vector
        vector of text chunk.
    """
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore
def get_conversation_chain(vectorstore):
    """
    get_conversation_chain read vectorstore and create the conversation chain.

    Parameters
    ----------
    vectorstore: vector
        vector of text chunk.
    
    Return
    ------
    conversation_chain
        return conversation chain.
    """
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", 
                         model_kwargs={"temperature":0.5,
                                       "max_length":512})
    memory = ConversationBufferMemory(
        memory_key = 'chat_history',
        return_messages = True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
        )
    return conversation_chain
def handle_userinput(user_question: str)-> None:
    """
    handle_userinput take questions and write the answer apeending
    with chat history.

    Parameters
    ----------
    user_question: str
        question asked by the user.
    
    Return
    ------
    None
    """
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(USER_TEMPLATE.replace(
                "{{MSG}}", message.content),
                unsafe_allow_html=True)
        else:
            st.write(BOT_TEMPLATE.replace(
                "{{MSG}}", message.content),
                unsafe_allow_html=True)
def main():
    """
    mian method execute all methods.

    Parameters
    ----------
    None

    Return
    ------
    None 
    """
    load_dotenv()
    st.set_page_config(page_title = "Question Answer With PDF",
                       page_icon = ":books:")
    st.write(CSS, unsafe_allow_html = True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("Question Answer With PDF :books:")
    user_question = st.text_input("Ask a question about your PDF file")
    if user_question:
        handle_userinput(user_question)
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload PDFs here", accept_multiple_files = True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
if __name__ == '__main__':
    main()
