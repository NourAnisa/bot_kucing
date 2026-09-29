# -*- coding: utf-8 -*-
"""
SondeR AI Office - Autonomous SEO Content Engine
Penulis & Penerbit Artikel Otomatis untuk Website https://nourastudio.co-id.id/
Atas Nama: Ir. Nor Anisa, S.Kom., M.Kom. (Dosen Informatika & Insinyur Profesional)
Ditenagai AI Hugging Face Bansos (ling-3.0-flash-fin-free) & FTP Deployment Otomatis
"""

import os
import sys
import json
import time
import ftplib
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DOWNLOADS_DIR = Path(r"c:\Users\Nor Anisa\Downloads")
ARTICLES_JSON = BASE_DIR / "articles_database.json"
INDEX_PATH = DOWNLOADS_DIR / "index.html"
SITEMAP_PATH = DOWNLOADS_DIR / "sitemap.xml"

# Konfigurasi FTP Hosting
FTP_HOST = "194.233.65.45"
FTP_PORT = 21
FTP_USER = "admin@nourastudio.co-id.id"
FTP_PASS = "O~VN*15u4X^K"

# Konfigurasi AI & Telegram
BANSOS_URL = "https://noranisa-bansos.hf.space/v1/chat/completions"
BANSOS_KEY = "bansos"
BANSOS_MODEL = "ling-3.0-flash-fin-free"
TG_TOKEN = "8664429930:AAGCvxMhh50wVBmHzZm48QA_L40wrt6rcx0"

CURATED_TOPICS = [
    {
        "category": "Tips Akademik & Pemrograman",
        "theme": "blue",
        "topic": "Strategi Merancang Arsitektur Web Skripsi dengan Laravel 11 & React yang Siap Diuji Penguji",
        "keywords": "skripsi laravel 11 react, bimbingan coding banjarmasin, bimbingan skripsi vercel, garansi bebas revisi",
        "wa_text": "Halo Ibu Ir. Nor Anisa, mau konsultasi skripsi Laravel dan React"
    },
    {
        "category": "Panduan Energi & Outdoor",
        "theme": "emerald",
        "topic": "Solusi Hemat Energi Masak Anak Kost & Cafe Grill: Mengapa Refill Gas Rp 12.000 Menjadi Pilihan Terbaik di Banjarmasin & Palangka Raya",
        "keywords": "refill gas portable banjarmasin, gas kaleng palangka raya toko karya perdana, isi ulang gas 12000",
        "wa_text": "Halo Admin, mau tanya refill gas portable untuk cafe dan harian"
    },
    {
        "category": "Kultur Kopi & Produktivitas",
        "theme": "amber",
        "topic": "Menjaga Ritme Fokus Saat Lembur Riset: Keunggulan Botol Literan (1 Liter) Bit & Bean Coffee Ramah Lambung",
        "keywords": "kopi susu aren literan, bit and bean coffee kalimantan, kopi programmer ramah lambung",
        "wa_text": "Halo Admin, mau pesan kopi susu aren 1 liter Bit and Bean"
    },
    {
        "category": "Tips Akademik & Machine Learning",
        "theme": "blue",
        "topic": "Kiat Praktis Menyusun Bab 4 Pembahasan Skripsi Machine Learning agar Lolos Sidang Sekali Maju",
        "keywords": "skripsi machine learning python, pembahasan bab 4 skripsi, bimbingan tugas akhir informatika",
        "wa_text": "Halo Ibu Ir. Nor Anisa, mau bimbingan bab 4 skripsi machine learning"
    },
    {
        "category": "Panduan Outdoor Kalimantan",
        "theme": "emerald",
        "topic": "Panduan Logistik Pendakian Pegunungan Meratus: Pentingnya Membawa Cadangan Canister Ulir dan Lokasi Refill Terdekat",
        "keywords": "pendakian pegunungan meratus, gas canister outdoor kalimantan, refill gas balikpapan lamaru",
        "wa_text": "Halo Admin, mau siapkan gas canister untuk pendakian Meratus"
    }
]

