# Neko Cat 🐾

**Neko Cat** adalah aplikasi *desktop pet* interaktif berbasis pixel art yang hidup di layar komputer Anda — menemani mengetik, tidur di atas jendela aplikasi, berjoget mengikuti alunan musik, dan dapat diajak mengobrol menggunakan kecerdasan buatan multi-model AI (*Google Gemini* dan *Bansos Router Multi-Model*).

Dibuat untuk **Windows** dan **Linux**. Ringan, open source, tanpa langganan, dan siap pakai.

![Neko Cat — reactions, poses, and cat themes](assets/showcase.png)

🔗 **Repositori Resmi**: [https://github.com/NourAnisa/bot_kucing](https://github.com/NourAnisa/bot_kucing)

---

## 🌟 Fitur Utama

### 1. Interaksi Alami dengan Pengguna
- 👀 **Eye Follow** — Pupil mata kucing mengikuti pergerakan kursor mouse di mana pun di layar dan berkedip secara natural.
- 🔴 **Laser Hunt** — Goyangkan kursor ke kiri dan kanan seperti titik laser, kucing akan berlari mengejarnya.
- 🐾 **Purring & Elusan** — Usap kepala kucing dengan mouse selama beberapa detik untuk memicu animasi hati (*hearts*), ekspresi dengkuran (*"purrr..."*), dan efek suara dengkuran asli.
- 🍡 **Mochi Drag** — Tarik tubuh kucing dengan mouse dan ia akan bergelantungan lucu meregang lentur seperti mochi.
- 😾 **Startle** — Gerakan kursor mendadak di dekatnya akan membuatnya melompat kaget.
- ⌨️ **Keyboard Kneading** — Saat Anda mengetik di keyboard, kucing ikut memijat tombol tuts mini 3D di layar secara realtime.
- 🔥 **Overheat Mode** — Jika Anda mengetik sangat cepat, kucing akan memerah dan mengeluarkan kepulan uap di atas kepalanya.
- 📜 **Paper Unroll** — Scroll mouse Anda dan kucing akan membuka gulungan kertas pixel.

### 2. Rekan Kerja Produktif (Productivity Companion)
- 😴 **Napping & Sleep** — Tertidur saat Anda tidak aktif; bangun dengan suara lembut *"mrrp?"*.
- 🧼 **Grooming** — Sesekali berhenti untuk menjilati kaki dan membersihkan diri.
- 🍽️ **Feeding Bowls** *(Opsional)* — Sediakan mangkuk makanan dan air di layar (*Behavior → Feeding bowls*).
- 🪟 **Window Climber** — Kucing bisa memanjat dan duduk di atas jendela aplikasi yang sedang aktif, ikut terbawa saat jendela digeser.
- ☂️ **Parachute Drop** — Jika jendela ditutup saat kucing berada di atasnya, kucing akan membuka parasut pixel dan meluncur anggun ke bagian bawah layar.
- 📺 **Auto-Hide** — Otomatis menyembunyikan diri saat Anda memutar video fullscreen.
- 🎧 **Music Vibes** — Mengenakan headphone pixel saat mendeteksi ada audio atau musik di komputer Anda.
- 🧘 **Stretch Reminders** — Pengingat peregangan tubuh setiap 30/50/90 menit.
- 🍅 **Pomodoro Timer** — Timer fokus dan istirahat pixel mengambang di samping kucing.

### 3. 🧠 Otak AI Multi-Model (Smart Auto-Failover)
Neko Cat dilengkapi integrasi kecerdasan buatan yang sangat tangguh:
- Tekan **Ctrl + Space** di mana saja untuk memunculkan kotak tanya-jawab (*Ask Neko*).
- **Multi-Model Provider**:
  * **Bansos Router**: Terhubung ke endpoint gratis OpenAI-compatible (`https://noranisa-bansos.hf.space/v1`).
  * **Google Gemini API**: Mendukung Gemini API key pribadi.
- **🔄 Smart Auto-Failover System**:
  Jika model utama mengalami *rate limit* (429) atau *offline* (400), Neko Cat otomatis beralih (*fallback*) secara instan ke model aktif berikutnya:
  1. `fast` *(LLM7 Fast - Ultra Cepat)*
  2. `codestral-latest` *(Mistral Codestral - Koding & Analisis)*
  3. `mistral-Nemo-Instruct-2407` *(Mistral Nemo - 128k Context)*
  4. `default` *(LLM7 Default)*
- **Menu Pemilih Model Instan**: Klik kanan pada kucing ➔ **AI Brain 🧠** ➔ **Pilih Model Router 🔀** untuk berganti model dengan satu klik.

### 4. 🎮 Mini Games Desktop
- 🦆 **Duck Hunt** — Mainkan tembak bebek pixel langsung di desktop Anda dengan musik latar 8-bit retro. Dapatkan 15 tembakan beruntun untuk memicu *Super Saiyan Blue Aura*!
- ✊ **Rock Paper Scissors** — Main suit batu-gunting-kertas cepat melawan Neko Cat.

### 5. Kustomisasi Tampilan Kucing
- 🐱 **Tema Kucing Nyata**: Lilly (Oranye putih), JJ (Tabby abu-abu), dan Mimi (Lynx-point mata biru).
- 🎨 **10 Pilihan Warna Bulu + Custom Color Picker**: Bebas memilih warna apa saja.
- 🧶 **5 Pola Corak**: Tabby, Solid, Tuxedo, Spots, Siamese.
- 👁️ **Warna Mata**: Midnight, Green, Hazel, Blue, Amber, Pink, atau Custom HEX.
- 📏 **7 Pilihan Ukuran**: Mulai dari 2× hingga 10×.
- 🐈🐈 **Multi-Cat**: Dukungan menampilkan lebih dari satu kucing di layar secara bersamaan.

---

## 🚀 Panduan Instalasi & Menjalankan

### Persyaratan Sistem
- **Windows 10 / 11 (64-bit)** atau **Linux** (X11 / Wayland)
- Python 3.9+ (Dilengkapi *offline libraries* di folder `libs/`)

### Cara Menjalankan Langsung (Windows):

1. **Jalankan Aplikasi:**
   Cukup klik dua kali berkas:
   ```cmd
   run.bat
   ```
   Atau jalankan melalui PowerShell / Command Prompt:
   ```cmd
   python nekocat.py
   ```

2. **Membuat Shortcut Desktop:**
   Jalankan:
   ```cmd
   CLICK_ME_TO_INSTALL.bat
   ```
   Shortcut **`Neko Cat.lnk`** akan dibuat otomatis di Desktop Anda.

3. **Mode Debug (Jika Mengalami Kendala):**
   ```cmd
   debug.bat
   ```

### Cara Menjalankan di Linux:
```bash
git clone https://github.com/NourAnisa/bot_kucing.git
cd bot_kucing
./install.sh
./run.sh
```

---

## 📁 Struktur Berkas Proyek

```text
bot_kucing/
├── nekocat.py                     # Program utama Neko Cat (GUI PySide6, AI, event loop)
├── sondercat.py                   # Berkas redirect kompatibilitas mundur
├── sprites.py                     # Definisi matriks pixel art ASCII & palet warna
├── neko_agent.py                  # Penghubung agent CLI
├── neko_antigravity.py            # Integrasi IDE Antigravity
├── neko_brave_userscript.user.js  # Ekstensi connector browser Brave
├── run.bat / run.sh               # Skrip peluncur cepat
├── debug.bat                      # Skrip peluncur mode debug
├── CLICK_ME_TO_INSTALL.bat        # Skrip installer desktop sekali klik
├── neko_cat_setup.exe             # Portable setup executable
├── nekocat_gray.ico               # Ikon aplikasi
├── meow.wav                       # Suara meong asli
├── sounds/                        # Efek suara dengkuran (purr_pet, purr_sleep)
├── assets/                        # Gambar dokumentasi & preview
├── ai_office/                     # Dashboard AI Office & sistem monitoring
├── whatsapp_bot/                  # Server bot customer service WhatsApp
└── libs/                          # Dependensi offline PySide6 & pynput
```

---

## 🎨 Mengubah / Mengedit Desain Pixel Art

Seluruh pose animasi digambar menggunakan matriks teks pixel di [`sprites.py`](sprites.py). Anda dapat mengeditnya secara langsung saat aplikasi berjalan:
1. Klik kanan pada kucing ➔ **Animations** ➔ **Open animations file**.
2. Centang **Auto-reload on save**.
3. Buka file `sprites.py` di code editor, lakukan perubahan, dan tekan **Ctrl + S**. Desain kucing di layar akan langsung berubah secara realtime!
4. Panduan lengkap sintaks pixel art tersedia di [`ANIMATIONS.md`](ANIMATIONS.md).

---

## 📜 Lisensi & Atribusi

Proyek ini dirilis di bawah lisensi **Apache License 2.0**.  
* Terinspirasi oleh konsep *Comnyang* (macOS).
* Dikembangkan dan disesuaikan dari basis arsitektur *SondeR-Cat* oleh Verisonder.
* Rebrand & Ekosistem Multi-Model AI Router dikembangkan untuk **Neko Cat** oleh Nor Anisa / Noura Studio.
* Rincian lisensi lengkap dapat dilihat pada berkas [`LICENSE`](LICENSE) dan [`NOTICE`](NOTICE).
