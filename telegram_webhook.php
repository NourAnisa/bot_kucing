<?php
/**
 * SondeR Cloud Telegram Bot Webhook (@noranisa_bot)
 * Melayani 3 Unit Usaha Nor Anisa 24 Jam Nonstop di Server Cloud (Tanpa Laptop Nyala):
 * 1. Refill Gas Portable Kalimantan (Rp 12.000)
 * 2. Bimbingan & Konsultasi IT & Akademik Master (Garansi Bebas Revisi, Skripsi, Print HVS)
 * 3. Bit & Bean Coffee & Roastery ☕
 * Ditenagai Hugging Face Bansos Router (ling-3.0-flash-fin-free)
 */

header('Content-Type: application/json');

$BOT_TOKEN = "8664429930:AAGCvxMhh50wVBmHzZm48QA_L40wrt6rcx0";
$TELEGRAM_API = "https://api.telegram.org/bot" . $BOT_TOKEN;
$BANSOS_API = "https://noranisa-bansos.hf.space/v1/chat/completions";
$BANSOS_KEY = "bansos";
$BANSOS_MODEL = "ling-3.0-flash-fin-free";

// Tangkap input dari webhook Telegram
$rawInput = file_get_contents('php://input');
if (empty($rawInput)) {
    echo json_encode(["status" => "online", "bot" => "@noranisa_bot", "server" => "LiteSpeed Cloud"]);
    exit;
}

$update = json_decode($rawInput, true);
if (!isset($update['message'])) {
    echo json_encode(["ok" => true]);
    exit;
}

$msg = $update['message'];
$chatId = $msg['chat']['id'] ?? null;
$senderName = $msg['from']['first_name'] ?? 'Kak';
$userText = trim($msg['text'] ?? '');

if (!$chatId || empty($userText)) {
    echo json_encode(["ok" => true]);
    exit;
}

// Helper kirim pesan ke Telegram
function sendTelegramReply($chatId, $text, $token) {
    $url = "https://api.telegram.org/bot" . $token . "/sendMessage";
    $payload = json_encode([
        'chat_id' => $chatId,
        'text' => $text,
        'parse_mode' => 'Markdown'
    ]);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}