def load_articles():
    if ARTICLES_JSON.exists():
        try:
            with open(ARTICLES_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_articles(articles):
    with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def generate_new_article_via_ai():
    articles = load_articles()
    existing_titles = [a["title"] for a in articles]

    # Pilih topik yang belum pernah ditulis
    chosen_seed = None
    for candidate in CURATED_TOPICS:
        if candidate["topic"] not in existing_titles:
            chosen_seed = candidate
            break

    if not chosen_seed:
        chosen_seed = CURATED_TOPICS[len(articles) % len(CURATED_TOPICS)]

    # Susun prompt ke Bansos AI
    prompt = f"""
Anda adalah asisten akademik untuk Ir. Nor Anisa, S.Kom., M.Kom. (Dosen Informatika di Kalimantan, Insinyur Profesional, pembina Bimbingan & Konsultasi Skripsi IT bergaransi pendampingan, Refill Gas Portable Rp 12.000 di 3 cabang Banjarmasin/Palangka Raya/Balikpapan, dan Bit & Bean Coffee).
Tolong buatkan SATU artikel edukasi SEO yang elegan, berbobot, manusiawi, dan santun.

Topik: {chosen_seed['topic']}
Kategori: {chosen_seed['category']}
Kata Kunci: {chosen_seed['keywords']}

ATURAN KETAT:
- Jangan sebut SOP uji rendam air atau timbangan digital.
- DILARANG KERAS menggunakan kata 'joki' atau 'joki skripsi'. Gunakan istilah 'Bimbingan & Konsultasi Skripsi / Tugas Akhir Informatika'.
- Selalu sebut nama Ir. Nor Anisa, S.Kom., M.Kom.
- Format respon JSON murni dengan struktur:
{{
  "title": "{chosen_seed['topic']}",
  "excerpt": "Ringkasan 2-3 kalimat menarik, informatif, dan mengalir santun untuk pembaca di Kalimantan.",
  "category": "{chosen_seed['category']}",
  "theme": "{chosen_seed['theme']}",
  "wa_text": "{chosen_seed['wa_text']}"
}}
Hanya kirimkan JSON tanpa markdown ```json atau teks pembuka lainnya.
"""
    try:
        payload = json.dumps({
            "model": BANSOS_MODEL,
            "messages": [
                {"role": "system", "content": "You are a professional educational editor outputting strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.6,
            "max_tokens": 600
        }).encode("utf-8")

        req = urllib.request.Request(
            BANSOS_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {BANSOS_KEY}",
                "User-Agent": "SondeR-AutoContent/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            content = data["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            new_art = json.loads(content)
            new_art["id"] = "art-" + str(int(time.time()))
            new_art["date"] = datetime.now().strftime("%Y-%m-%d")
            new_art["author"] = "Ir. Nor Anisa, S.Kom., M.Kom."
            return new_art
    except Exception as e:
        print(f"[!] AI API fallback to curated seed: {e}")
        return {
            "id": "art-" + str(int(time.time())),
            "title": chosen_seed["topic"],
            "excerpt": f"Artikel panduan mendalam dan telaah praktis dari Ir. Nor Anisa, S.Kom., M.Kom. untuk membantu civitas akademika dan masyarakat di Kalimantan memaksimalkan efisiensi, akurasi, dan kenyamanan aktivitas harian.",
            "category": chosen_seed["category"],
            "theme": chosen_seed["theme"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": "Ir. Nor Anisa, S.Kom., M.Kom.",
            "wa_text": chosen_seed["wa_text"]
        }

def render_articles_html(articles):
    cards_html = []
    # Tampilkan maksimal 6 artikel terbaru
    for art in articles[:6]:
        theme = art.get("theme", "blue")
        if theme == "emerald":
            badge_cls = "text-emerald-800 uppercase mb-2"
            link_cls = "text-emerald-800 hover:text-emerald-950"
            arrow = "→"
        elif theme == "amber":
            badge_cls = "text-amber-800 uppercase mb-2"
            link_cls = "text-amber-800 hover:text-amber-950"
            arrow = "→"
        else:
            badge_cls = "text-blue-800 uppercase mb-2"
            link_cls = "text-blue-800 hover:text-blue-950"
            arrow = "→"

        wa_url = "https://wa.me/6285155133070?text=" + urllib.parse.quote(art.get("wa_text", "Halo Ibu Ir. Nor Anisa"))

        card = f'''        <!-- {art['id']} -->
        <article class="paper-card p-6 rounded-2xl flex flex-col justify-between bg-white">
          <div>
            <div class="text-[11px] font-bold {badge_cls}">{art.get('category', 'Artikel Edukatif')}</div>
            <h3 class="serif-heading text-base font-bold text-slate-900 leading-snug">
              {art['title']}
            </h3>
            <p class="text-xs text-slate-600 mt-3 leading-relaxed">
              {art['excerpt']}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="text-[11px] text-slate-400 font-medium">Ditulis: {art.get('date', '2026-09-28')}</span>
            <a href="{wa_url}" target="_blank"
               class="font-bold {link_cls} transition flex items-center gap-1">
              <span>Konsultasi via WA</span> <span>{arrow}</span>
            </a>
          </div>
        </article>'''
        cards_html.append(card)

    return "\n\n".join(cards_html)

def update_website_with_articles(articles):
    if not INDEX_PATH.exists():
        print(f"[!] {INDEX_PATH} tidak ditemukan.")
        return False

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Cari section artikel
    start_tag = '<!-- ==================== 8. ARTIKEL & CATATAN EDUKASI ==================== -->'
    end_tag = '<!-- ==================== 9. FAQ / TANYA JAWAB ==================== -->'

    if start_tag not in html or end_tag not in html:
        print("[!] Tag pembatas section artikel tidak ditemukan di index.html")
        return False

    rendered_cards = render_articles_html(articles)

    new_section = f'''{start_tag}
  <section id="artikel" class="py-20 bg-[#faf9f6] border-b border-slate-200">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
        <div>
          <span class="text-xs font-bold text-emerald-800 uppercase tracking-wider">Artikel &amp; Catatan Edukatif</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-bold text-slate-900 mt-1">Panduan Praktis &amp; Analisis Terpercaya</h2>
          <p class="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">
            Ditulis langsung oleh <b>Ir. Nor Anisa, S.Kom., M.Kom.</b> untuk memberikan referensi mendalam bagi masyarakat di Kalimantan.
          </p>
        </div>
        <div class="text-xs text-slate-500 font-medium bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm">
          📚 Total: <b>{len(articles)} Artikel Edukasi</b> Terpublikasi
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
{rendered_cards}
      </div>
    </div>
  </section>

  '''

    before = html[:html.find(start_tag)]
    after = html[html.find(end_tag):]
    updated_html = before + new_section + after

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print(f"[✓] Berhasil memperbarui {INDEX_PATH} dengan {len(articles)} artikel!")

    # Perbarui sitemap.xml lastmod
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://nourastudio.co-id.id/</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(sitemap_content.strip())
        print(f"[✓] Berhasil memperbarui {SITEMAP_PATH} dengan lastmod {today_str}")
    except Exception as e:
        print(f"[!] Gagal update sitemap: {e}")

    return True

def deploy_to_server():
    print(f"[*] Menghubungkan ke FTP {FTP_HOST}:{FTP_PORT}...")
    try:
        ftp = ftplib.FTP(FTP_HOST, timeout=20)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"[✓] Berhasil login sebagai {FTP_USER}")

        files_to_send = ["index.html", "sitemap.xml", "robots.txt"]
        for fname in files_to_send:
            fpath = DOWNLOADS_DIR / fname
            if fpath.exists():
                print(f"[*] Mengunggah {fname}...")
                with open(fpath, "rb") as f:
                    ftp.storbinary(f"STOR {fname}", f)
                    print(f"    [✓] {fname} berhasil diunggah!")

        ftp.quit()

        # Trigger sinkronisasi root
        try:
            sync_url = "https://nourastudio.co-id.id/nourastudio.co-id.id/public/sync_to_public_html.php"
            req = urllib.request.Request(sync_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print("[✓] Sinkronisasi ke root public_html berhasil!")
        except Exception as se:
            print(f"[!] Sinkronisasi root: {se}")

        return True
    except Exception as e:
        print(f"[!] Gagal deploy: {e}")
        return False

def notify_telegram(new_article):
    # Cek apakah ada chat id tersimpan di log
    chat_id = None
    try:
        # Coba ambil chat_id terakhir dari webhook log di hosting
        req = urllib.request.Request("https://nourastudio.co-id.id/telegram_cloud_chats.json", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data and len(data) > 0:
                chat_id = data[0].get("chat_id")
    except Exception:
        pass

    msg_text = (
        f"📰 *ARTIKEL SEO BARU BERHASIL TERBIT!*\n\n"
        f"👤 *Penulis:* Ir. Nor Anisa, S.Kom., M.Kom.\n"
        f"📑 *Judul:* {new_article['title']}\n"
        f"🏷️ *Kategori:* {new_article['category']}\n"
        f"🌐 *Website:* https://nourastudio.co-id.id/#artikel\n\n"
        f"✅ *Status:* Artikel langsung tayang di website dan `sitemap.xml` telah diperbarui otomatis untuk bot Google."
    )

    if chat_id:
        try:
            send_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": chat_id,
                "text": msg_text,
                "parse_mode": "Markdown"
            }).encode("utf-8")
            req = urllib.request.Request(send_url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                print("[✓] Notifikasi Telegram berhasil terkirim!")
        except Exception as te:
            print(f"[!] Gagal kirim notif Telegram: {te}")
    else:
        print("[i] Bot Telegram ready. Pesan disiapkan untuk broadcast ketika chat aktif.")

def run_auto_publisher():
    print(f"\n==========================================")
    print(f"🚀 Menjalankan Auto Content Engine ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"==========================================")

    articles = load_articles()
    print(f"[*] Jumlah artikel saat ini: {len(articles)}")

    print("[*] Menghasilkan artikel baru dengan standar akademik Ir. Nor Anisa, S.Kom., M.Kom...")
    new_art = generate_new_article_via_ai()
    print(f"[✓] Artikel baru: '{new_art['title']}' ({new_art['category']})")

    # Masukkan ke daftar artikel paling depan
    articles.insert(0, new_art)
    save_articles(articles)

    print("[*] Menyuntikkan artikel ke index.html dan memperbarui sitemap...")
    if update_website_with_articles(articles):
        print("[*] Melakukan deploy otomatis via FTP ke hosting...")
        if deploy_to_server():
            print("[*] Mengirimkan laporan notifikasi...")
            notify_telegram(new_art)
            print("\n🎉 SUKSES! Artikel baru sudah tayang di https://nourastudio.co-id.id/!")
            return True

    return False

if __name__ == "__main__":
    run_auto_publisher()
