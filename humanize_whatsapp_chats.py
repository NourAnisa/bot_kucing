# -*- coding: utf-8 -*-
"""
Script Penyesuaian Pesan WhatsApp & Gaya Komunikasi agar 100% Alami, Humanis & Sopan
Founder: Ir. Nor Anisa, S.Kom., M.Kom.
"""

import sys
import urllib.parse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"c:\Users\Nor Anisa\Downloads\SondeR-Cat-main")
BUILD_SCRIPT = Path(r"C:\Users\Nor Anisa\.gemini\antigravity\brain\7617cfe6-1c57-4e58-801a-ca2bd2b82d17\scratch\build_human_crafted_site.py")

with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update link wa di navbar & hero (Konsultasi Umum Dosen)
old_msg1 = "Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20saya%20ingin%20berkonsultasi"
new_msg1 = urllib.parse.quote("Halo Bu Anisa, salam kenal. Saya membaca profil Ibu di website dan ingin berkonsultasi santai mengenai bimbingan IT & layanan Noura Studio, terima kasih Bu.")
text = text.replace(old_msg1, new_msg1)

# 2. Update link wa Refill Gas
old_msg_gas = "Halo%20Admin%20Refill%20Gas%2C%20saya%20mau%20isi%20ulang%20gas%20portable"
new_msg_gas = urllib.parse.quote("Halo Kak Admin, salam kenal ya. Saya mau tanya info isi ulang gas portable/canister, untuk cabang terdekat hari ini buka sampai jam berapa ya kak?")
text = text.replace(old_msg_gas, new_msg_gas)

# 3. Update link wa Bimbingan Skripsi
old_msg_bimb = "Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20konsultasi%20bimbingan%20skripsi%20informatika"
new_msg_bimb = urllib.parse.quote("Assalamu’alaikum Bu Ir. Nor Anisa, perkenalkan saya mahasiswa tingkat akhir. Saya sedang menyusun tugas akhir/skripsi dan ingin berkonsultasi mengenai bimbingan teknis program, mohon info waktu luang Ibu ya, terima kasih banyak Bu.")
text = text.replace(old_msg_bimb, new_msg_bimb)

# 4. Update link wa Bit & Bean Coffee
old_msg_kopi = "Halo%20Admin%2C%20mau%20pesan%20Kopi%20Bit%20and%20Bean%201%20Liter"
new_msg_kopi = urllib.parse.quote("Halo Kak, salam kenal! Mau tanya untuk kopi susu aren Bit & Bean kemasan botol 1 Liter apakah ready stok untuk dipesan hari ini? Terima kasih ya kak!")
text = text.replace(old_msg_kopi, new_msg_kopi)

# 5. Update link Promo 1 (Bimbingan Kopi)
old_promo1 = "Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20klaim%20Promo%20Bimbingan%20Gratis%20Kopi%201L"
new_promo1 = urllib.parse.quote("Assalamu’alaikum Bu Anisa, saya tertarik mendaftar program bimbingan skripsi IT dan ingin sekalian klaim bonus kopi Bit & Bean 1 Liter, boleh minta info alur pendaftarannya Bu?")
text = text.replace(old_promo1, new_promo1)

# 6. Update link Promo 2 (Gas 5 botol)
old_promo2 = "Halo%20Admin%2C%20mau%20ambil%20Promo%20Refill%205%20Botol%2055rb"
new_promo2 = urllib.parse.quote("Halo Kak Admin, saya mau ambil paket borongan isi ulang gas 5 botol (Rp 55.000) ya. Bisa dibantu info alamat lengkap dan patokan lokasinya kak?")
text = text.replace(old_promo2, new_promo2)

# 7. Update link Promo 3 (Wisuda Kilat)
old_promo3 = "Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20konsultasi%20Paket%20Wisuda%20Kilat"
new_promo3 = urllib.parse.quote("Assalamu’alaikum Bu Ir. Nor Anisa, saya ingin berkonsultasi mengenai paket pendampingan skripsi kilat sampai sidang dan cek Turnitin, mohon arahannya Bu.")
text = text.replace(old_promo3, new_promo3)

# 8. Update link QRIS Bukti Pembayaran
old_qris = "Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20saya%20sudah%20melakukan%20pembayaran%20via%20QRIS"
new_qris = urllib.parse.quote("Halo Bu Anisa / Admin, saya sudah selesai melakukan pembayaran melalui scan QRIS BIT & BEAN. Berikut saya lampirkan bukti transfernya ya, mohon dicek. Terima kasih banyak!")
text = text.replace(old_qris, new_qris)

