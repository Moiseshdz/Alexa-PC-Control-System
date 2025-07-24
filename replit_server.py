# main.py - Servidor intermediario para Replit
# Este archivo va en tu proyecto de Replit

from flask import Flask, request, jsonify
import requests
import json
import socket
import struct
import time

app = Flask(__name__)

# ========== CONFIGURACIÓN - CAMBIAR ESTOS VALORES ==========
PC_IP = "192.168.1.XXX"  # ⚠️ CAMBIAR: IP local de tu PC
PC_MAC = "XX:XX:XX:XX:XX:XX"  # ⚠️ CAMBIAR: MAC address de tu PC
PC_PORT = 8000  # Puerto del servidor en tu PC
# ===========================================================

def send_wol_packet(mac_address):
    """
    Envía un paquete Wake-on-LAN al PC
    """
    try:
        print(f"🌟 Enviando Wake-on-LAN a MAC: {mac_address}")
        
        # Limpiar MAC address (quitar : y -)
        mac = mac_address.replace(':', '').replace('-', '').upper()
        
        # Validar formato MAC
        if len(mac) != 12:
            print(f"❌ MAC address inválida: {mac}")
            return False
        
        # Crear paquete mágico: 6 bytes FF + 16 repeticiones de MAC
        magic_packet = bytes.fromhex('FF' * 6 + mac * 16)
        
        # Enviar por UDP broadcast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Enviar a múltiples puertos por compatibilidad
        ports = [7, 9]  # Puertos comunes para WOL
        for port in ports:
            sock.sendto(magic_packet, ('255.255.255.255', port))
            print(f"📡 Paquete WOL enviado al puerto {port}")
        
        sock.close()
        print("✅ Wake-on-LAN enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando WOL: {e}")
        return False

def check_pc_status():
    """
    Verifica si el PC está encendido
    """
    try:
        print(f"🔍 Verificando estado del PC en {PC_IP}:{PC_PORT}")
        response = requests.get(
            f"http://{PC_IP}:{PC_PORT}/status", 
            timeout=8
        )
        
        if response.status_code == 200:
            print("✅ PC está ONLINE")
            return True
        else:
            print(f"⚠️ PC respondió con código: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - PC probablemente OFFLINE")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión - PC está OFFLINE")
        return False
    except Exception as e:
        print(f"❌ Error verificando PC: {e}")
        return False

