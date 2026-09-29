# -*- coding: utf-8 -*-
"""
Script Integrasi QRIS Nasional & Kalkulator Interaktif di Website nourastudio.co-id.id
Founder: Ir. Nor Anisa, S.Kom., M.Kom.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BUILD_SCRIPT = Path(r"C:\Users\Nor Anisa\.gemini\antigravity\brain\7617cfe6-1c57-4e58-801a-ca2bd2b82d17\scratch\build_human_crafted_site.py")

with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Tambah tombol QRIS di Navbar samping tombol WhatsApp
nav_target = '''        <!-- Tombol Kontak Konsultasi -->
        <div class="flex items-center gap-3">'''

nav_replacement = '''        <!-- Tombol Kontak & QRIS -->
        <div class="flex items-center gap-2 sm:gap-3">
          <button onclick="openQrisModal()" type="button"
             class="px-3 py-2 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-xs flex items-center gap-1.5 transition shadow-sm">
            <span>💳</span> <span class="hidden sm:inline">Bayar</span> <span>QRIS</span>
          </button>'''

if nav_target in text and nav_replacement not in text:
    text = text.replace(nav_target, nav_replacement)
    print("[✓] Tombol QRIS di navbar berhasil ditambahkan!")

# 2. Tambah Section Kalkulator Interaktif sebelum Section Portofolio
calc_target = '''  <!-- ==================== 7. PORTOFOLIO IMPLEMENTASI & KARYA REKAYASA ==================== -->'''

calc_section = '''  <!-- ==================== KALKULATOR INTERAKTIF ESTIMASI BIAYA ==================== -->
  <section id="kalkulator" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-4xl mx-auto px-4 sm:px-6">
      <div class="text-center max-w-2xl mx-auto mb-10">
        <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Simulasi Biaya Cepat</span>
        <h2 class="serif-heading text-2xl sm:text-3xl font-bold text-slate-900 mt-1">Kalkulator Estimasi Layanan</h2>
        <p class="text-slate-600 text-xs sm:text-sm mt-2">
          Hitung rincian biaya refill gas portable atau cetak berkas skripsi Anda secara instan dan transparan.
        </p>
      </div>

      <!-- Tab Switcher -->
      <div class="flex justify-center mb-8">
        <div class="inline-flex rounded-xl bg-slate-100 p-1 border border-slate-200 text-xs font-bold">
          <button id="tabGasBtn" onclick="switchCalcTab('gas')" type="button"
                  class="px-5 py-2.5 rounded-lg bg-white text-emerald-800 shadow-sm transition">
            🔥 Refill Gas Kalimantan
          </button>
          <button id="tabPrintBtn" onclick="switchCalcTab('print')" type="button"
                  class="px-5 py-2.5 rounded-lg text-slate-600 hover:text-slate-900 transition">
            📄 Cetak / Print HVS Skripsi
          </button>
        </div>
      </div>

      <!-- Tab 1: Kalkulator Gas -->
      <div id="calcGasBox" class="paper-card p-6 sm:p-8 rounded-2xl bg-white border border-slate-200">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div class="space-y-4 text-xs">
            <div>
              <label class="block font-bold text-slate-800 mb-1">Pilih Cabang Pengambilan:</label>
              <select id="gasCabang" class="w-full p-2.5 rounded-lg border border-slate-300 text-xs bg-slate-50 font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none" onchange="calculateGas()">
                <option value="Banjarmasin (Komplek The Green Rahayu 2)">Banjarmasin — Komplek The Green Rahayu 2</option>
                <option value="Palangka Raya (Toko Karya Perdana)">Palangka Raya — Toko Karya Perdana (Jl. Seth Adji)</option>
                <option value="Balikpapan (Lamaru)">Balikpapan — Jln. Mulawarman, Lamaru</option>
              </select>
            </div>

            <div>
              <label class="block font-bold text-slate-800 mb-1">Jenis Layanan:</label>
              <div class="grid grid-cols-2 gap-2">
                <label class="flex items-center gap-2 p-2.5 rounded-lg border border-slate-200 cursor-pointer bg-slate-50 has-[:checked]:bg-emerald-50 has-[:checked]:border-emerald-500">
                  <input type="radio" name="gasType" value="refill" checked class="text-emerald-700" onchange="calculateGas()">
                  <span>Isi Ulang (Rp 12rb)</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 rounded-lg border border-slate-200 cursor-pointer bg-slate-50 has-[:checked]:bg-emerald-50 has-[:checked]:border-emerald-500">
                  <input type="radio" name="gasType" value="new" class="text-emerald-700" onchange="calculateGas()">
                  <span>Tabung Baru (Rp 20rb)</span>
                </label>
              </div>
            </div>

            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="font-bold text-slate-800">Jumlah Botol Tabung:</label>
                <span id="gasQtyLabel" class="font-bold text-emerald-800 text-sm">3 Botol</span>
              </div>
              <input id="gasQty" type="range" min="1" max="25" value="3" class="w-full accent-emerald-700 cursor-pointer" oninput="calculateGas()">
              <div class="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>1 Botol</span>
                <span>Borongan &gt;= 5 Botol (Hemat Rp 5rb)</span>
                <span>25 Botol</span>
              </div>
            </div>
          </div>

          <!-- Ringkasan Perhitungan Gas -->
          <div class="p-6 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col justify-between">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Perkiraan Biaya</span>
            <div class="my-4">
              <div id="gasTotalPrice" class="serif-heading text-3xl sm:text-4xl font-bold text-emerald-800">Rp 36.000</div>
              <div id="gasPromoNote" class="text-[11px] text-slate-500 mt-1">Tarif resmi Rp 12.000 / botol</div>
            </div>
            <div class="space-y-2">
              <button onclick="openQrisModal()" type="button"
                 class="w-full py-2.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-xs transition">
                💳 Bayar Langsung via QRIS
              </button>
              <a id="gasWaBtn" href="https://wa.me/6285155133070" target="_blank"
                 class="block w-full py-2.5 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs transition shadow-sm">
                Pesan Gas via WhatsApp →
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab 2: Kalkulator Print HVS -->
      <div id="calcPrintBox" class="paper-card p-6 sm:p-8 rounded-2xl bg-white border border-slate-200 hidden">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div class="space-y-4 text-xs">
            <div>
              <label class="block font-bold text-slate-800 mb-1">Jumlah Halaman Hitam-Putih (Rp 400/lbr):</label>
              <input id="printBwQty" type="number" min="0" value="50" class="w-full p-2.5 rounded-lg border border-slate-300 text-xs bg-slate-50 font-medium focus:ring-2 focus:ring-blue-500 focus:outline-none" oninput="calculatePrint()">
            </div>

            <div>
              <label class="block font-bold text-slate-800 mb-1">Jumlah Halaman Berwarna (Rp 800/lbr):</label>
              <input id="printColorQty" type="number" min="0" value="10" class="w-full p-2.5 rounded-lg border border-slate-300 text-xs bg-slate-50 font-medium focus:ring-2 focus:ring-blue-500 focus:outline-none" oninput="calculatePrint()">
            </div>

            <div>
              <label class="block font-bold text-slate-800 mb-1">Jumlah Rangkap / Eksemplar:</label>
              <input id="printCopies" type="number" min="1" max="10" value="2" class="w-full p-2.5 rounded-lg border border-slate-300 text-xs bg-slate-50 font-medium focus:ring-2 focus:ring-blue-500 focus:outline-none" oninput="calculatePrint()">
            </div>
          </div>

          <!-- Ringkasan Perhitungan Print -->
          <div class="p-6 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col justify-between">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Total Biaya Cetak Naskah</span>
            <div class="my-4">
              <div id="printTotalPrice" class="serif-heading text-3xl sm:text-4xl font-bold text-blue-800">Rp 56.000</div>
              <div id="printDetailNote" class="text-[11px] text-slate-500 mt-1">2 rangkap (100 lbr BW + 20 lbr Warna)</div>
            </div>
            <div class="space-y-2">
              <button onclick="openQrisModal()" type="button"
                 class="w-full py-2.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-xs transition">
                💳 Bayar Langsung via QRIS
              </button>
              <a id="printWaBtn" href="https://wa.me/6285155133070" target="_blank"
                 class="block w-full py-2.5 rounded-lg bg-blue-700 hover:bg-blue-800 text-white font-bold text-xs transition shadow-sm">
                Kirim Dokumen via WhatsApp →
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  ''' + calc_target

if calc_target in text and "<!-- ==================== KALKULATOR INTERAKTIF ESTIMASI BIAYA ==================== -->" not in text:
    text = text.replace(calc_target, calc_section)
    print("[✓] Section kalkulator interaktif berhasil disuntikkan!")

# 3. Tambah Modal QRIS dan Script JavaScript sebelum </body>
qris_modal = '''  <!-- ==================== 12. POP-UP MODAL QRIS RESMI ==================== -->
  <div id="qrisModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-300">
    <div class="relative w-full max-w-sm bg-white rounded-3xl p-6 border border-slate-200 shadow-2xl text-center transform scale-95 transition-transform duration-300" id="qrisBox">
      <!-- Tombol Tutup -->
      <button onclick="closeQrisModal()" type="button" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 flex items-center justify-center font-bold text-sm transition">
        ✕
      </button>

      <span class="text-[10px] font-bold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full uppercase tracking-wider border border-emerald-200">
        QRIS Nasional • Bebas Biaya Admin
      </span>
      
      <h3 class="serif-heading text-lg font-bold text-slate-900 mt-2">BIT &amp; BEAN</h3>
      <p class="text-xs text-slate-500">NMID: <b class="text-slate-800">ID1025428743757</b> (Noura Studio)</p>

      <!-- Gambar Barcode QRIS Asli -->
      <div class="my-4 p-2 bg-white rounded-2xl border border-slate-200 shadow-sm inline-block">
        <img src="/qris_bit_bean.png" alt="QRIS BIT & BEAN Noura Studio" class="w-56 h-auto mx-auto rounded-xl">
      </div>

      <div class="text-[11px] text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1 text-left">
        <div><b>1. Buka Aplikasi Pembayaran:</b> BCA, Mandiri, BRI, BNI, GoPay, OVO, DANA, ShopeePay.</div>
        <div><b>2. Scan Barcode:</b> Arahkan kamera ke QRIS di atas.</div>
        <div><b>3. Masukkan Nominal:</b> Sesuai pesanan gas, bimbingan, atau kopi.</div>
      </div>

      <div class="mt-4 pt-3 border-t border-slate-100 flex flex-col gap-2">
        <a href="https://wa.me/6285155133070?text=Halo%20Ibu%20Ir.%20Nor%20Anisa%2C%20saya%20sudah%20melakukan%20pembayaran%20via%20QRIS" target="_blank"
           class="w-full py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs transition shadow-sm">
          Konfirmasi Bukti Transfer via WhatsApp →
        </a>
        <button onclick="closeQrisModal()" type="button" class="w-full py-1.5 text-xs text-slate-500 hover:text-slate-700 font-semibold">
          Tutup Jendela
        </button>
      </div>
    </div>
  </div>

  <!-- JavaScript Logika Kalkulator & QRIS Modal -->
  <script>
    function openQrisModal() {
      const modal = document.getElementById('qrisModal');
      const box = document.getElementById('qrisBox');
      modal.classList.remove('hidden');
      setTimeout(() => {
        modal.classList.remove('opacity-0');
        box.classList.remove('scale-95');
        box.classList.add('scale-100');
      }, 10);
    }

    function closeQrisModal() {
      const modal = document.getElementById('qrisModal');
      const box = document.getElementById('qrisBox');
      modal.classList.add('opacity-0');
      box.classList.remove('scale-100');
      box.classList.add('scale-95');
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 250);
    }

    // Tutup jika klik latar belakang
    document.addEventListener('click', function(e) {
      const modal = document.getElementById('qrisModal');
      const box = document.getElementById('qrisBox');
      if (modal && !modal.classList.contains('hidden') && e.target === modal) {
        closeQrisModal();
      }
    });

    // Logika Tab Kalkulator
    function switchCalcTab(tab) {
      const gasBox = document.getElementById('calcGasBox');
      const printBox = document.getElementById('calcPrintBox');
      const gasBtn = document.getElementById('tabGasBtn');
      const printBtn = document.getElementById('tabPrintBtn');

      if (tab === 'gas') {
        gasBox.classList.remove('hidden');
        printBox.classList.add('hidden');
        gasBtn.className = 'px-5 py-2.5 rounded-lg bg-white text-emerald-800 shadow-sm transition';
        printBtn.className = 'px-5 py-2.5 rounded-lg text-slate-600 hover:text-slate-900 transition';
      } else {
        gasBox.classList.add('hidden');
        printBox.classList.remove('hidden');
        printBtn.className = 'px-5 py-2.5 rounded-lg bg-white text-blue-800 shadow-sm transition';
        gasBtn.className = 'px-5 py-2.5 rounded-lg text-slate-600 hover:text-slate-900 transition';
      }
    }

    // Hitung Estimasi Gas
    function calculateGas() {
      const qty = parseInt(document.getElementById('gasQty').value) || 1;
      const type = document.querySelector('input[name="gasType"]:checked').value;
      const cabang = document.getElementById('gasCabang').value;
      document.getElementById('gasQtyLabel').innerText = qty + ' Botol';

      let unitPrice = (type === 'refill') ? 12000 : 20000;
      let total = qty * unitPrice;
      let note = 'Tarif Rp ' + unitPrice.toLocaleString('id-ID') + ' / botol';

      // Promo borongan: Jika refill >= 5 botol, diskon Rp 5.000 per 5 botol
      if (type === 'refill' && qty >= 5) {
        const bonusBatches = Math.floor(qty / 5);
        const discount = bonusBatches * 5000;
        total -= discount;
        note = 'Promo borongan hemat Rp ' + discount.toLocaleString('id-ID') + ' diterapkan!';
      }

      document.getElementById('gasTotalPrice').innerText = 'Rp ' + total.toLocaleString('id-ID');
      document.getElementById('gasPromoNote').innerText = note;

      const waMsg = encodeURIComponent('Halo Admin, mau pesan ' + (type === 'refill' ? 'Refill ' : 'Tabung Baru ') + qty + ' botol di cabang ' + cabang + ' (Estimasi: Rp ' + total.toLocaleString('id-ID') + ')');
      document.getElementById('gasWaBtn').href = 'https://wa.me/6285155133070?text=' + waMsg;
    }

    // Hitung Estimasi Print HVS
    function calculatePrint() {
      const bw = parseInt(document.getElementById('printBwQty').value) || 0;
      const color = parseInt(document.getElementById('printColorQty').value) || 0;
      const copies = parseInt(document.getElementById('printCopies').value) || 1;

      const totalPerCopy = (bw * 400) + (color * 800);
      const grandTotal = totalPerCopy * copies;

      document.getElementById('printTotalPrice').innerText = 'Rp ' + grandTotal.toLocaleString('id-ID');
      document.getElementById('printDetailNote').innerText = copies + ' rangkap (' + (bw * copies) + ' lbr BW + ' + (color * copies) + ' lbr Warna)';

      const waMsg = encodeURIComponent('Halo Ibu Ir. Nor Anisa, mau cetak naskah skripsi HVS: ' + bw + ' hal BW, ' + color + ' hal Warna, sebanyak ' + copies + ' rangkap (Estimasi: Rp ' + grandTotal.toLocaleString('id-ID') + ')');
      document.getElementById('printWaBtn').href = 'https://wa.me/6285155133070?text=' + waMsg;
    }

    // Inisialisasi hitungan
    calculateGas();
    calculatePrint();
  </script>
'''

if "<!-- ==================== 12. POP-UP MODAL QRIS RESMI ==================== -->" not in text:
    text = text.replace("</body>", qris_modal + "\n</body>")
    print("[✓] Modal QRIS dan Script JavaScript berhasil disuntikkan!")

with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
    f.write(text)

print("[✓] build_human_crafted_site.py berhasil diperbarui dengan QRIS & Kalkulator!")
