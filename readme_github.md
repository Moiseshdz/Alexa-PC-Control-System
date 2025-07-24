# 🎤 Alexa PC Control System

Sistema completo para controlar tu PC con comandos de voz de Alexa. Permite encender, apagar y verificar el estado de tu computadora usando solo software (sin hardware adicional).

## 🚀 Características

- ✅ **Encendido remoto** usando Wake-on-LAN
- ✅ **Apagado remoto** mediante servidor web local
- ✅ **Verificación de estado** en tiempo real
- ✅ **Control por voz** con Alexa
- ✅ **Interfaz web** para pruebas manuales
- ✅ **100% software** - no requiere hardware adicional
- ✅ **Gratuito** - usa servicios cloud gratuitos

## 🎯 Comandos de Voz

```
"Alexa, dile a control PC que encienda mi computadora"
"Alexa, dile a control PC que apague mi PC"
"Alexa, dile a control PC cuál es el estado de mi computadora"
```

## 🏗️ Arquitectura del Sistema

```
[Alexa] → [AWS Lambda] → [Replit Server] → [Tu PC]
```

1. **Alexa** recibe comando de voz
2. **AWS Lambda** procesa el intent
3. **Servidor Replit** actúa como intermediario
4. **Tu PC** ejecuta la acción (WOL o shutdown)

## 📋 Requisitos

### Hardware
- PC con Windows 10/11
- Conexión Ethernet (para Wake-on-LAN)
- Router compatible con broadcast

### Software
- Python 3.7+ instalado
- Cuenta Amazon Developer (gratuita)
- Cuenta AWS (nivel gratuito)
- Cuenta Replit (gratuita)

### Red
- PC y Alexa en la misma red local
- Puerto 8000 disponible
- Wake-on-LAN habilitado

## 🛠️ Instalación

### Paso 1: Configurar tu PC

1. **Clonar repositorio:**
```cmd
git clone https://github.com/tu-usuario/alexa-pc-control.git
cd alexa-pc-control
```

2. **Obtener información de red:**
```cmd
ipconfig          # Anotar IP local
getmac /v         # Anotar MAC address
```

3. **Habilitar Wake-on-LAN:**
   - BIOS: Habilitar "Wake on LAN"
   - Windows: Configurar adaptador de red
   - Desactivar "inicio rápido"

4. **Ejecutar servidor:**
```cmd
start_server.bat
```

5. **Probar en navegador:**
```
http://localhost:8000
```

### Paso 2: Configurar Replit

1. Crear proyecto en [Replit.com](https://replit.com)
2. Subir `main.py` y `requirements.txt`
3. **Configurar variables:**
```python
PC_IP = "192.168.1.XXX"     # Tu IP real
PC_MAC = "XX:XX:XX:XX:XX:XX" # Tu MAC real
```
4. Ejecutar y anotar URL

### Paso 3: Crear Alexa Skill

1. [Amazon Developer Console](https://developer.amazon.com/alexa/console/ask)
2. Create Skill → Custom → Alexa-hosted
3. **Build:** Pegar `interaction-model.json`
4. **Code:** Pegar `index.js` y configurar URL de Replit
5. Deploy y Test

## 📁 Estructura del Proyecto

```
alexa-pc-control/
├── 📄 README.md                    # Este archivo
├── 📄 .gitignore                   # Archivos a ignorar
├── 📄 setup_instructions.md        # Instrucciones detalladas
│
├── 🖥️ pc-server/
│   ├── 📄 pc_control.py           # Servidor principal del PC
│   └── 📄 start_server.bat        # Script de inicio
│
├── 🌐 replit-bridge/
│   ├── 📄 main.py                 # Servidor intermediario
│   └── 📄 requirements.txt        # Dependencias Python
│
└── 🎤 alexa-skill/
    ├── 📄 index.js                # Código AWS Lambda
    └── 📄 interaction-model.json   # Modelo de voz
```

## 🔧 Configuración

### Variables de Entorno

**En `main.py` (Replit):**
```python
PC_IP = "192.168.1.105"              # IP de tu PC
PC_MAC = "AA:BB:CC:DD:EE:FF"         # MAC de tu PC
PC_PORT = 8000                       # Puerto del servidor
```

**En `index.js` (Lambda):**
```javascript
const SERVER_URL = 'https://tu-proyecto.username.repl.co';
```

## 🌐 Endpoints API

### Servidor PC (Puerto 8000)
```
GET  /status     # Estado del PC
POST /shutdown   # Apagar PC
POST /hibernate  # Hibernar PC  
POST /cancel     # Cancelar apagado
```

### Servidor Replit
```
GET  /test           # Probar conexión
POST /alexa/power    # Control desde Alexa
POST /wol            # Wake-on-LAN manual
```

## 🔍 Troubleshooting

### ❌ PC no enciende
- Verificar WOL en BIOS
- Cable Ethernet conectado
- PC en sleep/hibernate (no apagado completo)

### ❌ No se puede apagar
- Servidor local ejecutándose
- Firewall permite puerto 8000
- IP correcta en configuración

### ❌ Alexa no responde
- Replit ejecutándose
- URL correcta en Lambda
- Skill habilitado en Alexa app

## 📱 Uso

### Comandos directos:
```
"Alexa, abre control PC"
"Alexa, dile a control PC que enciende mi computadora"
```

### Con rutinas (opcional):
```
"Alexa, enciende mi PC"
"Alexa, apaga mi PC"
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crear branch (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'Agregar mejora'`)
4. Push al branch (`git push origin feature/mejora`)
5. Abrir Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

- **Tu Nombre** - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Comunidad de Alexa Skills Kit
- Documentación de Wake-on-LAN
- Usuarios que reportaron bugs y mejoras

## ⭐ Si te gustó el proyecto

¡Dale una estrella ⭐ al repositorio y compártelo!

---

### 🔗 Enlaces Útiles

- [Documentación Alexa Skills Kit](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html)
- [Wake-on-LAN Tutorial](https://www.howtogeek.com/70374/how-to-geek-explains-what-is-wake-on-lan-and-how-do-i-enable-it/)
- [Replit Documentation](https://docs.replit.com/)

---

**💡 ¿Necesitas ayuda?** Abre un [Issue](https://github.com/tu-usuario/alexa-pc-control/issues) con tu problema.