// Log aktivitas chat ke file JSON di hosting
function logCloudChat($senderName, $chatId, $userText, $replyText) {
    $logFile = __DIR__ . '/telegram_cloud_chats.json';
    $logs = [];
    if (file_exists($logFile)) {
        $logs = json_decode(file_get_contents($logFile), true) ?: [];
    }
    array_unshift($logs, [
        'time' => date('Y-m-d H:i:s'),
        'sender' => $senderName,
        'chat_id' => $chatId,
        'text' => $userText,
        'reply' => $replyText
    ]);
    if (count($logs) > 100) $logs = array_slice($logs, 0, 100);
    file_put_contents($logFile, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

// Panggil Hugging Face Bansos AI
function callBansosCloudAI($senderName, $userMessage, $apiUrl, $apiKey, $model) {
    $systemPrompt = "Anda adalah Nadia, admin / customer service manusiawi di WhatsApp & Telegram untuk Ir. Nor Anisa, S.Kom., M.Kom. (Noura Studio).\n\n"
        . "PENGETAHUAN LAYANAN:\n"
        . "- REFILL GAS KALIMANTAN: Rp 12.000/botol bawa sendiri (Banjarmasin di The Green Rahayu 2, Palangka Raya di Toko Karya Perdana Jl. Seth Adji [ada tabung baru Rp 20rb], Balikpapan di Lamaru). Siap setiap hari.\n"
        . "- BIMBINGAN SKRIPSI IT: Dibimbing langsung akademisi (Laravel, React, Next.js, Python, ML, Flutter). Garansi pendampingan sampai disetujui dosen, Turnitin <15%, print HVS (BW Rp 400, Warna Rp 800). DILARANG menyebut kata 'joki'.\n"
        . "- BIT & BEAN COFFEE: Kopi susu aren asli ramah lambung teman ngoding, ada botol 1 Liter stok kulkas, biji kopi & pesanan acara.\n\n"
        . "ATURAN WAJIB AGAR TIDAK TERLIHAT SEPERTI BOT (100% GAYA MANUSIA):\n"
        . "1. TULIS CHAT PENDEK & ALAMI: Maksimal 2 sampai 4 kalimat saja! Seperti admin cewek ramah yang mengetik santai dari HP. JANGAN PERNAH membuat daftar bernomor (1, 2, 3...) yang panjang.\n"
        . "2. FOKUS HANYA PADA YANG DITANYAKAN: Jika tanya gas, jawab soal gas saja (JANGAN sebut skripsi/kopi). Jika tanya skripsi, jawab skripsi saja. Jika tanya kopi, jawab kopi saja.\n"
        . "3. JIKA HANYA MENYAPA: Balas dengan ramah dan singkat: 'Halo Kak " . $senderName . "! Selamat pagi/siang yaa 😊 Ada yang bisa dibantu?' (JANGAN kirim penjelasan bisnis panjang).\n"
        . "4. BAHASA LUWES & HANGAT: Gunakan partikel chat wajar ('Iyaa kak', 'bisa banget yaa', 'ready kok kak', 'mau ambil di cabang mana nih?').\n"
        . "5. DILARANG KERAS kata 'joki' atau 'joki skripsi'. DILARANG bahas uji rendam air atau timbangan digital.\n";

    $payload = json_encode([
        'model' => $model,
        'messages' => [
            ['role' => 'system', 'content' => $systemPrompt],
            ['role' => 'user', 'content' => $userMessage]
        ],
        'temperature' => 0.7,
        'max_tokens' => 250
    ]);

    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $apiKey,
        'User-Agent: SondeR-CloudTelegramBot/1.0'
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    $response = curl_exec($ch);
    curl_close($ch);

    if ($response) {
        $data = json_decode($response, true);
        return $data['choices'][0]['message']['content'] ?? null;
    }
    return null;
}

$lower = strtolower($userText);

// 1. Command /start & /help
if ($lower === '/start' || $lower === '/help' || $lower === 'halo' || $lower === 'hai') {
    $reply = "👋 *Halo Kak {$senderName}! Selamat datang di Bot Resmi Ekosistem Bisnis Noura Studio (@noranisa_bot)* ✨\n\n"
        . "Pimpinan & Founder: *Ir. Nor Anisa, S.Kom., M.Kom.* (Dosen Informatika & Insinyur Profesional)\n"
        . "🌐 Website: https://nourastudio.co-id.id\n"
        . "📱 WhatsApp CS 24 Jam: 0851-5513-3070\n\n"
        . "Kami melayani 3 Unit Usaha Terpadu:\n"
        . "1️⃣ 🔥 *Refill Gas Portable Kalimantan* (Rp 12.000/botol bawa sendiri)\n"
        . "2️⃣ 💻 *Bimbingan & Konsultasi IT & Akademik Master* (100% garansi bebas revisi, skripsi, print HVS)\n"
        . "3️⃣ ☕ *Bit & Bean Coffee* (Kopi aren, literan 1L, roasted beans)\n\n"
        . "📌 *Perintah Cepat:*\n"
        . "• `/gas` — Cek harga & 3 cabang refill gas portable\n"
        . "• `/joki` — Layanan pengerjaan skripsi & ngoding tugas\n"
        . "• `/kopi` — Menu kopi Bit & Bean\n"
        . "• `/promo` — Cek 3 promo & penawaran eksklusif bulan ini\n"
        . "• Atau silakan langsung ketik pertanyaan kakak di sini, AI Nadia siap melayani 24 Jam Nonstop! 😊";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// Command /promo
if ($lower === '/promo' || $lower === 'promo') {
    $reply = "🎁 *PROMO & PENAWARAN EKSKLUSIF BULAN INI*\n\n"
        . "1️⃣ ☕💻 *Paket Koding + Kopi Literan (1L)*\n"
        . "Pesan joki coding / skripsi, GRATIS 1 Botol Kopi Susu Aren Bit & Bean (1.000ml) untuk teman nugas!\n\n"
        . "2️⃣ 🔥🏕️ *Refill 5 Botol Gas Rp 55.000 (Hemat Borongan)*\n"
        . "Bawa 5 botol portable/canister sekaligus cuma Rp 55.000 (hemat Rp 5.000). Berlaku di 3 cabang.\n\n"
        . "3️⃣ 🎓📜 *Paket Wisuda Kilat All-in-One*\n"
        . "Aplikasi skripsi + bimbingan bab 1-5 + sertifikat Turnitin <15% + cetak HVS rapi.\n\n"
        . "📲 Hubungi WhatsApp CS untuk klaim promo: *0851-5513-3070* ✨";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// 2. Command /gas
if ($lower === '/gas') {
    $reply = "🔥 *Refill Gas Portable & Canister Kalimantan*\n\n"
        . "💰 *Tarif Resmi:* Rp 12.000 / botol (botol kosong bawa sendiri)\n"
        . "🏪 *Gas Baru Segel Pabrik:* Rp 20.000 (tersedia di Cabang Palangka Raya)\n\n"
        . "📍 *3 Cabang Resmi Kami:*\n"
        . "1. *Banjarmasin*: Jln. Simpang Limau, Komplek The Green Rahayu 2 Blok A No. 15\n"
        . "   🗺️ Maps: https://maps.app.goo.gl/XpGwbcBdSgavG6XA9\n"
        . "2. *Palangka Raya*: Toko Karya Perdana, Jl. Seth Adji No. 70 Samping H. Kadap\n"
        . "   🗺️ Maps: https://maps.app.goo.gl/5mXcbhgjDztzZLe27\n"
        . "3. *Balikpapan*: Jln. Mulawarman RT 03 No. 16, Lamaru (Dekat Masjid Nurul Iman)\n"
        . "   🗺️ Maps: https://maps.app.goo.gl/gHZk2yU1qHqu3x1M6\n\n"
        . "📞 Hubungi WhatsApp: *0851-5513-3070* 🙏";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// 3. Command /joki
if ($lower === '/joki') {
    $reply = "💻 *Bimbingan & Konsultasi IT & Akademik Master*\n"
        . "🌐 Portal: https://bimbingan IT.vercel.app/\n\n"
        . "✅ *Layanan Kami:*\n"
        . "• Jasa Ngoding: Laravel, React, Next.js, Python, Java, Mobile App, AI\n"
        . "• Skripsi TI / Sistem Informasi: Proposal, Bab 1-5, Program Web/Mobile, Jurnal SINTA\n"
        . "• Cetak/Print HVS: Hitam-Putih Rp 400,- | Warna Rp 800,-\n\n"
        . "🌟 *4 Keunggulan Utama:*\n"
        . "1. 100% Garansi Bebas Revisi sampai acc/lulus\n"
        . "2. 100% Kerahasiaan data terjaga rapi\n"
        . "3. Express 24 Jam tersedia untuk deadline mendesak\n"
        . "4. Original & lolos uji Turnitin";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// 4. Command /kopi
if ($lower === '/kopi') {
    $reply = "☕ *Bit & Bean (Coffee & Roastery)*\n\n"
        . "Kopi berkualitas perpaduan dunia IT ('Bit') dan kenikmatan kopi ('Bean'):\n"
        . "• *Kopi Susu Aren* — Favorit teman ngoding & nugas\n"
        . "• *Espresso Based* — Americano, Latte, Cappuccino\n"
        . "• *Manual Brew* — Single Origin pilihan V60 & Japanese Drip\n"
        . "• *Kopi Susu Literan (1 Liter)* — Botol siap stok kulkas\n"
        . "• *Roasted Beans & Bubuk* — Siap seduh segar untuk anak kost & kantor\n\n"
        . "Pemesanan langsung via WA: *0851-5513-3070* ☕✨";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// 5. Cek Bukti Transfer / Handover ke Owner
$isHandover = (
    strpos($lower, 'owner') !== false ||
    strpos($lower, 'anisa') !== false ||
    strpos($lower, 'transfer') !== false ||
    strpos($lower, 'bukti') !== false ||
    strpos($lower, 'rekening') !== false ||
    strpos($lower, 'sudah bayar') !== false
);

if ($isHandover) {
    $reply = "Baik Kak {$senderName}! Bukti transfer / permohonan dari kakak sudah kami terima di sistem cloud dan diteruskan langsung ke *Ibu Ir. Nor Anisa, S.Kom., M.Kom.* ya. Mohon ditunggu sebentar, Ibu Ir. Nor Anisa akan segera merespons secara personal. Terima kasih banyak! 🙏✨";
    sendTelegramReply($chatId, $reply, $BOT_TOKEN);
    logCloudChat($senderName, $chatId, $userText, $reply);
    echo json_encode(["ok" => true]);
    exit;
}

// 6. AI Conversation via Hugging Face Bansos
$aiReply = callBansosCloudAI($senderName, $userText, $BANSOS_API, $BANSOS_KEY, $BANSOS_MODEL);
if (!$aiReply) {
    $aiReply = "Halo Kak {$senderName}! Terima kasih sudah menghubungi layanan kami. Pesan kakak sudah kami terima di sistem cloud 24 jam dan akan segera kami proses ya! 🙏";
}

sendTelegramReply($chatId, $aiReply, $BOT_TOKEN);
logCloudChat($senderName, $chatId, $userText, $aiReply);

echo json_encode(["ok" => true]);
