# -*- coding: utf-8 -*-
"""
Script Otomasi Pengelola Website nourastudio.co-id.id
Ditenagai FTP Deployment Otomatis
"""

import os
import sys
import ftplib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FTP_HOST = "194.233.65.45"
FTP_PORT = 21
FTP_USER = "admin@nourastudio.co-id.id"
FTP_PASS = "O~VN*15u4X^K"

DOWNLOADS_DIR = Path(r"c:\Users\Nor Anisa\Downloads")
SONDER_DIR = DOWNLOADS_DIR / "SondeR-Cat-main"
FILES_TO_DEPLOY = [
    "index.html",
    "robots.txt",
    "sitemap.xml",
    "sync_to_public_html.php",
    "google1bfaed16ab67c926.html",
    "qris_bit_bean.png"
]

def deploy_website():
    print(f"[*] Menghubungkan ke FTP {FTP_HOST}:{FTP_PORT}...")
    try:
        ftp = ftplib.FTP(FTP_HOST, timeout=20)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"[✓] Berhasil login sebagai {FTP_USER}")

        # Cari semua file verifikasi google*.html di Downloads dan SondeR-Cat-main
        all_files = list(FILES_TO_DEPLOY)
        for g in DOWNLOADS_DIR.glob("google*.html"):
            if g.name not in all_files:
                all_files.append(g.name)
        for g in SONDER_DIR.glob("google*.html"):
            if g.name not in all_files:
                all_files.append(g.name)

        for fname in all_files:
            fpath = DOWNLOADS_DIR / fname
            if not fpath.exists():
                fpath = SONDER_DIR / fname

            if fpath.exists():
                print(f"[*] Mengunggah {fname} ({fpath.stat().st_size} bytes)...")
                with open(fpath, "rb") as f:
                    res = ftp.storbinary(f"STOR {fname}", f)
                    print(f"    [✓] {fname}: {res}")
            else:
                print(f"[!] File {fname} tidak ditemukan!")

        files = ftp.nlst()
        print(f"\n[✓] Seluruh file aktif di server: {files}")
        ftp.quit()

        # Trigger sinkronisasi otomatis ke root public_html
        try:
            import urllib.request
            sync_url = "https://nourastudio.co-id.id/nourastudio.co-id.id/public/sync_to_public_html.php"
            req = urllib.request.Request(sync_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print("[✓] Sinkronisasi ke root public_html berhasil!")
        except Exception as se:
            print(f"[!] Sinkronisasi root: {se}")

        print("\n🎉 WEBSITE & SEO ASSETS BERHASIL AKTIF DI DOMAIN UTAMA!")
        print("• Website Utama : https://nourastudio.co-id.id/")
        print("• Sitemap XML   : https://nourastudio.co-id.id/sitemap.xml")
        print("• Robots TXT    : https://nourastudio.co-id.id/robots.txt")
        print("• Telegram Bot  : https://nourastudio.co-id.id/telegram_webhook.php")
        return True
    except Exception as e:
        print(f"[!] Gagal upload: {e}")
        return False

if __name__ == "__main__":
    deploy_website()
