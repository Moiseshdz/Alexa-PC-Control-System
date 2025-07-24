// index.js - Código para AWS Lambda (Alexa Skill)
// Este código va en la sección "Code" de tu Alexa Skill

const Alexa = require('ask-sdk-core');
const https = require('https');
const http = require('http');

// ========== CONFIGURACIÓN ==========
// ⚠️ CAMBIAR por la URL de tu servidor Replit
const SERVER_URL = 'https://tu-proyecto.username.repl.co';
// Ejemplo: 'https://alexa-pc-control.juan123.repl.co'
// ===================================

/**
 * Realiza llamada HTTP al servidor intermedio
 */
function callPCServer(action) {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({ action: action });
        const url = new URL(SERVER_URL + '/alexa/power');
        
        console.log(`🔗 Conectando a: ${url.href}`);
        console.log(`📤 Enviando acción: ${action}`);
        
        const options = {
            hostname: url.hostname,
            port: url.port || (url.protocol === 'https:' ? 443 : 80),
            path: url.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData),
                'User-Agent': 'Alexa-Skill/1.0'
            },
            timeout: 15000  // 15 segundos timeout
        };

        const client = url.protocol === 'https:' ? https : http;
        const req = client.request(options, (res) => {
            let data = '';
            
            console.log(`📨 Respuesta HTTP: ${res.statusCode}`);
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    console.log(`✅ Respuesta recibida:`, response);
                    resolve(response);
                } catch (e) {
                    console.error(`❌ Error parseando JSON:`, e);
                    console.error(`📄 Data recibida:`, data);
                    reject(new Error('Respuesta inválida del servidor'));
                }
            });
        });

        req.on('error', (error) => {
            console.error(`🚫 Error de conexión:`, error);
            reject(error);
        });
        
        req.on('timeout', () => {
            console.error(`⏰ Timeout de conexión`);
            req.destroy();
            reject(new Error('Timeout de conexión'));
        });

        req.write(postData);
        req.end();
    });
}

/**
 * Handler para encender el PC
 */
const PowerOnIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'PowerOnIntent';
    },
    async handle(handlerInput) {
        console.log('🔛 Intent: PowerOnIntent');
        
        try {
            const result = await callPCServer('on');
            
            // Extraer mensaje de la respuesta
            let speechText = 'Comando de encendido enviado';
            if (result.response && result.response.outputSpeech && result.response.outputSpeech.text) {
                speechText = result.response.outputSpeech.text;
            }
            
            console.log(`🗣️ Respuesta Alexa: ${speechText}`);
            
            return handlerInput.responseBuilder
                .speak(speechText)
                .getResponse();
                
        } catch (error) {