
# 🤖 Proyect2: Agente Inteligente Multiherramientas con RAG y WhatsApp

**Proyect2** es un agente conversacional autónomo impulsado por LLMs, diseñado para ejecutar tareas complejas como recuperación semántica (RAG), procesamiento de contenido multimedia, automatización de comunicación con clientes y respuesta a consultas vía **WhatsApp**. Se apoya en tecnologías como **LangChain**, **OpenAI**, **Chroma**, y **WAHA**.

---

## 🚀 Características Principales

- 🤖 Agente construido con **LangChain** y múltiples herramientas personalizadas  
- 📚 Recuperación aumentada con generación (**RAG**) utilizando **Chroma** como vector store  
- 💬 Integración directa con WhatsApp usando **WAHA** (Webhook Adapter)  
- 🎥 Descarga, transcripción y resumen de videos de YouTube  
- 📧 Envío de correos automatizados y registro en Google Sheets  
- 📢 Lectura dinámica de promociones de marketing  

---

## 🧩 Tecnologías Utilizadas

| Tecnología      | Propósito                                                   |
|----------------|--------------------------------------------------------------|
| `LangChain`     | Framework modular para agentes LLM                          |
| `OpenAI`        | Generación de lenguaje con GPT-4/GPT-3.5                    |
| `Chroma`        | Almacenamiento vectorial local para recuperación semántica |
| `WAHA`          | Integración WhatsApp mediante Webhook API                   |
| `Python`        | Lenguaje principal del proyecto                             |
| `Docker`        | Contenerización y despliegue                                |

---

## 📂 Estructura del Proyecto

```bash
📁 proyect2-ai-agent/
├── 📄 Dockerfile                  # Contenedor principal (backend, RAG, etc.)
├── 📄 Dockerfile.api              # Contenedor específico para app.py (API)
├── 📄 docker-compose.yml          # Orquestación de servicios (API, WAHA, Chroma, etc.)
├── 📄 README.md                   # Documentación del proyecto
├── 📄 requirements.txt            # Lista de dependencias
├── 📄 Nota_Importante.txt         # Advertencias o instrucciones internas
├── 📄 app.py                      # Punto de entrada del backend o API
├── 📄 agent_3_completo.py         # Configuración completa del agente LangChain
├── 📄 tools_3_completo.py         # Todas las herramientas (tools) integradas
│
├── 📁 bot/                        # Módulo de integración con WhatsApp (WAHA)
│   └── webhook.py                # Lógica del webhook para enviar y recibir mensajes
│
├── 📁 services/                   # Servicios externos y lógicos
│   ├── email.py                  # Envío de correos electrónicos personalizados
│   ├── sheets.py                 # Registro de leads en Google Sheets
│   └── promotions.py             # Consulta de promociones activas
│
├── 📁 utils/                      # Funcionalidades auxiliares
│   ├── youtube.py                # Descarga de videos de YouTube
│   ├── audio.py                  # Extracción de audio y transcripción
│   └── notes.py                  # Guardado y resumen de notas transcritas
│
├── 📁 RAG/                        # Recuperación aumentada con generación
│   ├── chroma_store.py           # Configuración y conexión con Chroma
│   ├── loader.py                 # Ingesta y vectorización de documentos
│   └── rag_tool.py               # Tool LangChain para consultar base RAG
```

---

## 🔧 Herramientas del Agente (LangChain Tools)

### 🎥 Multimedia

- `bajar_video_de_youtube(link)`: Descarga un video desde YouTube.  
- `extraer_audio(video_path)`: Extrae el audio del video.  
- `transcribir_audio(audio_path)`: Convierte el audio a texto.  
- `guardar_nota(transcripcion_path)`: Guarda la transcripción y genera un resumen útil.  

### 📬 Comunicación y Marketing

- `enviar_correo(nombre, correo, mensaje)`: Envía correos personalizados a leads.  
- `registrar_google_sheet(nombre, correo, programa, promocion)`: Registra interesados en una hoja de cálculo.  
- `lectura_promocion(curso)`: Muestra promociones activas según el curso.  

### 🔍 Recuperación Semántica

- `consultar_DataPath(query)`: Usa RAG (Chroma + embeddings) para buscar contenido técnico/documental.  

---

## ⚙️ Requisitos

- Python 3.10+  
- Docker & Docker Compose  
- OpenAI API Key  
- WAHA corriendo en entorno accesible  
- Chroma DB (modo local)  

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧪 Ejecución local

```bash
# Cargar documentos en Chroma (opcional)
python RAG/loader.py

# Ejecutar backend/API
python app.py
```

O vía Docker Compose:

```bash
docker-compose up --build
```

---

## 📱 Integración con WhatsApp (WAHA)

1. Configura WAHA y apunta el Webhook al backend.  
2. Usa el endpoint del webhook (en `bot/webhook.py`) para recibir mensajes.  
3. El agente procesará la entrada y devolverá una respuesta automática al usuario.  

---

## 📌 Estado Actual

- ✅ Agente LLM funcional con herramientas personalizadas  
- ✅ RAG con Chroma y búsqueda semántica  
- ✅ Recepción y respuesta por WhatsApp (WAHA)  
- 🟡 Interfaz de usuario para testing manual (pendiente)  
- 🟡 Log de métricas y seguimiento de conversaciones  

---

## 📜 Licencia

Este proyecto está bajo licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙌 Autor

**RadianVP**  
Desarrollador de soluciones de inteligencia artificial generativa e integración con agentes autónomos.  
Contacto: [radianvp@gmail.com]

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias al apoyo y la guía de **Datapath** y al acompañamiento del profesor **Kevin Inofuente** [@KevinInoCol], cuyo conocimiento y visión han sido fundamentales para el desarrollo de esta solución.
