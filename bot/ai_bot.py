import os

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()


class AIBot:

    def __init__(self):
        self.__chat = ChatOpenAI(model= 'gpt-4o-mini')
        self.__retriever = self.__build_retriever()

    def __build_retriever(self):
        persist_directory = 'RAG/chroma_vectorstore_RAG'
        embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model,
        )
        return vector_store.as_retriever( #El retrieve busca los datos correspondientes en nuestro VectorData Base
            search_kwargs={'k': 30}, #Busco hasta máximo 30 resultados de Chunks
        )

    def __build_messages(self, history_messages, question):
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get('fromMe') else AIMessage
            messages.append(message_class(content=message.get('body')))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = '''
        Responde las preguntas de los usuarios con base en el siguiente contexto.
        Tu nombre es Dr. Chelito, antes de cualquier interaccion siempre presentate amablemente.
        Eres un asistente especializado en resolver dudas sobre la empresa de educación online DataPath.
        Resuelve las dudas de los posibles alumnos que se pongan en contacto.
        Responde de forma natural, agradable y respetuosa. Sé objetivo en las respuestas, con información clara y directa.
        Enfócate en ser natural y humano, como un diálogo común entre dos personas.
        Ten en cuenta también el historial de mensajes de la conversación con el usuario.
        Responde siempre en español.
        Usa emojis cuando fuera posible.

        <context>
        {context}
        </context>
        '''

        docs = self.__retriever.invoke(question) #Estoy buscando en mi banco de datos.

        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    SYSTEM_TEMPLATE,
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)
        response = document_chain.invoke(
            {
                'context': docs,
                'messages': self.__build_messages(history_messages, question),
            }
        )
        return response