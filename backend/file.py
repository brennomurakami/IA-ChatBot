from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
def process_file(file_path):
    if file_path.endswith('.pdf'):
        return process_pdf(file_path)
    elif file_path.endswith('.csv'):
        return process_csv(file_path)
    elif file_path.endswith('.txt'):
        return process_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

def process_csv(file_path):
    print("PROCESSANDO CSV")
    df = pd.read_csv(file_path)
    raw_text = df.to_string(index=False)
    return split_text(raw_text)

def process_txt(file_path):
    print("PROCESSANDO TXT")
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()
    return split_text(raw_text)

def split_text(raw_text):
    # Aqui você pode usar a lógica de divisão de texto que você precisa
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_text(raw_text)
    return texts

def process_pdf(file_path):
    print("PROCESSANDO PDF")
    reader = PdfReader(file_path)
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    texts = text_splitter.split_text(raw_text)
    return texts

def criar_indices_faiss(file_path):
    texts = process_file(file_path)
    # Cria o índice FAISS a partir dos textos e dos embeddings
    vector_store = FAISS.from_texts(texts, embeddings)
    # Salva o índice em um arquivo
    vector_store.save_local("backend/faiss_index")
    return vector_store

def carregar_indices_faiss():
    # Carrega o índice FAISS a partir do arquivo com desserialização perigosa permitida
    vector_store = FAISS.load_local("backend/faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vector_store

def adicionar_texto_ao_indice(file_path, vector_store):
    texts = process_file(file_path)
    # Adiciona novos textos ao índice existente
    metadatas = [{} for _ in texts]  # Cria uma lista de dicionários vazios
    vector_store.add_texts(texts, embeddings, metadatas=metadatas)
    # Salva o índice atualizado em um arquivo
    vector_store.save_local("backend/faiss_index")

def verificar_e_atualizar_indice(file_path):
    if os.path.exists("backend/faiss_index"):
        vector_store = carregar_indices_faiss()
        adicionar_texto_ao_indice(file_path, vector_store)
    else:
        vector_store = criar_indices_faiss(file_path)
    return vector_store

def procurar_similaridade(query):
    query = query.split("VECTOR121:")
    query_embedding = embeddings.embed_query(query)
    # Verificar e atualizar o índice
    vector_store = carregar_indices_faiss()
    # Realiza a busca de similaridade
    query_embedding_str = "".join(str(query_embedding))
    resultados = vector_store.similarity_search(query_embedding_str, k=2)
    return resultados
