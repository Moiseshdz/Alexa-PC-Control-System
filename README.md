# 📋 Instrucciones de Instalación - Control PC con Alexa

## 🚀 PASO 1: CONFIGURAR TU PC

### 1.1 Crear carpeta del proyecto
```cmd
# Crear carpeta en C:\
mkdir C:\alexa-pc
cd C:\alexa-pc
```

### 1.2 Descargar y guardar archivos
1. **pc_control.py** → Guardar en `C:\alexa-pc\pc_control.py`
2. **start_server.bat** → Guardar en `C:\alexa-pc\start_server.bat`

### 1.3 Obtener información de tu PC
```cmd
# Ejecutar en CMD para obtener IP
ipconfig

# Anotar tu IP local (ej: 192.168.1.105)

# Ejecutar para obtener MAC
getmac /v

# Anotar la MAC de tu adaptador Ethernet
# Formato: XX-XX-XX-XX-XX-XX
```

### 1.4 Configurar Wake-on-LAN

#### En BIOS:
1. Reiniciar PC → Entrar a BIOS (F2/F12/Del)
2. Buscar "Power Management" o "Advanced"
3. Habilitar:
   - ☑️ Wake on LAN
   - ☑️ Wake on PCI-E
   - ☑️ Power on by PCI-E
4. Guardar y salir (F10)

#### En Windows:
1. `Clic derecho en "Este equipo" → Propiedades → Administrador de dispositivos`
2. `Adaptadores de red → Clic derecho en Ethernet → Propiedades`
3. **Pestaña "Administración de energía":**
   - ☑️ Permitir que este dispositivo active el equipo
   - ☑️ Solo permitir que un paquete mágico active el equipo
4. **Pestaña "Opciones avanzadas":**
   - `Wake on Magic Packet` → **Enabled**
   - `Wake on pattern match` → **Enabled**

#### Desactivar inicio rápido:
1. `Panel de control → Opciones de energía`
2. `Elegir el comportamiento del botón de inicio/apagado`
3. `Cambiar la configuración actualmente no disponible`
4. **DESMARCAR:** ☐ Activar inicio rápido

### 1.5 Probar el servidor local
1. Ejecutar `start_server.bat`
2. Abrir navegador → `http://localhost:8000`
3. Probar botones de la interfaz web
4. **Si funciona:** ✅ Continuar al Paso 2

---

## 🌐 PASO 2: CONFIGURAR SERVIDOR REPLIT

