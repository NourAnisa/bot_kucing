import makeWASocket, {
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    Browsers
} from '@whiskeysockets/baileys';
import pino from 'pino';
import fs from 'fs';
import path from 'path';

const tempDir = './test_auth_temp';
try { fs.rmSync(tempDir, { recursive: true, force: true }); } catch (e) {}
fs.mkdirSync(tempDir, { recursive: true });

const { state, saveCreds } = await useMultiFileAuthState(tempDir);
const { version } = await fetchLatestBaileysVersion();

console.log("Baileys version:", version.join('.'));

const sock = makeWASocket({
    version,
    logger: pino({ level: 'debug' }),
    auth: state,
    browser: Browsers.ubuntu("Chrome"),
    printQRInTerminal: false
});

sock.ev.on('creds.update', saveCreds);

sock.ev.on('connection.update', (update) => {
    console.log("Connection update:", JSON.stringify(update));
});

setTimeout(async () => {
    try {
        console.log("Requesting pairing code for 6285155133070...");
        const code = await sock.requestPairingCode("6285155133070");
        console.log("Received code:", code);
    } catch (e) {
        console.error("Pairing code error:", e);
    }
}, 3000);
