# -*- coding: utf-8 -*-
"""
SondeR AI Office - Telegram Bot Service (@noranisa_bot)
Melayani 3 Unit Usaha Nor Anisa:
1. Refill Gas Portable & Canister Kalimantan (Rp 12.000)
2. JokiCoding & Akademik Master (Garansi revisi, Skripsi, Print HVS)
3. Bit & Bean Coffee & Roastery ☕
Ditenagai Hugging Face Bansos Router (ling-3.0-flash-fin-free)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TELEGRAM_LOG_FILE = DATA_DIR / "telegram_chats.json"
CONFIG_PATH = Path(os.path.expanduser("~/.sondercat.json"))
TELEGRAM_CONFIG_FILE = DATA_DIR / "telegram_config.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = "8664429930:AAGCvxMhh50wVBmHzZm48QA_L40wrt6rcx0"
BOT_USERNAME = "noranisa_bot"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Simpan token & konfigurasi bot
telegram_config = {
    "token": BOT_TOKEN,
    "username": BOT_USERNAME,
    "configured": True,
    "paired": True,
    "connected": True,
    "registeredAt": int(time.time() * 1000)
}
with open(TELEGRAM_CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(telegram_config, f, indent=2)

# ----------------- HUGGING FACE BANSOS AI CLIENT -----------------

def get_ai_config():
    base_url = "https://noranisa-bansos.hf.space/v1"
    api_key = "bansos"
    model = "ling-3.0-flash-fin-free"
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f).get("global", {})
                if cfg.get("router_base_url"):
                    base_url = cfg["router_base_url"].rstrip("/")
                if cfg.get("router_key"):
                    api_key = cfg["router_key"]
                if cfg.get("router_model"):
                    model = cfg["router_model"]
    except Exception:
        pass
    return {"base_url": base_url, "api_key": api_key, "model": model}

def call_bansos_ai(user_name, user_message):
    ai_cfg = get_ai_config()
    system_prompt = f"""
Nama Anda adalah Nadia, Asisten Layanan & Customer Service Ekosistem Bisnis Nor Anisa di Telegram (@noranisa_bot).
Pimpinan & Founder: Ir. Nor Anisa, S.Kom., M.Kom.

Nomor WhatsApp Resmi CS Terpadu: +62 851-5513-3070
Website Resmi: https://nourastudio.co-id.id

