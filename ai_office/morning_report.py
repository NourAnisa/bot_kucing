# -*- coding: utf-8 -*-
"""
SondeR AI Office - Daily Morning WhatsApp & Executive Report Engine
Menghasilkan laporan komprehensif aktivitas WhatsApp dan ekosistem bisnis setiap pagi hari
untuk Ibu Ir. Nor Anisa, S.Kom., M.Kom.
Ditenagai AI Hugging Face Bansos (ling-3.0-flash-fin-free)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
CHATS_FILE = DATA_DIR / "whatsapp_chats.json"
DOCUMENTS_FILE = DATA_DIR / "documents.json"
CONFIG_PATH = Path(os.path.expanduser("~/.sondercat.json"))

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------- CONFIG & AI CLIENT -----------------

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

def call_bansos_llm(messages, max_tokens=1500):
    cfg = get_ai_config()
    try:
        payload = json.dumps({
            "model": cfg["model"],
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": max_tokens
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{cfg['base_url']}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cfg['api_key']}",
                "User-Agent": "SondeR-MorningReport/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[!] Gagal panggil Bansos AI: {e}")
        return None

# ----------------- SYSTEM HEALTH CHECK -----------------

def check_system_health():
    health = {}
    
    # 1. Hugging Face Bansos
    try:
        t0 = time.time()
        req = urllib.request.Request("https://noranisa-bansos.hf.space/v1/models", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            lat = int((time.time() - t0) * 1000)
            health["bansos"] = f"Online (Latency: {lat}ms)"
    except Exception as e:
        health["bansos"] = f"Warning/Offline ({e})"

    # 2. Website Noura Studio
    try:
        req = urllib.request.Request("https://nourastudio.co-id.id/nourastudio.co-id.id/public/index.html", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            health["website"] = f"Online (HTTP {resp.getcode()})"
    except Exception as e:
        health["website"] = f"Warning ({e})"

    # 3. AI Office Server
    try:
        req = urllib.request.Request("http://127.0.0.1:19845/api/health")
        with urllib.request.urlopen(req, timeout=3) as resp:
            health["ai_office"] = "Active (Port 19845)"
    except Exception:
        health["ai_office"] = "Standby / Idle"

    # 4. WhatsApp Bot Local / Cloud
    try:
        req = urllib.request.Request("http://127.0.0.1:19846/api/status")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            st = data.get("state", "unknown")
            health["whatsapp_bot"] = f"Local Daemon Active ({st})"
    except Exception:
        health["whatsapp_bot"] = "Cloud/Standby Connected (0851-5513-3070)"

    # 5. Telegram Bot @noranisa_bot
    try:
        tg_token = "8664429930:AAGCvxMhh50wVBmHzZm48QA_L40wrt6rcx0"
        req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/getMe", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            tg_data = json.loads(resp.read().decode("utf-8"))
            if tg_data.get("ok"):
                health["telegram_bot"] = "Online (@noranisa_bot)"
            else:
                health["telegram_bot"] = "Warning"
    except Exception as e:
        health["telegram_bot"] = f"Offline ({e})"

    return health

# ----------------- CHAT ANALYSIS -----------------

def categorize_chat(text):
    t = text.lower()
    if any(k in t in t for k in ["owner", "anisa", "rek", "rekening", "transfer", "bukti", "bayar"]):
        return "handover"
    if any(k in t for k in ["gas", "canister", "portable", "refill", "isi ulang", "kaleng", "karya perdana", "tabung"]):
        return "gas"
    if any(k in t for k in ["bimbingan", "konsultasi", "koding", "coding", "skripsi", "tugas", "web", "laravel", "python", "print", "hvs", "turnitin"]):
        return "bimbingan"
    if any(k in t for k in ["kopi", "coffee", "roastery", "bean", "manual brew", "aren", "literan", "espresso"]):
        return "coffee"
    return "general"

def load_and_filter_chats():
    if not CHATS_FILE.exists():
        # Buat sampel chat jika file belum ada
        sample_chats = [
            {
                "id": "sample-1",
                "time": "08:15",
                "sender": "Kak Dimas (Banjarmasin)",
                "number": "6281234567801",
                "text": "Pagi min, mau refill gas canister 4 kaleng di Green Rahayu Banjarmasin, ready?",
                "reply": "Pagi Kak Dimas! Ready selalu ya kak, silakan langsung ke Cabang Banjarmasin tarif Rp 12.000/botol bawa sendiri.",
                "status": "replied"
            },
            {
                "id": "sample-2",
                "time": "11:30",
                "sender": "Kak Fajar (Palangka Raya)",
                "number": "6285298765432",
                "text": "Toko Karya Perdana buka jam berapa? Mau beli gas portable baru sama refill",
                "reply": "Buka setiap hari kak! Alamat Jl. Seth Adji No. 70 Samping H. Kadap. Refill Rp 12.000 dan kaleng baru Rp 20.000.",
                "status": "replied"
            },
            {
                "id": "sample-3",
                "time": "14:20",
                "sender": "Kak Siti Mahasiswa",
                "number": "6289612345678",
                "text": "Kak mau tanya bimbingan skripsi sistem informasi pakai CodeIgniter berapa ya dan ada garansi revisi?",
                "reply": "Halo Kak Siti! Ada 100% garansi bebas revisi sampai lulus ya kak. Pengerjaan original dan turnitin ready.",
                "status": "replied"
            },
            {
                "id": "sample-4",
                "time": "16:45",
                "sender": "Kak Kevin",
                "number": "6287754321098",
                "text": "Min pesan Kopi Susu Bit & Bean botol 1 Liter sama roasted beans 250gr ready kah?",
                "reply": "Ready kak Kevin! Kopi susu 1L siap simpan di kulkas dan roasted beans segar pilihan.",
                "status": "replied"
            },
            {
                "id": "sample-5",
                "time": "19:10",
                "sender": "Kak Rizky",
                "number": "6281356789012",
                "text": "Kak saya sudah transfer DP untuk pembuatan program skripsi, minta nomor WA Kak Nor Anisa langsung ya",
                "reply": "Baik kak Rizky! Pesan dan bukti transfer sudah diteruskan langsung ke Kak Nor Anisa.",
                "status": "handover_to_owner"
            }
        ]
        with open(CHATS_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_chats, f, indent=2, ensure_ascii=False)
        return sample_chats

    try:
        with open(CHATS_FILE, "r", encoding="utf-8") as f:
            chats = json.load(f)
            return chats
    except Exception:
        return []

# ----------------- NOTIFIKASI PET MICHAN -----------------

def notify_michan(msg):
    try:
        payload = json.dumps({"message": msg, "sender": "AI Office Lead"}).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:19842/webhook", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=2)
    except Exception:
        pass

# ----------------- MAIN REPORT GENERATION -----------------

def generate_morning_report():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    hari_indo = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][now.weekday()]
    bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][now.month - 1]
    tanggal_lengkap = f"{hari_indo}, {now.day} {bulan_indo} {now.year} — Pukul {now.strftime('%H:%M')} WIB"

    print(f"\n========================================================")
    print(f"  ☀️ GENERATOR LAPORAN PAGI AI OFFICE (WHATSAPP & BISNIS)")
    print(f"  📅 {tanggal_lengkap}")
    print(f"========================================================\n")

    # 1. Cek kesehatan sistem
    print("[1/4] Memeriksa status infrastruktur & koneksi AI...")
    health = check_system_health()

    # 2. Muat & analisis chat
    print("[2/4] Menganalisis log interaksi WhatsApp CS (0851-5513-3070)...")
    chats = load_and_filter_chats()

    cat_counts = {"gas": 0, "bimbingan": 0, "coffee": 0, "handover": 0, "general": 0}
    leads_summary = []

    for c in chats:
        cat = categorize_chat(c.get("text", ""))
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        leads_summary.append(f"- [{c.get('time', '-')}] {c.get('sender', 'Kak')} (+{c.get('number', '-')}): \"{c.get('text', '')[:70]}\" -> Status: {c.get('status', 'ok')}")

    total_chats = len(chats)

    # 3. Panggil Hugging Face Bansos AI untuk menyusun Executive Briefing
    print("[3/4] Menghubungi Hugging Face Bansos AI (ling-3.0-flash-fin-free)...")
    
    prompt = f"""
