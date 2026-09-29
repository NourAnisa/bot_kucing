# -*- coding: utf-8 -*-
"""
Penyelarasan Total Istilah Bimbingan & Konsultasi Skripsi
Menghapus seluruh istilah 'joki' dari seluruh website, skrip bot, AI engine, dan diagram.
"""

import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"c:\Users\Nor Anisa\Downloads\SondeR-Cat-main")
DOWNLOADS_DIR = Path(r"c:\Users\Nor Anisa\Downloads")
BRAIN_DIR = Path(r"C:\Users\Nor Anisa\.gemini\antigravity\brain\7617cfe6-1c57-4e58-801a-ca2bd2b82d17")

# 1. Update telegram_webhook.php
tg_file = BASE_DIR / "telegram_webhook.php"
if tg_file.exists():
    with open(tg_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Ubah prompt dan aturan
    content = content.replace(
        "2. JOKICODING & AKADEMIK MASTER (https://jokicoding.vercel.app/)\n"
        "   - Pengerjaan skripsi & tugas programming: Next.js, React, Laravel, PHP, Python, Java, Mobile App\n"
        "   - 100% GARANSI BEBAS REVISI, Kerahasiaan Terjamin, Turnitin-ready",
        "2. BIMBINGAN & KONSULTASI SKRIPSI IT (https://jokicoding.vercel.app/)\n"
        "   - Layanan bimbingan & konsultasi skripsi, tugas akhir IT, dan asistensi programming: Next.js, React, Laravel, PHP, Python, Java, Mobile App\n"
        "   - 100% GARANSI PENDAMPINGAN REVISI SAMPAI LULUS & DISETUJUI DOSEN, Kerahasiaan Terjamin, Turnitin-ready"
    )
    content = content.replace(
        "- JANGAN PERNAH menyebutkan atau membahas SOP keselamatan uji rendam air atau timbangan digital.\n",
        "- JANGAN PERNAH menyebutkan atau membahas SOP keselamatan uji rendam air atau timbangan digital.\n"
        "- DILARANG KERAS menggunakan kata 'joki' atau 'joki skripsi'. Selalu gunakan istilah resmi & etis: 'Bimbingan & Konsultasi Skripsi', 'Asistensi Pemrograman', atau 'Pendampingan Tugas Akhir IT'.\n"
    )
    content = content.replace("JokiCoding", "Bimbingan & Konsultasi IT")
    content = content.replace("jokicoding", "bimbingan IT")

    with open(tg_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] telegram_webhook.php berhasil disterilkan dari istilah joki!")

# 2. Update auto_content_engine.py
auto_file = BASE_DIR / "auto_content_engine.py"
if auto_file.exists():
    with open(auto_file, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("pembina JokiCoding garansi revisi", "pembina Bimbingan & Konsultasi Skripsi IT bergaransi pendampingan")
    content = content.replace("jokicoding vercel", "bimbingan skripsi vercel")
    content = content.replace("JokiCoding", "Bimbingan & Konsultasi IT")
    content = content.replace("- Jangan sebut SOP uji rendam air atau timbangan digital.\n",
                              "- Jangan sebut SOP uji rendam air atau timbangan digital.\n"
                              "- DILARANG KERAS menggunakan kata 'joki' atau 'joki skripsi'. Gunakan istilah 'Bimbingan & Konsultasi Skripsi / Tugas Akhir Informatika'.\n")

    with open(auto_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] auto_content_engine.py berhasil diperbarui!")

# 3. Update articles_database.json
art_file = BASE_DIR / "articles_database.json"
if art_file.exists():
    with open(art_file, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("di JokiCoding", "dalam program Bimbingan & Konsultasi Skripsi kami")
    content = content.replace("JokiCoding", "Bimbingan & Konsultasi IT")
    content = content.replace("jokicoding", "bimbingan-skripsi")
    with open(art_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] articles_database.json berhasil disterilkan!")

# 4. Update morning_report.py
rep_file = BASE_DIR / "ai_office" / "morning_report.py"
if rep_file.exists():
    with open(rep_file, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('if any(k in t for k in ["koding", "coding", "skripsi", "joki", "tugas"',
                              'if any(k in t for k in ["bimbingan", "konsultasi", "koding", "coding", "skripsi", "tugas"')
    content = content.replace("JokiCoding", "Bimbingan & Konsultasi Skripsi")
    content = content.replace("Joki Coding", "Bimbingan Skripsi")
    content = content.replace("joki", "bimbingan")
    with open(rep_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] morning_report.py berhasil diselaraskan!")

# 5. Update diagram_arsitektur_ekosistem.md
diag_file = BRAIN_DIR / "diagram_arsitektur_ekosistem.md"
if diag_file.exists():
    with open(diag_file, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("JokiCoding & Bimbingan IT", "Bimbingan & Konsultasi Skripsi IT")
    content = content.replace("JokiCoding & Akademik Master", "Bimbingan & Konsultasi Akademik IT")
    content = content.replace("JokiCoding", "Bimbingan & Konsultasi Skripsi")
    content = content.replace("jokicoding", "bimbingan-skripsi")
    with open(diag_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] diagram_arsitektur_ekosistem.md berhasil diselaraskan!")

print("[*] Selesai pembaruan seluruh komponen!")
