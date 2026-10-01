import makeWASocket, {
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion,
    Browsers
} from '@whiskeysockets/baileys';
import pino from 'pino';
import express from 'express';
import QRCode from 'qrcode';
import qrcodeTerminal from 'qrcode-terminal';
import fs from 'fs';
import path from 'path';
import http from 'http';
import https from 'https';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = 19846;
const TARGET_PHONE_NUMBER = "6285155133070"; // Format nomor tanpa + atau 0 di depan
const AUTH_DIR = path.join(__dirname, 'auth_info_baileys');
const CONFIG_PATH = path.join(process.env.USERPROFILE || process.env.HOME || '', '.sondercat.json');

// ==================== STATE MANAGEMENT ====================
let sock = null;
let currentQR = null;
let currentPairingCode = null;
let connectionState = 'connecting'; // 'connecting', 'pairing', 'connected', 'disconnected'
let connectedNumber = null;
let autoReplyEnabled = true;
let isPairingRequested = false;
let recentChats = []; // Log riwayat chat masuk & balasan
const pausedUsers = new Map(); // User yang sedang di-handle manual oleh Owner

// ==================== LOAD KNOWLEDGE BASE ====================
let handbookContext = "";
const handbookPath = path.join(__dirname, '..', 'ai_office', 'data', 'documents.json');
try {
    if (fs.existsSync(handbookPath)) {
        const docs = JSON.parse(fs.readFileSync(handbookPath, 'utf-8'));
        const hb = docs.find(d => d.id === 'sample-handbook');
        if (hb) handbookContext = hb.content;
    }
} catch (e) {
    console.error("Gagal membaca handbook:", e.message);
}

// Tambahkan informasi Bit & Bean jika belum ada di handbook
if (!handbookContext.includes("Bit & Bean") && !handbookContext.includes("Bit and Bean")) {
    handbookContext += `\n
---

## 4. Unit Usaha III: Bit & Bean (Coffee & Roastery) ☕
Usaha kopi perpaduan dunia IT ("Bit") dan kenikmatan kopi ("Bean") yang menghadirkan kopi berkualitas untuk menemani ngoding, nugas, kerja santai, maupun nongkrong:
- **Produk & Menu Utama**:
  * **Kopi Susu Bit & Bean** (Gula Aren / Creamy / Vanilla / Caramel) — Favorit teman ngoding & nugas.
  * **Espresso Based**: Espresso, Americano / Long Black, Cafe Latte, Cappuccino.
  * **Manual Brew**: Single Origin pilihan (V60, Aeropress, Japanese Drip).
  * **Non-Coffee**: Matcha Latte, Cokelat Klasik, Red Velvet, Artisan Tea.
  * **Kopi Susu Literan (1 Liter)**: Botol siap simpan di kulkas untuk stok beberapa hari.
  * **Biji Kopi (Whole Beans) & Bubuk Siap Seduh**: Pilihan roasting segar untuk anak kost, rumahan, dan kantor.
- **Layanan Acara & Kemitraan**:
  * Melayani pemesanan botol / cup untuk seminar kampus, workshop IT, rapat kantor, dan katering acara.
- **Pemesanan**: Bisa pesan langsung melalui chat WhatsApp resmi ini (**0851-5513-3070**).
`;
}

// ==================== BANSOS ROUTER CALL ====================
function getAIConfig() {
    let baseUrl = "https://noranisa-bansos.hf.space/v1";
    let apiKey = "bansos";
    let model = "ling-3.0-flash-fin-free";
    try {
        if (fs.existsSync(CONFIG_PATH)) {
            const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
            const g = cfg.global || {};
            if (g.router_base_url) baseUrl = g.router_base_url.replace(/\/+$/, '');
            if (g.router_key) apiKey = g.router_key;
            if (g.router_model) model = g.router_model;
        }
    } catch (e) {}
    return { baseUrl, apiKey, model };
}

