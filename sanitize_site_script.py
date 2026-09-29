# -*- coding: utf-8 -*-
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(r"C:\Users\Nor Anisa\.gemini\antigravity\brain\7617cfe6-1c57-4e58-801a-ca2bd2b82d17\scratch\build_human_crafted_site.py")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Ganti seluruh kata joki
text = text.replace('Pembina JokiCoding Skripsi Bebas Revisi', 'Pembina Bimbingan & Konsultasi Skripsi Bebas Revisi')
text = text.replace('JokiCoding Vercel, Bimbingan Skripsi Informatika', 'Bimbingan Skripsi Informatika, Konsultasi Tugas Akhir')
text = text.replace('bimbingan JokiCoding garansi revisi', 'bimbingan & konsultasi skripsi garansi revisi')
text = text.replace('laboratorium asistensi komputasi <b>JokiCoding</b> bergaransi bebas revisi', 'laboratorium asistensi komputasi <b>Bimbingan & Konsultasi Skripsi IT</b> bergaransi pendampingan')
text = text.replace('<a href="#joki" class="hover:text-blue-800 transition">JokiCoding</a>', '<a href="#bimbingan" class="hover:text-blue-800 transition">Bimbingan Skripsi</a>')
text = text.replace('id="joki"', 'id="bimbingan"')
text = text.replace('<!-- Usaha 2: JokiCoding -->', '<!-- Usaha 2: Bimbingan & Konsultasi Skripsi IT -->')
text = text.replace('JokiCoding &amp; Bimbingan IT', 'Bimbingan &amp; Konsultasi Skripsi IT')
text = text.replace('Asistensi profesional pengerjaan program skripsi, pembuatan aplikasi web/mobile, analisis data, dan persiapan sidang yang dibimbing langsung oleh akademisi berpengalaman.', 'Bimbingan dan asistensi komprehensif penyusunan program skripsi, konsultasi arsitektur web/mobile, analisis data, dan persiapan sidang yang dibimbing langsung oleh akademisi berpengalaman.')
text = text.replace('Kunjungi jokicoding.vercel.app ↗', 'Kunjungi Portal Bimbingan Akademik ↗')
text = text.replace('wa.me/6285155133070?text=Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20konsultasi%20bimbingan%20tugas%20coding', 'wa.me/6285155133070?text=Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20konsultasi%20bimbingan%20skripsi%20informatika')
text = text.replace('Order Coding + Gratis Kopi 1 Liter', 'Paket Bimbingan Skripsi + Gratis Kopi 1 Liter')
text = text.replace('Setiap pemesanan jasa pembuatan program tugas akhir atau proyek web di JokiCoding,', 'Setiap pendaftaran program bimbingan & konsultasi skripsi atau proyek web,')
text = text.replace('wa.me/6285155133070?text=Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20klaim%20Promo%20Coding%20Gratis%20Kopi%201L', 'wa.me/6285155133070?text=Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20mau%20klaim%20Promo%20Bimbingan%20Gratis%20Kopi%201L')
text = text.replace('Pengerjaan aplikasi web/mobile + pendampingan revisi sampai sidang + pengecekan similarity Turnitin &lt;15% + cetak naskah HVS rapi siap jilid.', 'Pendampingan rancang bangun sistem web/mobile + bimbingan revisi sampai sidang + verifikasi similarity Turnitin &lt;15% + cetak naskah HVS rapi siap jilid.')
text = text.replace('keunggulan bimbingan <b>100% garansi bebas revisi</b> di JokiCoding.', 'keunggulan <b>100% bimbingan pendampingan revisi</b> hingga disetujui dosen.')
text = text.replace('Bagaimana jaminan garansi dan kerahasiaan di JokiCoding?', 'Bagaimana jaminan garansi dan kerahasiaan bimbingan skripsi?')
text = text.replace('Dibimbing langsung oleh <b>Ir. Nor Anisa, S.Kom., M.Kom.</b>, JokiCoding memberikan <b>100% Garansi Bebas Revisi</b> sampai kode atau karya tulis Anda disetujui dosen, <b>100% Kerahasiaan Identitas Terjamin</b>, dan karya original bebas plagiasi (Turnitin-ready).', 'Dibimbing langsung oleh <b>Ir. Nor Anisa, S.Kom., M.Kom.</b>, layanan bimbingan memberikan <b>100% Garansi Pendampingan Revisi</b> sampai program atau karya tulis Anda disetujui dosen pembimbing, <b>100% Kerahasiaan Identitas Terjamin</b>, dan karya original bebas plagiasi (Turnitin-ready).')
text = text.replace('>JokiCoding<', '>Bimbingan Skripsi<')

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("[✓] build_human_crafted_site.py berhasil disterilkan sepenuhnya!")
