import os
import re

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

class Notes:
    def crea_tags(texto):
        """Crea etiquetas relacionadas con el texto."""
        print('Creando etiquetas...')
        tags = llm.invoke(
            f'Crea hasta 10 etiquetas relacionadas con este texto: \n{texto}\n'
            f'Debes responder solo con las etiquetas, sin comentarios ni numeración.\n'
            f'Las etiquetas deben estar en una única línea, separadas por un espacio.\n'
            f'Deben estar relacionadas únicamente con el contenido del texto.\n'
            f'Por ejemplo, un texto sobre filosofía puede tener la etiqueta #filosofía.\n'
            f'Otro ejemplo, un texto sobre entrenamiento en el gimnasio puede tener las etiquetas #fitness #salud.\n'
            f'Todas las etiquetas deben llevar # al inicio, por ejemplo: #ejemplo.'
            )
        return tags.content

    def crea_resumen_corto(texto):
        """Crea un resumen corto de hasta 20 palabras de la transcripción."""
        print('Creando resumen corto...')
        resumen_corto = llm.invoke(
            f'Crea un resumen del texto en 20 palabras: \n{texto}'
            )
        return resumen_corto.content

    def crea_resumen_detallado(texto):
        """Crea un resumen detallado de la transcripción."""
        print('Creando resumen detallado...')
        resumen_detallado= llm.invoke(
            f'Resume detalladamente el texto: \n{texto}\n'
            f'Mantén toda la información importante de forma estructurada.\n'
            f'El resumen debe contener toda la información necesaria para que una persona que no leyó el texto original pueda entenderlo completamente.'
            )
        return resumen_detallado.content

    def crea_bullet_point(texto):
        """Crea una lista de puntos clave basada en la transcripción."""
        print('Creando lista de puntos clave...')
        bullet_point = llm.invoke(
            f'Enumera en puntos clave las ideas principales relacionadas con el texto: \n{texto}'
            )
        return bullet_point.content

    def formatea_nota(tags, resumen_corto, resumen_detallado, bullet_point):
        """Da formato a los textos en una única nota con título, etiquetas y resúmenes."""
        print('Formateando texto...')
        texto_final = (
            f'{tags}\n\n'
            f'# Resumen del Video\n\n'
            f'## Resumen Corto\n{resumen_corto}\n\n'
            f'## Resumen Detallado\n{resumen_detallado}\n\n'
            f'## Puntos Clave\n{bullet_point}\n\n'
            # f'Link: {msg}'
        )
        return texto_final

    def guardar_nota(transcripcion_path):
        """Guarda el texto en un archivo en el directorio _notas."""
        print('Creando texto de la nota...')
        
        transcripcion_path = transcripcion_path.replace("'", "")
        print(f'transcripcion_path {transcripcion_path}')

        with open(transcripcion_path, "rb") as file:
            transcripcion = file.read()
            tags = Notes.crea_tags(transcripcion)
            resumen_corto = Notes.crea_resumen_corto(transcripcion)
            resumen_detallado = Notes.crea_resumen_detallado(transcripcion)
            bullet_point = Notes.crea_bullet_point(transcripcion)
            nota = Notes.formatea_nota(tags, resumen_corto, resumen_detallado, bullet_point)
            print ('nota creada\n\n')

        output_path = os.path.dirname(transcripcion_path)
        output_path = output_path.replace('transcripciones_extraídos_descargados', 'notas')

        base_name = os.path.splitext(os.path.basename(transcripcion_path))[0]
        resumen_path = f'{output_path}/{base_name}.md'

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Carpeta creada 'notas' en: {output_path}")
        
        with open(resumen_path, 'w') as f:
            f.write(nota)
        print(f"Nota guardada en: {resumen_path}")

        return nota

if __name__ == '__main__':
    transcripcion_path =  '_transcripciones_extraídos_descargados/_Wesley_Safadão_-_Jejum_de_Amor_-_TBT_WS_2.md'
    Notes.guardar_nota(transcripcion_path)