# 9. Update JavaScript Kalkulator Gas
old_js_gas = "const waMsg = encodeURIComponent('Halo Admin, mau pesan ' + (type === 'refill' ? 'Refill ' : 'Tabung Baru ') + qty + ' botol di cabang ' + cabang + ' (Estimasi: Rp ' + total.toLocaleString('id-ID') + ')');"
new_js_gas = "const waMsg = encodeURIComponent('Halo Kak Admin, salam kenal. Saya mau pesan ' + (type === 'refill' ? 'isi ulang (refill) ' : 'tabung kaleng baru ') + qty + ' botol gas di cabang ' + cabang + '. Untuk perkiraan biayanya sekitar Rp ' + total.toLocaleString('id-ID') + ', apakah hari ini ready kak? Terima kasih.');"
text = text.replace(old_js_gas, new_js_gas)

# 10. Update JavaScript Kalkulator Print
old_js_print = "const waMsg = encodeURIComponent('Halo Ibu Ir. Nor Anisa, mau cetak naskah skripsi HVS: ' + bw + ' hal BW, ' + color + ' hal Warna, sebanyak ' + copies + ' rangkap (Estimasi: Rp ' + grandTotal.toLocaleString('id-ID') + ')');"
new_js_print = "const waMsg = encodeURIComponent('Assalamu’alaikum Bu Anisa / Admin, saya mau cetak naskah skripsi HVS: ' + bw + ' halaman Hitam-Putih dan ' + color + ' halaman Warna, sebanyak ' + copies + ' rangkap (perkiraan Rp ' + grandTotal.toLocaleString('id-ID') + '). Apakah file dokumennya bisa langsung saya kirimkan ke nomor ini Bu? Terima kasih.');"
text = text.replace(old_js_print, new_js_print)

# Simpan ke build_human_crafted_site.py
with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
    f.write(text)
print("[✓] build_human_crafted_site.py berhasil diperbarui dengan pesan WA yang santun & humanis!")

# 11. Update server.js di whatsapp_bot agar CS Nadia membalas sangat ramah & hangat
wa_server = BASE_DIR / "whatsapp_bot" / "server.js"
if wa_server.exists():
    with open(wa_server, "r", encoding="utf-8") as f:
        js_code = f.read()

    js_code = js_code.replace(
        "JOKICODING & AKADEMIK MASTER (jokicoding.vercel.app — Ngoding, Skripsi TI/SI, Jurnal SINTA, PPT, CV, Print HVS)",
        "BIMBINGAN & KONSULTASI SKRIPSI IT (https://jokicoding.vercel.app/ — Asistensi pemrograman, bimbingan tugas akhir, Turnitin-ready, Print HVS)"
    )
    js_code = js_code.replace(
        "Jika tanya JOKI / SKRIPSI / KODING: Jelaskan jasa ngoding (Laravel/React/Python/Java, dsb), skripsi, 100% garansi bebas revisi, Turnitin-ready, print dokumen (BW Rp 400, Warna Rp 800).",
        "Jika tanya SKRIPSI / KODING / BIMBINGAN: Jelaskan program bimbingan & konsultasi skripsi langsung bersama akademisi (Laravel, React, Python, ML, dsb), garansi pendampingan sampai disetujui dosen, cek Turnitin <15%, dan jasa print dokumen HVS (BW Rp 400, Warna Rp 800). JANGAN gunakan istilah joki."
    )
    js_code = js_code.replace(
        "- Berikan balasan dalam Bahasa Indonesia yang sangat ramah, hangat, sopan, dan jelas seperti CS manusia profesional.\n",
        "- Berikan balasan dalam Bahasa Indonesia yang SANGAT HUMANIS, hangat, bersahabat, penuh empati, dan santun seperti sahabat/mentor yang siap membantu.\n"
        "- Gunakan sapaan akrab yang sopan seperti 'Halo Kak [Nama]! 😊' atau 'Selamat pagi/siang Kak'.\n"
        "- Jangan terdengar kaku seperti robot template, melainkan luwes dan tulus mendengarkan kebutuhan pelanggan.\n"
    )

    with open(wa_server, "w", encoding="utf-8") as f:
        f.write(js_code)
    print("[✓] whatsapp_bot/server.js berhasil diperbarui dengan prompt humanis!")