### 2.1 Crear cuenta en Replit
1. Ir a [https://replit.com](https://replit.com)
2. Crear cuenta gratuita
3. `Create Repl → Python`
4. Nombre: `alexa-pc-control`

### 2.2 Configurar archivos en Replit

#### Archivo: `main.py`
- Copiar el código del archivo **main.py**
- **⚠️ IMPORTANTE:** Cambiar estas líneas:
```python
PC_IP = "192.168.1.XXX"  # ← Tu IP real
PC_MAC = "XX:XX:XX:XX:XX:XX"  # ← Tu MAC real (con :)
```

#### Archivo: `requirements.txt`
- Crear nuevo archivo: `requirements.txt`
- Copiar el contenido del archivo **requirements.txt**

### 2.3 Ejecutar y probar
1. Clic en **"Run"** en Replit
2. Anotar la URL que aparece (ej: `https://alexa-pc-control.username.repl.co`)
3. Probar endpoints:
   - `GET /test` → Debe mostrar estado del PC
   - `POST /wol` → Debe intentar encender PC

**Mantener Replit siempre ejecutándose** (pestaña abierta)

---

## 🎤 PASO 3: CREAR ALEXA SKILL

### 3.1 Amazon Developer Console
1. Ir a [https://developer.amazon.com/alexa/console/ask](https://developer.amazon.com/alexa/console/ask)
2. Iniciar sesión / Crear cuenta
3. `Create Skill`
4. Configurar:
   - **Skill name:** `Control PC`
   - **Primary locale:** `Spanish (MX)` o `Spanish (ES)`
   - **Model:** `Custom`
   - **Hosting:** `Alexa-hosted (Node.js)`
5. `Create skill`

### 3.2 Configurar Interaction Model
1. En el menú izquierdo: `Build → JSON Editor`
2. **Borrar todo** el contenido actual
3. Copiar y pegar el contenido de **interaction-model.json**
4. `Save Model → Build Model`
5. ⏳ Esperar que termine de compilar

### 3.3 Configurar el código Lambda
1. Ir a `Code → index.js`
2. **Borrar todo** el contenido actual
3. Copiar y pegar el contenido de **index.js**
4. **⚠️ IMPORTANTE:** Cambiar esta línea:
```javascript
const SERVER_URL = 'https://tu-proyecto.username.repl.co';
// ↑ Cambiar por tu URL real de Replit
```
5. `Save → Deploy`

### 3.4 Probar el skill
1. Ir a `Test`
2. Cambiar dropdown a `Development`
3. Probar comandos:
   - **"abre control pc"**
   - **"enciende mi computadora"**
   - **"apaga mi pc"**

---

## ✅ PASO 4: CONFIGURACIÓN FINAL

### 4.1 Configurar inicio automático (Opcional)
Para que el servidor se inicie con Windows:

1. `Windows + R → shell:startup → Enter`
2. Copiar `start_server.bat` a esta carpeta
3. El servidor se iniciará automáticamente

### 4.2 Configurar firewall
Si Windows pregunta sobre el firewall:
- ✅ **Permitir acceso** para redes privadas
- ✅ **Permitir acceso** para redes públicas

### 4.3 Mantener Replit activo
Replit gratuito se duerme después de inactividad:

**Opciones:**
1. **Manual:** Mantener pestaña abierta
2. **UptimeRobot:** Crear monitor gratuito que haga ping cada 5 minutos
3. **Upgrade Replit:** Pagar por Always On ($5/mes)

---

## 🎯 COMANDOS DE VOZ FINALES

Una vez configurado completamente:

### Comandos directos:
- **"Alexa, abre control PC"**
- **"Alexa, dile a control PC que encienda mi computadora"**
- **"Alexa, dile a control PC que apague mi PC"**
- **"Alexa, dile a control PC cuál es el estado de mi computadora"**

### Con rutinas (opcional):
Crear rutinas en Alexa app para comandos más cortos:
- **"Alexa, enciende mi PC"** → Ejecutar skill
- **"Alexa, apaga mi PC"** → Ejecutar skill

---

## 🔧 TROUBLESHOOTING

### ❌ PC no enciende con WOL
**Posibles causas:**
- Cable Ethernet desconectado
- WOL no habilitado en BIOS
- Router bloquea broadcast
- PC completamente apagado (debe estar en sleep/hibernate)

**Soluciones:**
1. Verificar configuración BIOS
2. Probar WOL manual: `wakeonlan XX:XX:XX:XX:XX:XX`
3. En router, buscar "Enable WOL" o "Allow broadcast"

### ❌ No se puede apagar PC
**Posibles causas:**
- Servidor local no está ejecutándose
- Firewall bloquea puerto 8000
- IP del PC cambió

**Soluciones:**
1. Verificar que `start_server.bat` esté corriendo
2. Probar manualmente: abrir `http://localhost:8000`
3. Verificar IP con `ipconfig`

### ❌ Alexa no responde
**Posibles causas:**
- Replit está dormido
- URL incorrecta en Lambda
- Error en configuración del skill

**Soluciones:**
1. Verificar que Replit esté ejecutándose
2. Revisar logs en Alexa Developer Console
3. Probar endpoints de Replit manualmente

### ❌ Error "No pude conectar"
**Posibles causas:**
- PC y router en redes diferentes
- NAT/Firewall bloquea conexión
- IP pública vs privada

**Soluciones:**
1. Asegurar que PC y Alexa estén en misma red
2. Configurar port forwarding si es necesario
3. Usar IP privada local (192.168.x.x)

---

## 📊 VERIFICACIÓN FINAL

### ✅ Checklist completo:
- [ ] PC configurado para WOL
- [ ] Servidor local funciona (`http://localhost:8000`)
- [ ] Replit ejecutándose con IPs correctas
- [ ] Alexa Skill creado y desplegado
- [ ] URLs actualizadas en Lambda
- [ ] Firewall permite conexiones
- [ ] Pruebas de voz exitosas

### 🎉 ¡LISTO!
Si todos los pasos están completos, tu PC debería responder a:
**"Alexa, dile a control PC que encienda mi computadora"**

---

## 💡 MEJORAS FUTURAS

1. **Rutinas Alexa:** Comandos más cortos
2. **Multiple PCs:** Controlar varios equipos
3. **Scheduling:** Encendido/apagado programado
4. **Mobile App:** Control desde celular
5. **Status LED:** Indicador visual de estado
