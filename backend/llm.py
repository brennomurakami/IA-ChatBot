from backend.instruction import instruction
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-multilingual-embedding-002"
)

safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0,
    safety_settings=safety_settings,
    cache=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instruction),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

set_llm_cache(InMemoryCache())

chain = prompt | llm


new_vectorstore = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)

client_vector = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=new_vectorstore.as_retriever()
)