async function callBansosAI(senderName, userMessage, conversationHistory = []) {
    const aiConfig = getAIConfig();
    const systemPrompt = `
Anda adalah Nadia, admin / customer service manusiawi di WhatsApp (+62 851-5513-3070) untuk Ir. Nor Anisa, S.Kom., M.Kom. (Noura Studio).

PENGETAHUAN LAYANAN KAMI:
1. REFILL GAS PORTABLE & CANISTER KALIMANTAN: Rp 12.000 / botol bawa sendiri.
   - Banjarmasin: Komplek The Green Rahayu 2 Blok A No. 15, Jln. Simpang Limau | Jam Buka: Senin - Jumat jam 17.00 - 21.00 WITA (5 sore - 9 malam), Sabtu - Minggu jam 08.00 - 21.00 WITA (8 pagi - 9 malam) | WA Cabang: 0851-5513-3070 | Maps: https://maps.app.goo.gl/XpGwbcBdSgavG6XA9
   - Palangka Raya: Toko Karya Perdana, Jl. Seth Adji No. 70 samping H. Kadap | Jam Buka: 07.00 - 11.00 siang, istirahat/ishoma, buka kembali 14.00 - 16.00 sore | WA Cabang: 0812-5090-197 | Maps: https://maps.app.goo.gl/5mXcbhgjDztzZLe27 — Tersedia juga kaleng baru Rp 20.000.
   - Balikpapan: Jln. Mulawarman RT 03 No. 16, Lamaru dekat Masjid Nurul Iman | WA Cabang: 0878-7246-2520 | Maps: https://maps.app.goo.gl/gHZk2yU1qHqu3x1M6
2. BIMBINGAN & KONSULTASI SKRIPSI IT: Dibimbing langsung oleh akademisi Ir. Nor Anisa, S.Kom., M.Kom. (Laravel, React, Next.js, Python, ML, Mobile App). Garansi pendampingan sampai disetujui dosen, Turnitin <15%, jasa print HVS (BW Rp 400, Warna Rp 800). DILARANG KERAS menggunakan kata 'joki'.
3. BIT & BEAN COFFEE ☕: Kopi susu aren asli ramah lambung teman ngoding & nugas, ada botol literan (1 Liter) pas stok kulkas, biji kopi sangrai, dan pesanan acara seminar.

ATURAN WAJIB AGAR 100% TERASA SEPERTI MANUSIA ASLI (BUKAN BOT):
- TULIS CHAT PENDEK, SANTAI & ALAMI: Maksimal 2 sampai 4 kalimat saja! Seperti admin wanita ramah yang mengetik santai lewat keyboard HP.
- JANGAN PERNAH membuat daftar bernomor (1, 2, 3...) yang panjang seperti brosur robot!
- JAWAB HANYA APA YANG DITANYAKAN:
  * Jika tanya Gas / Cabang: Jawab soal gas saja! Berikan alamat, jam buka operasional, nomor WA cabang terkait, dan link Google Maps. Khusus Banjarmasin sebutkan jam bukanya (Senin-Jumat 17.00-21.00 WITA, Sabtu-Minggu 08.00-21.00 WITA). Khusus Palangka Raya sebutkan jam bukanya (07.00-11.00 siang, istirahat/ishoma, dan 14.00-16.00 sore) serta WA 0812-5090-197. JANGAN sebut skripsi atau kopi.
  * Jika tanya Skripsi: Jawab soal bimbingan skripsi saja! Semangati mereka dengan hangat.
  * Jika tanya Kopi: Jawab soal kopi saja!
  * Jika baru menyapa umum ("Halo / Pagi / Permisi"): Balas singkat & ramah: "Halo Kak ${senderName || ''}! Selamat pagi/siang yaa 😊 Ada yang bisa Nadia bantu?" (JANGAN langsung kirim brosur 3 bisnis!).
- BAHASA LUWES & AKRAB: Gunakan partikel wajar ("Iyaa kak", "bisa banget yaa", "ready kok kak", "mau ambil di cabang mana nih?").
- DILARANG menggunakan kata 'joki' atau 'joki skripsi'.
- DILARANG membahas uji rendam air atau timbangan digital.
- Nama pengirim yang disapa: ${senderName || 'Kak'}.
`.trim();

    const messages = [
        { role: "system", content: systemPrompt }
    ];

    if (conversationHistory.length > 0) {
        for (const m of conversationHistory.slice(-4)) {
            messages.push({
                role: m.isAi ? "assistant" : "user",
                content: m.text
            });
        }
    }

    messages.push({ role: "user", content: userMessage });

    try {
        const payload = JSON.stringify({
            model: aiConfig.model,
            messages: messages,
            temperature: 0.7,
            max_tokens: 250
        });

        const url = new URL(`${aiConfig.baseUrl}/chat/completions`);
        const options = {
            hostname: url.hostname,
            port: url.port || (url.protocol === 'https:' ? 443 : 80),
            path: url.pathname + url.search,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${aiConfig.apiKey}`,
                'User-Agent': 'SondeR-WhatsApp-Bot/1.0',
                'Content-Length': Buffer.byteLength(payload)
            }
        };

        const protocol = url.protocol === 'https:' ? https : http;

        return new Promise((resolve) => {
            const req = protocol.request(options, (res) => {
                let data = '';
                res.on('data', (chunk) => data += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        const reply = json.choices?.[0]?.message?.content || "";
                        resolve(reply.trim());
                    } catch (err) {
                        resolve(null);
                    }
                });
            });
            req.on('error', () => resolve(null));
            req.setTimeout(25000, () => {
                req.destroy();
                resolve(null);
            });
            req.write(payload);
            req.end();
        });
    } catch (e) {
        console.error("Error callBansosAI:", e.message);
        return null;
    }
}

// Notifikasi ke SondeR Cat Desktop Pet (Michan) jika aktif
function notifyDesktopPet(text) {
    try {
        const payload = JSON.stringify({ message: text, sender: "WhatsApp Bot" });
        const req = http.request({
            hostname: '127.0.0.1',
            port: 19842,
            path: '/webhook',
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
        }, () => {});
        req.on('error', () => {});
        req.write(payload);
        req.end();
    } catch (e) {}
}

// ==================== BAILEYS WHATSAPP CLIENT ====================
async function connectToWhatsApp() {
    connectionState = 'connecting';
    const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
    const { version } = await fetchLatestBaileysVersion();

    sock = makeWASocket({
        version,
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
        auth: state,
        browser: Browsers.ubuntu("Chrome"),
        syncFullHistory: false
    });

    // PENTING: Hanya minta pairing code jika BELUM terdaftar dan BELUM pernah di-pair
    const hasExistingSession = Boolean(state.creds?.me?.id || state.creds?.registered);

    if (!hasExistingSession && !isPairingRequested) {
        connectionState = 'pairing';
        isPairingRequested = true;
        console.log(`[WhatsApp] Menyiapkan Pairing Code untuk nomor: ${TARGET_PHONE_NUMBER}...`);
        setTimeout(async () => {
            try {
                if (sock && !sock.authState.creds.me && !sock.authState.creds.registered) {
                    const code = await sock.requestPairingCode(TARGET_PHONE_NUMBER);
                    currentPairingCode = code;
                    console.log(`\n======================================================`);
                    console.log(`  📱 KODE TAUTKAN WHATSAPP (PAIRING CODE): ${code}`);
                    console.log(`======================================================`);
                    console.log(`Buka WhatsApp di HP Anda (Nomor: 0851-5513-3070):`);
                    console.log(`1. Buka Pengaturan > Perangkat Tertaut > Tautkan Perangkat`);
                    console.log(`2. Pilih 'Tautkan dengan nomor telepon saja'`);
                    console.log(`3. Masukkan kode di atas: ${code}\n`);
                }
            } catch (err) {
                console.error("[WhatsApp] Gagal request pairing code:", err.message);
                isPairingRequested = false;
            }
        }, 3000);
    } else if (hasExistingSession) {
        console.log(`[WhatsApp] Sesi tersimpan ditemukan untuk ${state.creds.me?.id || TARGET_PHONE_NUMBER}. Menyambungkan ulang...`);
        connectionState = 'connecting';
    }

    sock.ev.on('creds.update', (creds) => {
        saveCreds();
        if (creds.me) {
            connectedNumber = creds.me.id ? creds.me.id.split(':')[0] : TARGET_PHONE_NUMBER;
            console.log(`[WhatsApp] Kredensial akun diterima: +${connectedNumber}`);
        }
    });

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr && !hasExistingSession && !currentPairingCode) {
            currentQR = qr;
            console.log("[WhatsApp] QR Code tersedia (bisa di-scan di http://127.0.0.1:19846)");
            try {
                qrcodeTerminal.generate(qr, { small: true });
            } catch (e) {}
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            console.log(`[WhatsApp] Status koneksi: Ditutup (Code: ${statusCode}). Reconnecting: ${shouldReconnect}`);

            // Jika error adalah restart required (515), jangan reset pairing code!
            if (statusCode === DisconnectReason.loggedOut) {
                console.log("[WhatsApp] Perangkat di-logout dari HP. Mereset sesi...");
                connectionState = 'disconnected';
                currentQR = null;
                currentPairingCode = null;
                isPairingRequested = false;
                try {
                    fs.rmSync(AUTH_DIR, { recursive: true, force: true });
                } catch (e) {}
                setTimeout(connectToWhatsApp, 2000);
            } else if (shouldReconnect) {
                // Koneksi biasa terputus / restart required saat handshake selesai
                connectionState = 'connecting';
                setTimeout(connectToWhatsApp, 2500);
            }
        } else if (connection === 'open') {
            connectionState = 'connected';
            currentQR = null;
            currentPairingCode = null;
            isPairingRequested = false;
            connectedNumber = sock.user?.id ? sock.user.id.split(':')[0] : TARGET_PHONE_NUMBER;
            console.log(`\n======================================================`);
            console.log(`  ✅ [WhatsApp] RESMI TERHUBUNG! Nomor: +${connectedNumber}`);
            console.log(`  🤖 AI Nadia Humanis aktif melayani 3 Usaha:`);
            console.log(`     1. Refill Gas Portable Kalimantan`);
            console.log(`     2. Bimbingan & Konsultasi Skripsi IT`);
            console.log(`     3. Bit & Bean Coffee ☕`);
            console.log(`======================================================\n`);
            notifyDesktopPet(`WhatsApp Terhubung! (+${connectedNumber}) - AI Nadia siap melayani 3 usaha Anda!`);
        }
    });

    // Handle Pesan Masuk
    sock.ev.on('messages.upsert', async (m) => {
        if (m.type !== 'notify') return;

        for (const msg of m.messages) {
            if (msg.key.fromMe) continue;
            if (msg.key.remoteJid === 'status@broadcast') continue;
            if (msg.key.remoteJid.endsWith('@g.us')) continue; // Khusus chat pribadi / CS

            const fromJid = msg.key.remoteJid;
            const senderNumber = fromJid.split('@')[0];
            const senderName = msg.pushName || "Kak";

            let userText = "";
            if (msg.message?.conversation) {
                userText = msg.message.conversation;
            } else if (msg.message?.extendedTextMessage?.text) {
                userText = msg.message.extendedTextMessage.text;
            } else if (msg.message?.imageMessage?.caption) {
                userText = msg.message.imageMessage.caption;
            }

            userText = (userText || "").trim();
            if (!userText) continue;

            console.log(`\n📩 [WA Masuk] Dari: ${senderName} (+${senderNumber}): "${userText}"`);

            const logItem = {
                id: msg.key.id,
                time: new Date().toLocaleTimeString('id-ID'),
                sender: senderName,
                number: senderNumber,
                text: userText,
                reply: "Memproses AI...",
                status: "processing"
            };
            recentChats.unshift(logItem);
            if (recentChats.length > 50) recentChats.pop();

            notifyDesktopPet(`Chat WA dari ${senderName}: "${userText.slice(0, 45)}..."`);

            if (!autoReplyEnabled) {
                logItem.reply = "[Auto-reply dinonaktifkan oleh Owner]";
                logItem.status = "paused";
                continue;
            }

            // Cek apakah pengirim sedang di-pause untuk penanganan manual oleh Owner
            const now = Date.now();
            if (pausedUsers.has(senderNumber)) {
                const pauseUntil = pausedUsers.get(senderNumber);
                if (now < pauseUntil) {
                    logItem.reply = "[Sedang ditangani manual oleh Kak Nor Anisa]";
                    logItem.status = "human_mode";
                    continue;
                } else {
                    pausedUsers.delete(senderNumber);
                }
            }

            // Cek kata kunci Handover ke Manusia / Bukti Transfer
            const lowerText = userText.toLowerCase();
            const isHandover = lowerText.includes("owner") ||
                               lowerText.includes("kak nor anisa") ||
                               lowerText.includes("kak anisa") ||
                               lowerText.includes("bicara dengan admin") ||
                               lowerText.includes("minta rek") ||
                               lowerText.includes("bukti transfer") ||
                               lowerText.includes("sudah transfer");

            if (isHandover) {
                const handoverReply = `Baik kak ${senderName}! Pesan / bukti dari kakak sudah kami terima dan diteruskan langsung ke *Kak Nor Anisa* ya. Mohon ditunggu sebentar, Kak Nor Anisa akan segera merespons secara personal. Terima kasih banyak! 🙏✨`;
                await sock.sendMessage(fromJid, { text: handoverReply }, { quoted: msg });
                pausedUsers.set(senderNumber, now + (30 * 60 * 1000));
                logItem.reply = handoverReply;
                logItem.status = "handover_to_owner";
                notifyDesktopPet(`⚠️ Perhatian: ${senderName} meminta respon personal / mengirim bukti pembayaran!`);
                continue;
            }

            // Sapaan instan murni agar terasa 100% humanis tanpa jeda & tanpa robot
            const cleanText = lowerText.replace(/[^a-z0-9\s]/g, '').trim();
            const pureGreetings = [
                'halo', 'hallo', 'halo kak', 'halo admin', 'hai', 'hai kak', 'hi', 'hi kak',
                'hey', 'hei', 'p', 'pe', 'siang', 'pagi', 'sore', 'malam',
                'assalamualaikum', 'assalamu alaikum', 'assalamuallaikum', 'tes', 'test', 'spada'
            ];

            const d = new Date();
            const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
            const witaTime = new Date(utc + (3600000 * 8)); // UTC+8 WITA
            const h = witaTime.getHours();
            let waktu = 'siang';
            if (h >= 5 && h < 11) waktu = 'pagi';
            else if (h >= 11 && h < 15) waktu = 'siang';
            else if (h >= 15 && h < 18) waktu = 'sore';
            else waktu = 'malam';

            if (pureGreetings.includes(cleanText)) {
                await sock.sendPresenceUpdate('composing', fromJid);
                const gReply = cleanText.includes('assalam')
                    ? `Wa'alaikumussalam kak ${senderName}! Selamat ${waktu} yaa 😊 Ada yang bisa Nadia bantu?`
                    : `Halo kak ${senderName}! Selamat ${waktu} yaa 😊 Ada yang bisa Nadia bantu hari ini?`;
                await sock.sendMessage(fromJid, { text: gReply }, { quoted: msg });
                await sock.sendPresenceUpdate('paused', fromJid);
                logItem.reply = gReply;
                logItem.status = "replied";
                console.log(`💬 [WA Sapaan Humanis]: "${gReply}" ke ${senderName}`);
                continue;
            }

            // Panggil AI Nadia via Bansos Router
            try {
                await sock.sendPresenceUpdate('composing', fromJid);
                let aiReply = await callBansosAI(senderName, userText);

                if (!aiReply) {
                    aiReply = `Halo kak ${senderName}! Maaf Nadia baru cek yaa. Boleh diinfokan detail kebutuhannya kak? Biar Nadia bantu infokan dengan senang hati 😊🙏`;
                }

                // Kirim balasan ke WhatsApp pelanggan
                await sock.sendMessage(fromJid, { text: aiReply }, { quoted: msg });
                await sock.sendPresenceUpdate('paused', fromJid);

                logItem.reply = aiReply;
                logItem.status = "replied";
                console.log(`🤖 [WA Terkirim ke +${senderNumber}]:\n${aiReply.slice(0, 150)}...\n`);
            } catch (err) {
                console.error("[WhatsApp] Gagal mengirim balasan:", err.message);
                logItem.status = "error";
                logItem.reply = `Error: ${err.message}`;
            }
        }
    });
}

