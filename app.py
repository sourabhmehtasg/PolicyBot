import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings

import os

os.environ['USER_AGENT'] = 'myagent'

err_str = "Unfortunately, I was not able to answer your question, because of the following error:"

# -- App data loading
# URL processing
def process_input(urls, question):
    model_local = OllamaLLM(model="mistral")
    
    # Convert string of URLs to list
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    #split the text into chunks
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)
    
    #convert text chunks into embeddings and store in vector database
    embedding=OllamaEmbeddings(model='nomic-embed-text')

    vectorstore = Chroma.from_documents(documents=doc_splits, collection_name="rag-chroma", embedding=embedding)
    retriever = vectorstore.as_retriever()
    
    #perform the RAG 
    
    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """

    model_local = OllamaLLM(model="mistral")

    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)

    after_rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | after_rag_prompt | model_local | StrOutputParser())


    return after_rag_chain.invoke(question) 


# App UI config

# App config
st.set_page_config(
    page_title="Policy Bot",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar config
with st.sidebar:
    st.subheader("Select the policy", help="select one from below in which you are interested",  divider='rainbow')
    
    policy_number = st.radio(
        "Which policy you want to know more about today",
        [":rainbow[Policy-1]", ":rainbow[Policy-2]", ":rainbow[Policy-3]"],
        captions=[
            "Comprehensive Data Privacy Policy.",
            "Comprehensive AI Ethics Policy Document.",
            "Model Governance Policy.",
        ],
        index=None,
    )


# --- App UI

col1, col2, col3 = st.columns(3)
with col2:
    st.header('🤖  Welcome to PolicyBot')


st.subheader(" ⌨️ Please select policy topic from sidebar", help="This chatbot will answer your questions about Data & AI policy of the company",  divider='rainbow')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # st.session_state.messages.append({"role": "ai", "content": "Here are few questions to try out"})
    # st.session_state.messages.append({"role": "ai", "content": st.button("How would you introduce yourself in terms of your knowledge?")})

# Display chat messages from history on app rerun
with st.chat_message("ai"):
    st.markdown("How can I help you? To start please select the policy topic you are interested from the sidebar.")
    bt1 = st.button(":rainbow[1.> Comprehensive Data Privacy Policy]", key="bt1", disabled=True)
    bt2 = st.button(":rainbow[2.> Comprehensive AI Ethics Policy Document]", key="bt2", disabled=True)
    bt3 = st.button(":rainbow[3.> Model Governance Policy]", key="bt3", disabled=True)

# if bt1:
#     b_prompt = "How would you introduce yourself in terms of your knowledge?"

# if bt2:
#     b_prompt = "what is your educational background?"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Please select topic & ask anything about that"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # time.sleep(1)
    if prompt in ["HI", "hi", "Hi", "HELLO", "hello", "Hello"]:
        response = "Hi, this is PolicyBot, you can select the Policy by passing option number in chat to further proceed. 😄"
    else:
        try:
            if policy_number == ':rainbow[Policy-1]':
                response = process_input("https://sourabhmehtasg.github.io/PolicyBot/Policy_1", prompt)
            elif policy_number == ':rainbow[Policy-2]':
                response = process_input("https://sourabhmehtasg.github.io/PolicyBot/Policy_2", prompt)
            elif policy_number == ':rainbow[Policy-3]':
                response = process_input("https://sourabhmehtasg.github.io/PolicyBot/Policy_3", prompt)
            else:
                response = "Please select atleast one policy from sidebar to proceed further"
        except Exception as ex:
            print ("An internal exception occurred:-")
            print(ex)
            answer = "Can not undersand your question, kindly repharse and ask."
            response = answer


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(f":rainbow[PolicyBot:]")
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

