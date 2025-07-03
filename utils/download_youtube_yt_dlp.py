import os
import re
import yt_dlp

class YoutubeDownloader:
    def bajar_video(self, link='https://www.youtube.com/watch?v=zUQxQKoMnOU'):
        print(f"Descargando vídeo del enlace: {link}")

        # Configuración de yt-dlp para extraer información
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bv*+ba/b',  # # Mejor video (bv*) + mejor audio (ba), sino el mejor disponible (b)
            #bv* → Descarga el mejor video disponible (sin audio).
            #+ba → Descarga el mejor audio disponible y lo combina con el video.
            #/b → Si no se pueden combinar, usa el mejor archivo disponible (con audio y video juntos).
            'merge_output_format': 'mp4',  # Formato final
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)  # Obtener metadata sin descargar
            titulo = info.get('title', 'video_descargado')  # Obtener título del video

        #Carpeta de descarga de los vídeos
        output_path = '_videos_descargados'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Creada carpeta '{output_path}'")

        # Limpiar el título del video para que sea un nombre de archivo válido
        title = re.sub(r'[<>:"/\\|?*]', '', titulo).replace("'", "").strip().replace(' ', '_')
        title = f'_{title}.mp4'
        video_path = os.path.join(output_path, title)

        # Opciones de descarga
        ydl_opts.update({
            'outtmpl': video_path,  # Ruta de salida del video
        })

        # Descargamos el video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        print(f"Descargado el vídeo '{titulo}' en '{video_path}'")
        return video_path

# if __name__ == '__main__':
#     yt = YoutubeDownloader()
#     link = 'https://www.youtube.com/watch?v=zUQxQKoMnOU'
#     yt.bajar_video(link)