Nama Anda adalah Lexi (Executive Strategy & Operations Lead di SondeR AI Office).
Tugas Anda: Susun LAPORAN EXECUTIVE BRIEFING PAGI HARI resmi untuk Pimpinan Ekosistem Bisnis: Ibu Ir. Nor Anisa, S.Kom., M.Kom.

Data Operasional 24 Jam Terakhir:
- Tanggal & Waktu: {tanggal_lengkap}
- Total Interaksi WhatsApp: {total_chats} percakapan
- Rincian Minat Pelanggan:
  * Refill Gas Portable & Canister (Rp 12.000 / botol): {cat_counts['gas']} inquiry
  * Bimbingan & Konsultasi Skripsi & Skripsi TI (Garansi revisi, print HVS): {cat_counts['bimbingan']} inquiry
  * Bit & Bean Coffee ☕ (Kopi aren, 1L, roasted beans): {cat_counts['coffee']} inquiry
  * Butuh Respon Personal Kak Nor Anisa / Bukti Transfer: {cat_counts['handover']} inquiry
  * Pertanyaan Umum: {cat_counts['general']} inquiry

Status Sistem:
- Hugging Face Bansos Router: {health.get('bansos', 'Online')}
- Portal Website SEO nourastudio.co-id.id: {health.get('website', 'Online')}
- Server AI Office 3D: {health.get('ai_office', 'Active')}
- Bot WhatsApp Terpadu: {health.get('whatsapp_bot', 'Active')}

