"""
Aplicación web para el chatbot MAC-GPT.
"""
import os
from flask import Flask, render_template, request, jsonify
from src.chatbot import ask_mac_gpt, configure_google_api
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'mac-gpt-secret-key')

# Configurar la API de Google
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
api_configured = False
if api_key:
    api_configured = configure_google_api(api_key)

@app.route('/')
def index():
    """
    Renderiza la página principal del chatbot.
    """
    return render_template('index.html', api_configured=api_configured)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint para procesar mensajes del chat.
    """
    if not api_configured:
        return jsonify({
            'success': False,
            'message': 'La API de Google no está configurada correctamente. Por favor, comprueba tu API key.'
        }), 500

    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó ninguna pregunta.'
        }), 400

    try:
        # Obtener respuesta del chatbot
        response = ask_mac_gpt(message)
        return jsonify({
            'success': True,
            'message': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al procesar la pregunta: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """
    Endpoint para verificar el estado de la API.
    """
    return jsonify({
        'api_configured': api_configured,
        'status': 'ready' if api_configured else 'not_configured'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) 