# -*- coding: utf-8 -*-
"""
Script Pembersihan & Penyelarasan Istilah Etika Akademik Dosen
Mengganti seluruh istilah 'joki' menjadi 'bimbingan & konsultasi'
sesuai etika perguruan tinggi dan arahan resmi Ir. Nor Anisa, S.Kom., M.Kom.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"c:\Users\Nor Anisa\Downloads\SondeR-Cat-main")
DOWNLOADS_DIR = Path(r"c:\Users\Nor Anisa\Downloads")
BRAIN_DIR = Path(r"C:\Users\Nor Anisa\.gemini\antigravity\brain\7617cfe6-1c57-4e58-801a-ca2bd2b82d17")

TARGET_FILES = [
    BRAIN_DIR / "scratch" / "build_human_crafted_site.py",
    BASE_DIR / "telegram_webhook.php",
    BASE_DIR / "auto_content_engine.py",
    BASE_DIR / "articles_database.json",
    BASE_DIR / "ai_office" / "morning_report.py",
    BRAIN_DIR / "diagram_arsitektur_ekosistem.md"
]

REPLACEMENTS = [
    ("joki skripsi", "bimbingan & konsultasi skripsi"),
    ("Joki Skripsi", "Bimbingan & Konsultasi Skripsi"),
    ("Jasa joki coding", "Layanan bimbingan & konsultasi coding"),
    ("jasa joki", "layanan bimbingan"),
    ("jasa pengerjaan program skripsi", "layanan bimbingan pemrograman & skripsi"),
    ("pengerjaan program skripsi", "bimbingan penyusunan program skripsi"),
    ("pengerjaan aplikasi skripsi", "bimbingan rekayasa sistem skripsi"),
    ("pengerjaan tugas", "bimbingan teknis tugas"),
    ("JokiCoding & Akademik Master", "Bimbingan & Konsultasi Akademik IT"),
    ("JokiCoding & Bimbingan IT", "Bimbingan & Konsultasi Akademik IT"),
    ("JokiCoding", "Bimbingan IT & Konsultasi"),
    ("jokicoding", "bimbingan IT"), # perhatikan url jangan sampai rusak
    ("Order Coding", "Program Bimbingan Skripsi"),
    ("order coding", "bimbingan coding"),
]

print("[*] Memulai pembersihan dan penyesuaian istilah etika akademik...")