def send_pc_command(command):
    """
    Envía comando al PC (shutdown, hibernate, cancel)
    """
    try:
        print(f"📤 Enviando comando '{command}' al PC")
        response = requests.post(
            f"http://{PC_IP}:{PC_PORT}/{command}", 
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Comando '{command}' enviado exitosamente")
            return response.json()
        else:
            print(f"⚠️ Error en comando: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error enviando comando '{command}': {e}")
        return None

@app.route('/')
def home():
    """Página de inicio con información del servidor"""
    return jsonify({
        "service": "Alexa PC Control Bridge",
        "status": "online",
        "version": "1.0",
        "endpoints": [
            "GET /test - Probar conexión con PC",
            "POST /alexa/power - Control de Alexa",
            "POST /wol - Wake-on-LAN manual",
            "GET /status - Estado del servidor"
        ],
        "pc_config": {
            "ip": PC_IP,
            "mac": PC_MAC,
            "port": PC_PORT
        }
    })

@app.route('/test')
def test():
    """Endpoint para probar la conexión con el PC"""
    pc_online = check_pc_status()
    
    return jsonify({
        "server": "online",
        "pc_status": "online" if pc_online else "offline",
        "pc_ip": PC_IP,
        "pc_mac": PC_MAC,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/wol', methods=['POST'])
def manual_wol():
    """Endpoint para enviar Wake-on-LAN manualmente"""
    success = send_wol_packet(PC_MAC)
    
    return jsonify({
        "action": "wake_on_lan",
        "success": success,
        "message": "WOL enviado exitosamente" if success else "Error enviando WOL",
        "mac_address": PC_MAC
    })

@app.route('/alexa/power', methods=['POST'])
def alexa_power_control():
    """
    Endpoint principal para Alexa
    Recibe comandos de encendido/apagado y responde en formato Alexa
    """
    try:
        print("\n" + "="*50)
        print(f"🎤 SOLICITUD DE ALEXA RECIBIDA")
        print("="*50)
        
        data = request.get_json()
        if not data:
            print("❌ No se recibió data JSON")
            return create_alexa_response("Error: no se recibió comando válido")
        
        action = data.get('action', '').lower()
        print(f"🎯 Acción solicitada: '{action}'")
        
        if action == 'on':
            print("🔄 Procesando: ENCENDER PC")
            
            # Verificar estado actual
            if check_pc_status():
                message = "Tu computadora ya está encendida"
                print(f"ℹ️ Resultado: {message}")
            else:
                # PC está apagado, intentar encender con WOL
                if send_wol_packet(PC_MAC):
                    # Esperar un momento para ver si WOL funcionó
                    print("⏳ Esperando respuesta del PC...")
                    time.sleep(5)
                    
                    if check_pc_status():
                        message = "Computadora encendida exitosamente"
                        print(f"✅ Resultado: {message}")
                    else:
                        message = "Señal de encendido enviada. El PC debería encender en unos momentos"
                        print(f"📡 Resultado: {message}")
                else:
                    message = "Error al enviar señal de encendido"
                    print(f"❌ Resultado: {message}")
            
            return create_alexa_response(message)
        
        elif action == 'off':
            print("🔄 Procesando: APAGAR PC")
            
            if check_pc_status():
                # PC está encendido, enviar comando de apagado
                result = send_pc_command('shutdown')
                if result:
                    message = "Apagando tu computadora"
                    print(f"✅ Resultado: {message}")
                else:
                    message = "Error al conectar con tu computadora para apagarla"
                    print(f"❌ Resultado: {message}")
            else:
                message = "Tu computadora ya está apagada"
                print(f"ℹ️ Resultado: {message}")
            
            return create_alexa_response(message)
        
        elif action == 'status':
            print("🔄 Procesando: VERIFICAR ESTADO")
            
            if check_pc_status():
                message = "Tu computadora está encendida"
            else:
                message = "Tu computadora está apagada"
            
            print(f"📊 Resultado: {message}")
            return create_alexa_response(message)
        
        else:
            message = f"Comando '{action}' no reconocido. Usa 'on', 'off' o 'status'"
            print(f"❌ Resultado: {message}")
            return create_alexa_response(message)
            
    except Exception as e:
        error_msg = f"Error interno del servidor: {str(e)}"
        print(f"💥 ERROR CRÍTICO: {error_msg}")
        return create_alexa_response("Lo siento, hubo un error interno")
    
    finally:
        print("="*50 + "\n")

def create_alexa_response(text):
    """
    Crea respuesta en formato estándar de Alexa
    """
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": True
        }
    })

@app.route('/status')
def server_status():
    """Estado del servidor intermediario"""
    return jsonify({
        "server": "online",
        "service": "Alexa PC Control Bridge",
        "pc_configured": PC_IP != "192.168.1.XXX",
        "configuration": {
            "pc_ip": PC_IP,
            "pc_mac": PC_MAC,
            "pc_port": PC_PORT
        },
        "last_check": time.strftime('%Y-%m-%d %H:%M:%S')
    })

# Middleware para logging
@app.before_request
def log_request():
    if request.endpoint not in ['home', 'server_status']:
        print(f"\n📨 {request.method} {request.path} - {request.remote_addr}")

if __name__ == '__main__':
    print("🚀 Iniciando servidor bridge Alexa-PC...")
    print(f"🖥️ PC configurado: {PC_IP} ({PC_MAC})")
    print("🔗 Servidor listo para recibir comandos de Alexa")
    
    # Verificar configuración
    if PC_IP == "192.168.1.XXX" or PC_MAC == "XX:XX:XX:XX:XX:XX":
        print("\n⚠️ ADVERTENCIA: Debes configurar PC_IP y PC_MAC en la parte superior del archivo")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