// ==================== EXPRESS DASHBOARD UI ====================
const app = express();
app.use(express.json());

app.get('/api/status', async (req, res) => {
    let qrDataUrl = null;
    if (currentQR) {
        try {
            qrDataUrl = await QRCode.toDataURL(currentQR, { margin: 2, scale: 6 });
        } catch (e) {}
    }

    res.json({
        state: connectionState,
        pairingCode: currentPairingCode,
        qr: qrDataUrl,
        number: connectedNumber || TARGET_PHONE_NUMBER,
        autoReply: autoReplyEnabled,
        recentChats: recentChats.slice(0, 25)
    });
});

app.post('/api/toggle-autoreply', (req, res) => {
    autoReplyEnabled = !autoReplyEnabled;
    res.json({ autoReply: autoReplyEnabled });
});

app.post('/api/reset-session', async (req, res) => {
    try {
        if (sock) {
            await sock.logout();
        }
    } catch (e) {}
    try {
        fs.rmSync(AUTH_DIR, { recursive: true, force: true });
    } catch (e) {}
    currentQR = null;
    currentPairingCode = null;
    isPairingRequested = false;
    connectionState = 'connecting';
    setTimeout(connectToWhatsApp, 1500);
    res.json({ ok: true });
});

// Sajikan dashboard statis dari folder public
app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Jalankan Server Web Dashboard & Baileys
app.listen(PORT, '127.0.0.1', () => {
    console.log(`======================================================`);
    console.log(`  🌐 Dashboard WhatsApp Bridge: http://127.0.0.1:${PORT}`);
    console.log(`======================================================`);
    connectToWhatsApp();
});