Anda melayani 3 UNIT USAHA UTAMA:
1. REFILL GAS PORTABLE & CANISTER KALIMANTAN (Rp 12.000 / botol bawa sendiri)
   - 📍 Cabang Banjarmasin: Jln. Simpang Limau, Komplek The Green Rahayu 2 Blok A No. 15 (Maps: https://maps.app.goo.gl/XpGwbcBdSgavG6XA9)
   - 📍 Cabang Palangka Raya: Toko Karya Perdana, Jl. Seth Adji No. 70 Samping H. Kadap (Maps: https://maps.app.goo.gl/5mXcbhgjDztzZLe27) — Tersedia gas kaleng baru Rp 20.000
   - 📍 Cabang Balikpapan: Jln. Mulawarman RT 03 No. 16, Lamaru (Maps: https://maps.app.goo.gl/gHZk2yU1qHqu3x1M6)
2. JOKICODING & AKADEMIK MASTER (https://jokicoding.vercel.app/)
   - Pengerjaan skripsi/tugas programming: Next.js, React, Laravel, PHP, Python, Java, Mobile App
   - 100% GARANSI BEBAS REVISI, Kerahasiaan Terjamin, Turnitin-ready
   - Jasa Print Dokumen HVS: Hitam-Putih Rp 400/lembar, Warna Rp 800/lembar
3. BIT & BEAN (Coffee & Roastery ☕)
   - Kopi Susu Aren teman nugas/ngoding, espresso based, manual brew
   - Kopi Susu Literan (1 Liter) botol siap stok kulkas, roasted beans & bubuk segar

ATURAN KOMUNIKASI:
- JANGAN PERNAH menyebutkan atau membahas SOP keselamatan uji rendam air atau timbangan digital.
- Jawab dalam Bahasa Indonesia yang ramah, santun, hangat, dan sangat membantu.
- Gunakan emoji secukupnya agar chat terasa hidup (😊, ☕, 🔥, 💻, ✨, 🙏).
- Nama pengguna: {user_name or 'Kak'}.
""".strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        payload = json.dumps({
            "model": ai_cfg["model"],
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{ai_cfg['base_url']}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ai_cfg['api_key']}",
                "User-Agent": "SondeR-TelegramBot/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[!] Gagal panggil Bansos AI untuk Telegram: {e}")
        return None

# ----------------- TELEGRAM API HELPERS -----------------

def send_telegram_message(chat_id, text, parse_mode="Markdown"):
    try:
        payload = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{API_URL}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        # Fallback tanpa parse_mode jika ada karakter format markdown tidak valid
        try:
            payload = json.dumps({
                "chat_id": chat_id,
                "text": text
            }).encode("utf-8")
            req = urllib.request.Request(f"{API_URL}/sendMessage", data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e2:
            print(f"[!] Gagal kirim pesan Telegram ke {chat_id}: {e2}")
            return None

def log_telegram_chat(chat_id, sender_name, user_text, bot_reply, status="replied"):
    log_item = {
        "id": f"tg-{int(time.time()*1000)}",
        "time": time.strftime("%H:%M"),
        "date": time.strftime("%Y-%m-%d"),
        "sender": sender_name,
        "chat_id": str(chat_id),
        "text": user_text,
        "reply": bot_reply,
        "status": status
    }
    
    logs = []
    if TELEGRAM_LOG_FILE.exists():
        try:
            with open(TELEGRAM_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
            
    logs.insert(0, log_item)
    if len(logs) > 100:
        logs = logs[:100]
        
    try:
        with open(TELEGRAM_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def notify_michan(text):
    try:
        payload = json.dumps({"message": text, "sender": "Telegram Bot"}).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:19842/webhook", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=2)
    except Exception:
        pass

# ----------------- MESSAGE PROCESSOR -----------------

def handle_telegram_message(message):
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    sender = message.get("from", {})
    sender_name = sender.get("first_name", "Kak")
    text = message.get("text", "").strip()

    if not text or not chat_id:
        return

    print(f"\n💬 [Telegram Masuk] Dari {sender_name} (ID: {chat_id}): \"{text}\"")
    notify_michan(f"Telegram dari {sender_name}: \"{text[:40]}...\"")

    lower = text.lower()

    # 1. Command: /start atau /help
    if lower in ("/start", "/help", "halo", "hai"):
        reply = (
            f"👋 *Halo Kak {sender_name}! Selamat datang di Bot Resmi Ekosistem Bisnis Nor Anisa (@{BOT_USERNAME})* ✨\n\n"
            f"Pimpinan: *Ir. Nor Anisa, S.Kom., M.Kom.*\n"
            f"🌐 Website: https://nourastudio.co-id.id\n"
            f"📱 WhatsApp CS 24 Jam: 0851-5513-3070\n\n"
            f"Kami melayani 3 Unit Usaha Terpadu:\n"
            f"1️⃣ 🔥 *Refill Gas Portable Kalimantan* (Rp 12.000/botol bawa sendiri)\n"
            f"2️⃣ 💻 *JokiCoding & Akademik Master* (100% garansi bebas revisi, skripsi, print HVS)\n"
            f"3️⃣ ☕ *Bit & Bean Coffee* (Kopi aren, literan 1L, roasted beans)\n\n"
            f"📌 *Perintah Cepat:*\n"
            f"• `/gas` — Cek harga & 3 cabang refill gas portable\n"
            f"• `/joki` — Layanan pengerjaan skripsi & ngoding tugas\n"
            f"• `/kopi` — Menu kopi Bit & Bean\n"
            f"• `/laporan` — Cek Ringkasan Laporan Pagi Bisnis Hari Ini\n"
            f"• Atau silakan langsung ketik pertanyaan kakak di sini, AI Nadia siap membantu! 😊"
        )
        send_telegram_message(chat_id, reply)
        log_telegram_chat(chat_id, sender_name, text, reply, "welcome")
        return

    # 2. Command: /gas
    if lower == "/gas":
        reply = (
            f"🔥 *Refill Gas Portable & Canister Kalimantan*\n\n"
            f"💰 *Tarif Resmi:* Rp 12.000 / botol (botol kosong bawa sendiri)\n"
            f"🏪 *Gas Baru Segel Pabrik:* Rp 20.000 (tersedia di Cabang Palangka Raya)\n\n"
            f"📍 *3 Cabang Resmi Kami:*\n"
            f"1. *Banjarmasin*: Jln. Simpang Limau, Komplek The Green Rahayu 2 Blok A No. 15\n"
            f"   🗺️ Maps: https://maps.app.goo.gl/XpGwbcBdSgavG6XA9\n"
            f"2. *Palangka Raya*: Toko Karya Perdana, Jl. Seth Adji No. 70 Samping H. Kadap\n"
            f"   🗺️ Maps: https://maps.app.goo.gl/5mXcbhgjDztzZLe27\n"
            f"3. *Balikpapan*: Jln. Mulawarman RT 03 No. 16, Lamaru (Dekat Masjid Nurul Iman)\n"
            f"   🗺️ Maps: https://maps.app.goo.gl/gHZk2yU1qHqu3x1M6\n\n"
            f"📞 Hubungi kami kapan saja via WhatsApp: *0851-5513-3070* 🙏"
        )
        send_telegram_message(chat_id, reply)
        log_telegram_chat(chat_id, sender_name, text, reply, "info_gas")
        return

    # 3. Command: /joki
    if lower == "/joki":
        reply = (
            f"💻 *JokiCoding & Akademik Master*\n"
            f"🌐 Portal: https://jokicoding.vercel.app/\n\n"
            f"✅ *Layanan Kami:*\n"
            f"• Jasa Ngoding: Laravel, React, Next.js, Python, Java, Mobile App, AI\n"
            f"• Skripsi TI / Sistem Informasi: Proposal, Bab 1-5, Program Web/Mobile, Jurnal SINTA\n"
            f"• Cetak/Print HVS: Hitam-Putih Rp 400,- | Warna Rp 800,-\n\n"
            f"🌟 *4 Keunggulan:*\n"
            f"1. 100% Garansi Bebas Revisi sampai acc/lulus\n"
            f"2. 100% Kerahasiaan data terjaga rapi\n"
            f"3. Express 24 Jam tersedia untuk deadline mepet\n"
            f"4. Original & lolos Turnitin"
        )
        send_telegram_message(chat_id, reply)
        log_telegram_chat(chat_id, sender_name, text, reply, "info_joki")
        return

    # 4. Command: /kopi
    if lower == "/kopi":
        reply = (
            f"☕ *Bit & Bean (Coffee & Roastery)*\n\n"
            f"Kopi berkualitas perpaduan dunia IT ('Bit') dan kenikmatan kopi ('Bean'):\n"
            f"• *Kopi Susu Aren* — Favorit teman ngoding & nugas\n"
            f"• *Espresso Based* — Americano, Latte, Cappuccino\n"
            f"• *Manual Brew* — Single Origin pilihan V60 & Japanese Drip\n"
            f"• *Kopi Susu Literan (1 Liter)* — Botol siap stok kulkas\n"
            f"• *Roasted Beans & Bubuk* — Siap seduh segar untuk anak kost & kantor\n\n"
            f"Pemesanan langsung via WA: *0851-5513-3070* ☕✨"
        )
        send_telegram_message(chat_id, reply)
        log_telegram_chat(chat_id, sender_name, text, reply, "info_coffee")
        return

    # 5. Command: /laporan
    if lower in ("/laporan", "/report", "laporan pagi"):
        reports_dir = DATA_DIR / "reports"
        latest_file = None
        if reports_dir.exists():
            files = sorted(reports_dir.glob("Laporan_Pagi_*.md"), reverse=True)
            if files:
                latest_file = files[0]

        if latest_file:
            with open(latest_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Ringkas laporan untuk Telegram
            summary_msg = f"📊 *LAPORAN EKSEKUTIF BISNIS NOR ANISA*\n\n{content[:3800]}"
            send_telegram_message(chat_id, summary_msg)
            log_telegram_chat(chat_id, sender_name, text, "[Laporan Pagi Terkirim]", "report_sent")
        else:
            send_telegram_message(chat_id, "⚠️ Belum ada file laporan pagi hari ini. Laporan akan di-generate otomatis pukul 07:00 WIB.")
        return

    # 6. Cek Handover ke Owner / Bukti Transfer
    is_handover = any(k in lower for k in ["owner", "anisa", "kak anisa", "minta rek", "rekening", "transfer", "bukti transfer", "sudah bayar"])
    if is_handover:
        handover_reply = (
            f"Baik Kak {sender_name}! Bukti / permohonan dari kakak sudah kami catat dan diteruskan langsung ke *Ibu Ir. Nor Anisa, S.Kom., M.Kom.* ya. "
            f"Mohon ditunggu sebentar, Ibu Nor Anisa akan segera merespons secara personal. Terima kasih banyak! 🙏✨"
        )
        send_telegram_message(chat_id, handover_reply)
        log_telegram_chat(chat_id, sender_name, text, handover_reply, "handover_to_owner")
        notify_michan(f"⚠️ Telegram: {sender_name} mengirim bukti pembayaran / minta bicara personal dengan Kak Nor Anisa!")
        return

    # 7. AI Response via Hugging Face Bansos
    ai_reply = call_bansos_ai(sender_name, text)
    if not ai_reply:
        ai_reply = f"Halo Kak {sender_name}! Terima kasih sudah menghubungi layanan kami. Pesan kakak sudah kami terima dan akan segera kami proses ya! 🙏"

    send_telegram_message(chat_id, ai_reply)
    log_telegram_chat(chat_id, sender_name, text, ai_reply, "replied")
    print(f"🤖 [Telegram Terkirim ke {sender_name}]: \"{ai_reply[:80]}...\"")

# ----------------- LONG POLLING LOOP -----------------

def run_telegram_bot(single_pass=False):
    print("======================================================")
    print(f"  🤖 TELEGRAM BOT SERVICE (@{BOT_USERNAME}) AKTIF")
    print(f"  ⚡ Ditenagai Hugging Face Bansos (ling-3.0-flash-fin-free)")
    print("======================================================")

    offset = 0
    while True:
        try:
            url = f"{API_URL}/getUpdates?offset={offset}&timeout=20"
            req = urllib.request.Request(url, headers={"User-Agent": "SondeR-TelegramBot/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if data.get("ok"):
                updates = data.get("result", [])
                for u in updates:
                    offset = max(offset, u.get("update_id", 0) + 1)
                    if "message" in u:
                        handle_telegram_message(u["message"])

            if single_pass:
                break
        except Exception as e:
            if not single_pass:
                time.sleep(3)
            else:
                break

if __name__ == "__main__":
    is_once = "--once" in sys.argv
    run_telegram_bot(single_pass=is_once)