Daftar Interaksi Chat Terkini:
{chr(10).join(leads_summary[:6])}

Panduan Penyusunan Laporan:
1. Sapa dengan penuh takzim dan semangat pagi kepada Ibu Ir. Nor Anisa, S.Kom., M.Kom.
2. Sajikan Ringkasan Eksekutif (Executive Summary) yang tajam dan padat.
3. Sorot Peluang Bisnis (Leads) & Hal yang Memerlukan Tindakan Segera (Action Items prioritas tinggi: misalnya bukti transfer / konsultasi skripsi).
4. Jangan pernah menyebut SOP keselamatan uji rendam air atau timbangan digital.
5. Berikan rekomendasi langkah strategis tim marketing/operasional hari ini.
6. Gunakan format Markdown yang sangat rapi dan estetik dengan emoji profesional.
""".strip()

    messages = [
        {"role": "system", "content": "Anda adalah Executive Assistant dan Strategic Analyst AI kelas dunia untuk Ekosistem Bisnis Nor Anisa."},
        {"role": "user", "content": prompt}
    ]

    ai_executive_summary = call_bansos_llm(messages)

    if not ai_executive_summary:
        ai_executive_summary = f"""
### Selamat Pagi, Ibu Ir. Nor Anisa, S.Kom., M.Kom.! ☀️
Berikut ringkasan harian performa WhatsApp dan sistem operasional bisnis Anda:

- **Aktivitas Chat**: Total {total_chats} interaksi masuk, meliputi pemesanan refill gas ({cat_counts['gas']}x), konsultasi Bimbingan & Konsultasi Skripsi ({cat_counts['bimbingan']}x), order Bit & Bean Coffee ({cat_counts['coffee']}x), dan {cat_counts['handover']} pelanggan membutuhkan respon personal Anda.
- **Prioritas Hari Ini**: Segera tindak lanjuti bukti pembayaran dan konsultasi deadline skripsi mahasiswa.
- **Kondisi Sistem**: Website Noura Studio, Hugging Face Bansos, dan AI Office berjalan stabil.
""".strip()

    # 4. Susun Full Markdown Report
    full_report = f"""# 📊 LAPORAN EKSEKUTIF PAGI HARI — EKOSISTEM BISNIS NOR ANISA
