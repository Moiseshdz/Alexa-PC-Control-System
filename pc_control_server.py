# Guardar como: C:\alexa-pc\pc_control.py
# Servidor web para controlar apagado del PC

import http.server
import socketserver
import subprocess
import json
import os
from urllib.parse import urlparse, parse_qs
import threading
import time
import socket

PORT = 8000

class PCControlHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override para logging personalizado"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")
    
    def do_OPTIONS(self):
        """Manejar preflight requests para CORS"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _set_cors_headers(self):
        """Configurar headers CORS"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_POST(self):
        if self.path == '/shutdown':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            print("🔴 Solicitud de apagado recibida")
            
            # Programar apagado en 10 segundos para dar tiempo a responder
            def delayed_shutdown():
                time.sleep(2)
                print("⏰ Ejecutando apagado del sistema...")
                os.system('shutdown /s /t 8 /c "Apagado iniciado por Alexa"')
            
            threading.Thread(target=delayed_shutdown, daemon=True).start()
            
            response = {
                "status": "success", 
                "message": "PC apagándose en 10 segundos",
                "countdown": 10
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/cancel':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            print("⏹️ Cancelando apagado...")
            os.system('shutdown /a')  # Cancelar apagado programado
            
            response = {"status": "success", "message": "Apagado cancelado"}
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/status':
            self._handle_status()
            
        elif self.path == '/hibernate':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            print("💤 Hibernando sistema...")
            
            def delayed_hibernate():
                time.sleep(2)
                os.system('shutdown /h')  # Hibernar
            
            threading.Thread(target=delayed_hibernate, daemon=True).start()
            
            response = {"status": "success", "message": "PC hibernando"}
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {"status": "error", "message": "Endpoint no encontrado"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_GET(self):
        if self.path == '/status':
            self._handle_status()
        elif self.path == '/':
            self._handle_web_interface()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")
    
    def _handle_status(self):
        """Manejar solicitudes de estado"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        
        # Obtener información del sistema
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            hostname = "Unknown"
            local_ip = "Unknown"
        
        response = {
            "status": "online",
            "message": "PC está encendido y listo",
            "hostname": hostname,
            "ip": local_ip,
            "port": PORT,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def _handle_web_interface(self):
        """Interfaz web simple para pruebas"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self._set_cors_headers()
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Control PC - Alexa</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial; margin: 40px; background: #f0f0f0; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
                button { padding: 15px 30px; margin: 10px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; }
                .shutdown { background: #ff4444; color: white; }
                .cancel { background: #44ff44; color: black; }
                .status { background: #4444ff; color: white; }
                .hibernate { background: #ff8800; color: white; }
                #result { margin: 20px 0; padding: 15px; border-radius: 5px; background: #f9f9f9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🖥️ Control PC - Alexa</h1>
                <p>Servidor funcionando correctamente en puerto """ + str(PORT) + """</p>
                
                <h3>Pruebas manuales:</h3>
                <button class="status" onclick="testStatus()">📊 Estado del PC</button>
                <button class="shutdown" onclick="testShutdown()">🔴 Apagar PC</button>
                <button class="hibernate" onclick="testHibernate()">💤 Hibernar PC</button>
                <button class="cancel" onclick="testCancel()">⏹️ Cancelar Apagado</button>
                
                <div id="result"></div>
                
                <h3>📋 Información:</h3>
                <ul>
                    <li><strong>Estado:</strong> ✅ Servidor activo</li>
                    <li><strong>Puerto:</strong> """ + str(PORT) + """</li>
                    <li><strong>Endpoints disponibles:</strong></li>
                    <ul>
                        <li>GET /status - Estado del PC</li>
                        <li>POST /shutdown - Apagar PC</li>
                        <li>POST /hibernate - Hibernar PC</li>
                        <li>POST /cancel - Cancelar apagado</li>
                    </ul>
                </ul>
            </div>
            
            <script>
                function showResult(data, type = 'info') {
                    const result = document.getElementById('result');
                    result.innerHTML = '<strong>' + type.toUpperCase() + ':</strong> ' + JSON.stringify(data, null, 2);
                    result.style.background = type === 'error' ? '#ffeeee' : '#eeffee';
                }
                
                function testStatus() {
                    fetch('/status')
                        .then(response => response.json())
                        .then(data => showResult(data, 'success'))
                        .catch(error => showResult(error.message, 'error'));
                }
                
                function testShutdown() {
                    if (confirm('¿Seguro que quieres apagar el PC?')) {
                        fetch('/shutdown', { method: 'POST' })
                            .then(response => response.json())
                            .then(data => showResult(data, 'success'))
                            .catch(error => showResult(error.message, 'error'));
                    }
                }
                
                function testHibernate() {
                    if (confirm('¿Seguro que quieres hibernar el PC?')) {
                        fetch('/hibernate', { method: 'POST' })
                            .then(response => response.json())
                            .then(data => showResult(data, 'success'))
                            .catch(error => showResult(error.message, 'error'));
                    }
                }
                
                function testCancel() {
                    fetch('/cancel', { method: 'POST' })
                        .then(response => response.json())
                        .then(data => showResult(data, 'success'))
                        .catch(error => showResult(error.message, 'error'));
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

def get_local_ip():
    """Obtener IP local del PC"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    try:
        local_ip = get_local_ip()
        
        print("=" * 60)
        print("🖥️  SERVIDOR DE CONTROL PC - ALEXA")
        print("=" * 60)
        print(f"✅ Servidor iniciado exitosamente")
        print(f"🌐 IP Local: {local_ip}")
        print(f"🔌 Puerto: {PORT}")
        print(f"🔗 URL Local: http://{local_ip}:{PORT}")
        print(f"🔗 URL Localhost: http://localhost:{PORT}")
        print("")
        print("📋 Endpoints disponibles:")
        print(f"   GET  http://{local_ip}:{PORT}/status")
        print(f"   POST http://{local_ip}:{PORT}/shutdown")
        print(f"   POST http://{local_ip}:{PORT}/hibernate")
        print(f"   POST http://{local_ip}:{PORT}/cancel")
        print("")
        print("🌍 Abre en navegador: http://localhost:8000")
        print("⏹️  Presiona Ctrl+C para detener")
        print("=" * 60)
        
        with socketserver.TCPServer(("", PORT), PCControlHandler) as httpd:
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
        print("💡 Tips:")
        print("   - Verificar que el puerto 8000 no esté en uso")
        print("   - Ejecutar como administrador si es necesario")
        print("   - Verificar firewall de Windows")
        input("\nPresiona Enter para cerrar...")
