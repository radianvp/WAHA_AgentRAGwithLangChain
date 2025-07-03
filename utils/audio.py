import os

from moviepy.editor import *

from faster_whisper import WhisperModel

from dotenv import load_dotenv
load_dotenv()

class Audio:
    def extraer(video_path):
        #video_path = f'/app/{video_path}'
        """Extrae el audio de un vídeo y guarda en formato .mp3."""
        print(f"\nExtrayendo audio del video: {video_path}")
        
        video_path = video_path.replace("'", "") #Garantizamos que el vídeo no tenga comillas simples
        
        print(f'video_path = {video_path}')
        
        output_path = os.path.dirname(video_path)
        output_path = output_path.replace('videos', 'audios_extraídos')
        print(f'output_path = {output_path}')
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        print(f'basename = {base_name}')

        audio_path = f'{output_path}/{base_name}.mp3'
        print(f'audio_path = {audio_path}')

        video = VideoFileClip(video_path)

        #Creamos la carpeta que guarda los audios extraídos de los vídeos
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Carpeta creada {output_path}")
        #----------------------------------------------------------------

        video.audio.write_audiofile(audio_path)

        print(f'Audio guardado en: {audio_path}')
        print("") #Para dejar un espacio entre esta y la segunda función que se va a ejecutar
        return audio_path

    def transcribir(audio_path: str) -> str:
        """Transcribe un archivo de audio guardado en audio_path a texto utilizando reconocimiento de voz."""
        print(f"Transcribiendo audio: {audio_path}")
        
        audio_path = audio_path.replace("'", "") #Garantizamos que el vídeo no tenga comillas simples
        model = WhisperModel("small") # , "cuda" "medium"

        result = model.transcribe(audio_path)

        transcripcion = ""
        for segment in result[0]:
            transcripcion += segment.text + " "

        #Creamos la carpeta que guarda los audios extraídos de los vídeos
        output_path = os.path.dirname(audio_path)
        output_path = output_path.replace('audios', 'transcripciones')
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        transcripcion_path = f'{output_path}/{base_name}.md'

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Carpeta creada '{output_path}'")

        with open(transcripcion_path, 'w') as f:
            f.write(transcripcion.strip())

        print(f'Transcripción guardada en: {transcripcion_path}')
        return transcripcion_path

# if __name__ == '__main__':
#     video_path = '_videos_descargados/_Wesley_Safadão_-_Jejum_de_Amor_-_TBT_WS_2.mp4'
#     print('PARA PROBAR, AGREGA LA RUTA DE UN VIDEO MP4')
#     audio_path = Audio.extraer(video_path)
#     transcricao = Audio.transcribir(audio_path)