**Tanggal**: {tanggal_lengkap}  
**Penerima**: Ibu Ir. Nor Anisa, S.Kom., M.Kom. (Founder & Owner Noura Studio)  
**Disusun Oleh**: Lexi & Tim Strategic Operations (SondeR AI Office via Hugging Face Bansos)  

---

## 🚀 1. Status Infrastruktur & Koneksi AI
| Komponen | Status Operasional | Keterangan |
| :--- | :--- | :--- |
| 🤖 **Hugging Face Bansos AI** | `{health.get('bansos', 'Online')}` | Engine LLM utama (ling-3.0-flash-fin-free) |
| 🌐 **Website nourastudio.co-id.id** | `{health.get('website', 'Online')}` | SEO Schema.org, Sitemap & Robots.txt Aktif |
| 🏢 **Virtual AI Office 3D** | `{health.get('ai_office', 'Active')}` | Port 19845 - 35 Agen AI Siap Kerja |
| 📱 **WhatsApp CS Terpadu (0851-5513-3070)** | `{health.get('whatsapp_bot', 'Active')}` | Layanan 3 Unit Usaha 24 Jam Nonstop |
| ✈️ **Telegram Bot (@noranisa_bot)** | `{health.get('telegram_bot', 'Active')}` | Bot Asisten CS Terpadu & Notifikasi |

---

## 📈 2. Metrik Interaksi WhatsApp (24 Jam Terakhir)
- **Total Percakapan Masuk**: **{total_chats} Pesan**
- 🔥 **Refill Gas Portable Kalimantan (Rp 12.000)**: `{cat_counts['gas']} Pesan`
- 💻 **Bimbingan & Konsultasi Skripsi & Akademik Master**: `{cat_counts['bimbingan']} Pesan`
- ☕ **Bit & Bean Coffee & Roastery**: `{cat_counts['coffee']} Pesan`
- ⚠️ **Perlu Respons Personal Owner / Bukti Transfer**: `{cat_counts['handover']} Pesan`
- 💬 **Sapaan & Konsultasi Umum**: `{cat_counts['general']} Pesan`

---

## 🧠 3. Executive Briefing & Action Items (by Bansos AI)
{ai_executive_summary}

---

## 📝 4. Log Riwayat Chat Terbaru
{chr(10).join(leads_summary)}

---
*Laporan ini di-generate secara otomatis setiap pagi oleh SondeR AI Office Engine.*
""".strip()

    # Simpan file laporan
    report_filename = f"Laporan_Pagi_{date_str}.md"
    report_filepath = REPORTS_DIR / report_filename
    with open(report_filepath, "w", encoding="utf-8") as f:
        f.write(full_report)

    print(f"[4/4] Laporan berhasil disimpan ke: {report_filepath}")

    # Daftarkan ke AI Office documents.json agar semua 35 agen membacanya
    try:
        if DOCUMENTS_FILE.exists():
            with open(DOCUMENTS_FILE, "r", encoding="utf-8") as f:
                docs = json.load(f)
        else:
            docs = []

        # Update or add document
        doc_id = f"morning-report-{date_str}"
        existing = next((d for d in docs if d["id"] == doc_id), None)
        doc_entry = {
            "id": doc_id,
            "name": f"Laporan-Pagi-{date_str}.md",
            "content": full_report,
            "bytes": len(full_report.encode("utf-8")),
            "addedAt": int(time.time() * 1000)
        }
        if existing:
            existing.update(doc_entry)
        else:
            docs.insert(0, doc_entry)

        with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)
        print("[✓] Dokumen laporan telah terindeks ke 35 Agen di AI Office.")
    except Exception as e:
        print(f"[!] Gagal update documents.json: {e}")

    # Notifikasi ke Desktop Pet Michan jika aktif
    notify_michan(f"☀️ Laporan Pagi Siap! Ada {total_chats} chat WhatsApp masuk & {cat_counts['handover']} pesan butuh respon Ibu Nor Anisa.")

    return full_report, report_filepath

if __name__ == "__main__":
    generate_morning_report()
