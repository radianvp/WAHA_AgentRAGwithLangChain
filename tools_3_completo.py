from langchain.tools import tool
from langchain.tools import StructuredTool

from utils.download_youtube_yt_dlp import YoutubeDownloader
from utils.audio import Audio
from utils.crea_partes_notas import Notes
from utils.lectura_promocion import GetPromotions

from utils.envio_correo import EnvioCorreo
from utils.registro_google_sheet import RegistroGoogleSheet

from bot.ai_bot import AIBot


#from utils.lectura_tablas import Lectura_tablas

class DataPathTools:
    #============================================================================
    @tool
    def bajar_video_de_youtube(link: str) -> str:
        """Descarga un video desde un enlace de YouTube y devuelve la ruta del archivo descargado."""
        video_path = YoutubeDownloader().bajar_video(link)
        return video_path
    
    @tool
    def extraer_audio(video_path):
        """Extrae el audio de un video y lo guarda en formato WAV."""
        audio_path = Audio.extraer(video_path)
        return audio_path
    
    @tool
    def transcribir_audio(audio_path: str) -> str:
        """Transcribe un archivo de audio guardado en audio_path a texto."""
        transcripcion_path = Audio.transcribir(audio_path)
        return transcripcion_path
    
    @tool
    def guardar_nota(transcripcion_path):
        """Guarda el texto final en un archivo de texto dentro del directorio _notas y además devuelve los resumenes al usuario."""
        notas = Notes.guardar_nota(transcripcion_path)
        return notas
    #==========================================================================

    @staticmethod
    def enviar_correo_func(nombre_lead: str, correo_lead: str, mensaje_para_lead: str):
        """Envía un correo necesitando solo el nombre del interesado, el correo del interesado y un mensaje para el interesado que va a depender del programa en el cuál él tenga el interés."""
        envio = EnvioCorreo()
        envio.enviar_correo(nombre_lead, correo_lead, mensaje_para_lead)
    
    enviar_correo = StructuredTool.from_function(
        enviar_correo_func,
        name="enviar_correo",
        description="Envía un correo necesitando solo el nombre del interesado, el correo del interesado y un mensaje para el interesado que va a depender del programa en el cuál él tenga el interés."
    )

    @staticmethod
    def registrar_google_sheet_func(nombre: str, correo: str, programa: str, promocion_julio: str):
        """Registra los datos del interesado pidiendo nombre, correo y programa, estos 3 datos son los que registra en su hoja."""
        registro = RegistroGoogleSheet()
        registro.registrar_google_sheets(nombre,correo,programa,promocion_julio)
    
    # Crear la herramienta estructurada
    registrar_google_sheet = StructuredTool.from_function(
        registrar_google_sheet_func,
        name="registrar_google_sheet",
        description="Registra los datos del interesado pidiendo nombre, correo y programa en Google Sheets."
    )
    
    # Agregar RAG como Tool
    @tool
    def consultar_DataPath(query: str, history_messages: list = None) -> str:
        """Usa el sistema RAG para buscar información sobre DataPath y devuelve la respuesta."""
        rag_instance = AIBot()  # Inicializar el sistema RAG
        # Usa historial de mensajes si está disponible
        if history_messages:
            response = rag_instance.invoke(history_messages, query)
        else:
            response = rag_instance.invoke([], query)
        return response
    
    @tool
    def lectura_promocion(promocion_curso: str, limit: int = None) -> list:
        """Obtiene promociones generadas por el equipo de Marketing para cada curso que este configurado con una promoción."""
        list_promocion = []
        promotions=GetPromotions()
        list_promocion = promotions.get_active_promotions(promocion_curso, limit = 3)
        formatted_promocion = promotions.format_promotions_output(list_promocion)
        return formatted_promocion
    
    #@staticmethod
    #def lectura_all_promocion_func():
    #    """Obtiene promociones generadas por el equipo de Marketing para cada curso que este configurado con una promoción."""
    #    list_all_promocion = GetPromotions.get_all_active_promotions()
    #    formatted_all_promocion = GetPromotions.format_promotions_output(list_all_promocion)
    #    return formatted_all_promocion
    
     # Crear la herramienta estructurada
    #lectura_all_promocion = StructuredTool.from_function(
    #    lectura_all_promocion_func,
    #    name="lectura_all_promocion",
    #    description="btiene promociones generadas por el equipo de Marketing."
    #)

    