from time import sleep

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

from tools_3_completo import DataPathTools


class DataPath:
    def __init__(self):
        self.llm = ChatOpenAI(model= 'gpt-4o-mini') # no olvides adicionar tu api_key en el .env
        self.tool = DataPathTools()


    def crear_agente(self):
        tools = [
            Tool(name="bajar_video_youtube", func=DataPathTools.bajar_video_de_youtube, description="Descarga un video de YouTube y devuelve la ruta del archivo descargado para que sea usado por otra tool."),
            Tool(name="extraer_audio_video", func=DataPathTools.extraer_audio, description="Extrae el audio de un archivo MP4 ubicado en una carpeta local, que podría haber sido extraído del youtube por otra Tool."),
            #Tool(name="describir_imagen", func=DataPathTools.describe_imagen, description="Analiza la imagen en image_path y devuelve una descripción detallada. Si la imagen contiene texto, será transcrito."),
            Tool(name="transcribir_audio", func=DataPathTools.transcribir_audio, description="Transcribe un archivo de audio guardado en audio_path a texto utilizando reconocimiento de voz."),
            Tool(name="guardar_nota", func=DataPathTools.guardar_nota, description="Guarda el texto en un archivo de texto dentro del directorio de notas y además devuelve ese texto o nota resumen al usuario."),
            DataPathTools.enviar_correo,  # Ya es un StructuredTool
            DataPathTools.registrar_google_sheet,  # Ya es un StructuredTool
            Tool(name="consultar_DataPath",func=DataPathTools.consultar_DataPath, description="Usa el sistema RAG para responder consultas sobre DataPath."),
            Tool(name="lectura_promocion", func=DataPathTools.lectura_promocion, description="Usa tablas del sistema CRM para responder consultas sobre precios de los cursos en Datapath."),
            #DataPathTools.lectura_all_promocion
            #Tool(name="lectura_all_promocion", func=DataPathTools.lectura_all_promocion, description="Usa tablas del sistema CRM para responder consultas sobre precios de los cursos en Datapath.")
        ]

        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Eres un asistente amigable llamado Dr. Chelito.

                    Tienes cuatro roles principales:

                    1 **Responder preguntas sobre DataPath:**  
                        - Usa la herramienta 'consultar_DataPath' para responder cualquier consulta sobre cursos, programas y servicios.  
                        - Continúa respondiendo preguntas mientras el usuario siga consultando sobre DataPath.  
                    
                    2 **Responder preguntas sobre Promociones:**  
                        - usa la herramienta 'lectura_promocion' para consultar las promociones sobre un programa de interes.
                        - Solo después de obtener estos datos, usa los campos (**precio_regular**, **promo_julio**, **detalles_promocion**, **vigencia**) para armar la información de la promocion.  
                        - Una ves mostrada la promocion ofrece al ususario comunicarse con un asesor.

                    3 **Conectar al usuario con un asesor:**  
                        - Si el usuario expresa interés en comunicarse con un asesor o recibir información personalizada, solicita su **nombre completo**, **correo electrónico**, **programa de interés** y usa el campo  **promo_julio** para completar el registro.  
                        - usa 'registrar_google_sheet', para verificar el programa de interes y promocion de interes.
                        - Solo después de obtener estos datos, usa 'registrar_google_sheet' pasando los argumentos  (**nombre**, **correo**, **programa**, **promo_julio**) para registrar la información. 
                        - Es decir asegúrate de darle el formato correspondiente para la entrada de la función "registrar_google_sheet".
                        - Luego, usa 'a_enviar_correo' para notificar al usuario que un asesor se pondrá en contacto.  

                    4 **Procesar contenido multimedia:**  
                        - Si el usuario proporciona un enlace de YouTube o un archivo multimedia (MP4, MP3, OGG):  
                            - Usa 'bajar_video_youtube' para descargar el video (si es un enlace de YouTube).  
                            - Usa 'extraer_audio_video' para extraer el audio de videos MP4/YouTube.  
                            - Usa 'transcribir_audio' para convertir el audio en texto.  
                            - Finalmente, usa 'guardar_nota' para crear y guardar una nota basada en la transcripción.  
                            - Entrega el resultado de la nota creada y guardada en español, aquella que obtuviste basada en la transcripción.  

                    ⚡️ **Reglas Importantes:**  
                    - No pidas datos personales si el usuario solo hace preguntas generales sobre DataPath o usa las funciones multimedia.  
                    - Detecta claramente la intención del usuario: si está preguntando, quiere contacto o procesar contenido.  
                    - Si el mensaje es ambiguo, pide más detalles.  
                    - Responde siempre en español y usa emojis para mantener un tono amigable. 😊  
                    """
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )


        agent = create_tool_calling_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )
        return agent, tools

    def procesar_mensaje(self, msg, agente, tools, history_messages=None):
        

        """Procesa el mensaje recibido vía WhatsApp y llama a la herramienta correcta."""
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agente,
            tools=tools,
            verbose=True,
        )


        # Prompt mejorado
        executor_prompt = {
            "input": (
                f"Analiza el siguiente mensaje y decide qué acción tomar:\n\n"

                f"1 **Si es una consulta general sobre DataPath:**\n"
                f"- Usa 'consultar_DataPath' para responder.\n"
                f"- Continúa respondiendo mientras el usuario siga haciendo preguntas.\n\n"

                f"2 **Si es una consulta sobre las promociones:**\n"
                f"- solicita el nombre del **programa de interés**.\n"
                f"- usa 'lectura_promocion' con el campo **curso** para responder. \n" 
                f"- Para formular tu respuesta utiliza información obtenida **precio_regular**, **promo_julio**, **detalles_promocion**, **vigencia**.\n"
                f"- Despues de mostrar la promocion conecta al ususario con un asesor.\n\n"

                f"3 **Si el usuario quiere hablar con un asesor o recibir información personalizada:**\n"
                f"- Solicita el **nombre completo**, **correo electrónico**, **programa de interés**\n"
                f"- Solo después de obtener estos datos completos:\n"
                f"  - Solicita al ususario que los campos solicitados esten completos y usa el campo *promo_julio** \n"
                f"  - Si el ususario confirmo con Si, Usa 'registrar_google_sheet' para registrar al usuario.\n"
                f"  - Usa 'a_enviar_correo' para enviar una notificación.\n\n"

                f"4 **Si el mensaje contiene contenido multimedia (YouTube, MP4, MP3, OGG):**\n"
                f"- Si es un enlace de YouTube:\n"
                f"  - Usa 'bajar_video_youtube' para descargar el video.\n"
                f"  - Luego, usa 'extraer_audio_video' para extraer el audio.\n"
                f"  - Usa 'transcribir_audio' para transcribir el audio.\n"
                f"  - Finalmente, usa 'guardar_nota' para crear una nota.\n\n"

                f"- Si el usuario envía un archivo MP4:\n"
                f"  - Extrae el audio usando 'extraer_audio_video'.\n"
                f"  - Transcribe el audio con 'transcribir_audio'.\n"
                f"  - Guarda la nota usando 'guardar_nota'.\n\n"

                f"- Si el usuario envía un archivo MP3/OGG:\n"
                f"  - Transcribe directamente el audio usando 'transcribir_audio'.\n"
                f"  - Guarda la nota usando 'guardar_nota'.\n\n"

                f"**Reglas Generales:**\n"
                f"- No pidas datos personales a menos que el usuario exprese interés en comunicarse con un asesor.\n"
                f"- Si el mensaje es ambiguo, pide más detalles.\n"
                f"- Responde siempre en español, manteniendo un tono amigable y usando emojis. 😊\n\n"

                f"💬 **Mensaje del usuario:**\n{msg}"
            )
        }


        # Incluir el historial de mensajes en el contexto si está disponible
        if history_messages:
            executor_prompt["history_messages"] = history_messages
        
        resultado = agent_executor.invoke(executor_prompt)


        return resultado