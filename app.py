from flask import Flask, request, jsonify

from bot.ai_bot import AIBot
from services.waha import Waha

import time

import random

from agent_3_completo import DataPath

app = Flask(__name__)



@app.route('/chatbot/webhook/', methods=['POST']) #Endpoint
def webhook():
    data = request.json

    #Para no enviar mensaje de respuesta a los Grupos de Whatsapp que tengo -------------------------
    chat_id = data['payload']['from']
    received_message = data['payload']['body']
    is_group = '@g.us' in chat_id

    if is_group:
        return jsonify({'status': 'success', 'message': 'Mensaje de grupo/status ignorada'}), 200
    #------------------------------------------------------------------------------------------------

    print(f'EVENTO RECIBIDO: {data}')

    waha = Waha()
    #ai_bot = AIBot() #Este es solo para probar el RAG, sólo el RAG
    bot = DataPath()
    agente, tools = bot.crear_agente()

    waha.start_typing(chat_id=chat_id)

    #--------------------- Test del Agente con los 4 y luego 6 Tools ----------------
    # Procesar el mensaje con el Agente
    # try:
    #     resultado = bot.procesar_mensaje(received_message, agente, tools)
    #     response_message = resultado.get("output", "No se pudo procesar el mensaje correctamente.")
    # except Exception as e:
    #     response_message = f"Ocurrió un error: {str(e)}"
    #--------------------------------------------------------------------------------


    #---------------------- Test de Solo el RAG ----------------------
    # history_messages = waha.get_history_messages(
    #     chat_id=chat_id,
    #     limit=10, #Voy a coger los 10 últimos mensajes del chat
    # )
    # response_message = ai_bot.invoke(
    #     history_messages=history_messages,
    #     question=received_message,
    # )
    #----------------------------------------------------------------

    #--------------------------------- Test del RAG como Tool del Agente------------------------------
    # Obtener historial de mensajes para pasarlo al RAG
    history_messages = waha.get_history_messages(
        chat_id=chat_id,
        limit=10  # Recuperar los últimos 10 mensajes
    )
    
    try:
        resultado = bot.procesar_mensaje(received_message, agente, tools, history_messages)
        response_message = resultado.get("output", "No se pudo procesar el mensaje correctamente.")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        response_message = f"Ocurrió un error al procesar tu mensaje: {str(e)}"
    #--------------------------------------------------------------------------------------------------

    waha.send_message(
        chat_id=chat_id,
        message=response_message,
    )

    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)