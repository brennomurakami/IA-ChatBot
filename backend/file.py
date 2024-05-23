from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()

def limpar_texto(texto):
    return " ".join(texto.split())
def process_pdf(files):
    print(files)
    reader = PdfReader(files)
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len
    )

    texts = text_splitter.split_text(raw_text)
    return texts

def criar_indices_faiss(files):
    texts = process_pdf(files)
    # Cria o índice FAISS a partir dos textos e dos embeddings
    vector_store = FAISS.from_texts(texts, embeddings)
    # Salva o índice em um arquivo
    vector_store.save_local("faiss_index")
    return vector_store

def carregar_indices_faiss():
    # Carrega o índice FAISS a partir do arquivo com desserialização perigosa permitida
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vector_store

def adicionar_texto_ao_indice(vector_store, files):
    texts = process_pdf(files)
    # Adiciona novos textos ao índice existente
    metadatas = [{} for _ in texts] 
    vector_store.add_texts(texts, metadatas=metadatas)
    # Salva o índice atualizado em um arquivo
    vector_store.save_local("faiss_index")

def verificar_e_atualizar_indice(files):
    if os.path.exists("faiss_index"):
        vector_store = carregar_indices_faiss()
        adicionar_texto_ao_indice(vector_store, files)
    else:
        vector_store = criar_indices_faiss(files)
    return vector_store

def procurar_similaridade(query):
    query.split('VECTOR121:')
    query_embedding = embeddings.embed_query(query)
    # Verificar e atualizar o índice
    vector_store = carregar_indices_faiss()
    # Realiza a busca de similaridade
    query_embedding_str = "".join(str(query_embedding))
    resultados = vector_store.similarity_search(query=query_embedding_str, k=2)
    textos_resultados = [limpar_texto(doc.page_content) for doc in resultados]
    textos_resultados = ' '.join(textos_resultados)
    print("RESULTADOS: ", textos_resultados)
    return textos_resultados