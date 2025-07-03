import os

#Paso 1: Elección de la Técnica de DocumentLoader
from langchain_community. document_loaders import PyPDFLoader

#Paso 2: Elección de Técnica de Splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter #Mi técnica de Splitting

#Paso 3: Elección del Modelo de Word Embedding
from langchain_openai import OpenAIEmbeddings

#Paso 4: Elección de BaSE DE datos Vectorial
from langchain_chroma import Chroma

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    #----------------------------- Paso 1: Documment Loader---------------------------------------------
    path = "Base_de_Conocimientos/SOBRE_DATAPATH.pdf" #HAY QUE AGREGAR LUEGO ESE DNI
    loader = PyPDFLoader(path)
    documentos = loader.load()


    #-------------------------------- Paso 2: Chunking -------------------------------------------------
    text_splitter =  RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
    )
    chunks = text_splitter.split_documents(
        documents=documentos
    )


    #---------- Paso 3: Embeddings - Convertir los documentos de mi PDF a Embeddings --------------------
    embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')


    #----------------- Paso 4: VectorStore - Crear la Base de Datos Vectorial ---------------------------
    directorio_de_vectores = 'chroma_vectorstore_RAG'

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model, #ada de OpenAI
        persist_directory=directorio_de_vectores #Carpeta que contiene mis vectores
    )