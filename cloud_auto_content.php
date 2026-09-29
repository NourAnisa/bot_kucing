<?php
/**
 * SondeR 100% Cloud Autonomous Content Engine
 * Berjalan langsung di server LiteSpeed Hosting tanpa memerlukan laptop menyala sama sekali.
 * Terkoneksi ke Hugging Face Bansos AI & Telegram Bot (@noranisa_bot)
 */

header('Content-Type: application/json; charset=utf-8');

// Proteksi token keamanan
$SECRET_TOKEN = "noranisa_content_secret_2026";
$incomingToken = $_GET['token'] ?? '';

if ($incomingToken !== $SECRET_TOKEN) {
    http_response_code(403);
    echo json_encode(["status" => "error", "message" => "Akses ditolak: token keamanan tidak valid."]);
    exit;
}

$BANSOS_URL = "https://noranisa-bansos.hf.space/v1/chat/completions";
$BANSOS_KEY = "bansos";
$BANSOS_MODEL = "ling-3.0-flash-fin-free";
$TG_TOKEN = "8664429930:AAGCvxMhh50wVBmHzZm48QA_L40wrt6rcx0";

$publicHtmlDir = dirname(__DIR__); // /home/.../public_html
$indexPath = $publicHtmlDir . '/index.html';
$sitemapPath = $publicHtmlDir . '/sitemap.xml';
$articlesDbPath = __DIR__ . '/cloud_articles.json';

if (!file_exists($indexPath)) {
    // Fallback jika berada di level yang sama
    $indexPath = __DIR__ . '/index.html';
    $sitemapPath = __DIR__ . '/sitemap.xml';
}

$topics = [
    [
        "topic" => "Strategi Membangun Basis Data Relasional untuk Skripsi Sistem Informasi yang Tahan Uji Penguji",
        "category" => "Tips Akademik & Pemrograman",
        "theme" => "blue",
        "wa_text" => "Halo Ibu Ir. Nor Anisa, mau konsultasi basis data skripsi"
    ],
    [
        "topic" => "Efisiensi Biaya Bahan Bakar Kuliner Kalimantan: Solusi Refill Gas Portable Rp 12.000 untuk Usaha Grill & Katering",
        "category" => "Panduan Energi & Usaha",
        "theme" => "emerald",
        "wa_text" => "Halo Admin, mau tanya refill gas portable untuk kebutuhan usaha kuliner"
    ],
    [
        "topic" => "Menjaga Konsentrasi Saat Analisis Data Ilmiah: Racikan Kopi Susu Aren Asli Bit & Bean yang Bersahabat dengan Lambung",
        "category" => "Kultur Kopi & Produktivitas",
        "theme" => "amber",
        "wa_text" => "Halo Admin, mau pesan kopi literan Bit and Bean"
    ],
    [
        "topic" => "Panduan Pengujian Sistem Black Box & White Box pada Skripsi Informatika Sesuai Standar IEEE",
        "category" => "Tips Akademik & Pemrograman",
        "theme" => "blue",
        "wa_text" => "Halo Ibu Ir. Nor Anisa, mau bimbingan pengujian sistem skripsi"
    ],
    [
        "topic" => "Persiapan Perlengkapan Memasak Pendakian Alam Terbuka di Kalimantan: Keunggulan Canister Ulir Lindal Valve",
        "category" => "Panduan Outdoor Kalimantan",
        "theme" => "emerald",
        "wa_text" => "Halo Admin, mau konsultasi gas canister untuk pendakian outdoor"
    ]
];

// Muat database artikel
$articles = [];
if (file_exists($articlesDbPath)) {
    $articles = json_decode(file_get_contents($articlesDbPath), true) ?: [];
}

$existingTitles = array_column($articles, 'title');
$selectedTopic = null;
foreach ($topics as $t) {
    if (!in_array($t['topic'], $existingTitles)) {
        $selectedTopic = $t;
        break;
    }
}
if (!$selectedTopic) {
    $selectedTopic = $topics[array_rand($topics)];
}

// Panggil Bansos AI via cURL
$prompt = "Anda adalah asisten akademik resmi untuk Ir. Nor Anisa, S.Kom., M.Kom. (Dosen Informatika di Kalimantan, Insinyur Profesional, pembina Bimbingan & Konsultasi Skripsi IT bergaransi pendampingan, Refill Gas Portable Rp 12.000 di 3 cabang Banjarmasin/Palangka Raya/Balikpapan, dan Bit & Bean Coffee).\n"
    . "Buatkan SATU artikel edukasi SEO yang elegan, santun, dan berbobot akademis.\n"
    . "Topik: " . $selectedTopic['topic'] . "\n"
    . "Kategori: " . $selectedTopic['category'] . "\n\n"
    . "ATURAN KETAT:\n"
    . "- DILARANG menggunakan kata 'joki' atau 'joki skripsi'. Selalu gunakan 'Bimbingan & Konsultasi Skripsi' atau 'Asistensi Pemrograman'.\n"
    . "- JANGAN sebut SOP keselamatan uji rendam air atau timbangan digital.\n"
    . "- Selalu sebut nama Ir. Nor Anisa, S.Kom., M.Kom.\n"
    . "- Format respon JSON murni:\n"
    . '{"title":"' . $selectedTopic['topic'] . '","excerpt":"Ringkasan 2-3 kalimat menarik, mengalir, dan informatif.","category":"' . $selectedTopic['category'] . '","theme":"' . $selectedTopic['theme'] . '","wa_text":"' . $selectedTopic['wa_text'] . '"}';

$payload = json_encode([
    'model' => $BANSOS_MODEL,
    'messages' => [
        ['role' => 'system', 'content' => 'You are a professional academic editor outputting strictly valid JSON.'],
        ['role' => 'user', 'content' => $prompt]
    ],
    'temperature' => 0.6,
    'max_tokens' => 600
]);

$ch = curl_init($BANSOS_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $BANSOS_KEY,
    'User-Agent: SondeR-CloudAutoContent/1.0'
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 30);
$aiRes = curl_exec($ch);
curl_close($ch);

$newArticle = null;
if ($aiRes) {
    $aiData = json_decode($aiRes, true);
    $text = $aiData['choices'][0]['message']['content'] ?? '';
    if (strpos($text, '```') !== false) {
        $text = preg_replace('/^```(?:json)?\s*|\s*```$/i', '', trim($text));
    }
    $newArticle = json_decode($text, true);
}

if (!$newArticle || empty($newArticle['title'])) {
    $newArticle = [
        "title" => $selectedTopic['topic'],
        "excerpt" => "Telaah dan panduan praktis dari Ir. Nor Anisa, S.Kom., M.Kom. untuk mendukung civitas akademika dan masyarakat Kalimantan mencapai efisiensi, akurasi, dan kepastian mutu terbaik.",
        "category" => $selectedTopic['category'],
        "theme" => $selectedTopic['theme'],
        "wa_text" => $selectedTopic['wa_text']
    ];
}

$newArticle['id'] = 'cloud-art-' . time();
$newArticle['date'] = date('Y-m-d');
$newArticle['author'] = 'Ir. Nor Anisa, S.Kom., M.Kom.';

// Masukkan ke database artikel
array_unshift($articles, $newArticle);
if (count($articles) > 15) $articles = array_slice($articles, 0, 15);
file_put_contents($articlesDbPath, json_encode($articles, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

// Render Kartu HTML
$cardsHtml = "";
foreach (array_slice($articles, 0, 6) as $art) {
    $thm = $art['theme'] ?? 'blue';
    $badge = ($thm === 'emerald') ? 'text-emerald-800' : (($thm === 'amber') ? 'text-amber-800' : 'text-blue-800');
    $link = ($thm === 'emerald') ? 'text-emerald-800 hover:text-emerald-950' : (($thm === 'amber') ? 'text-amber-800 hover:text-amber-950' : 'text-blue-800 hover:text-blue-950');
    $wa = "https://wa.me/6285155133070?text=" . urlencode($art['wa_text'] ?? 'Halo Ibu Ir. Nor Anisa');

    $cardsHtml .= '        <!-- ' . $art['id'] . ' -->
        <article class="paper-card p-6 rounded-2xl flex flex-col justify-between bg-white">
          <div>
            <div class="text-[11px] font-bold ' . $badge . ' uppercase mb-2">' . htmlspecialchars($art['category']) . '</div>
            <h3 class="serif-heading text-base font-bold text-slate-900 leading-snug">
              ' . htmlspecialchars($art['title']) . '
            </h3>
            <p class="text-xs text-slate-600 mt-3 leading-relaxed">
              ' . htmlspecialchars($art['excerpt']) . '
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="text-[11px] text-slate-400 font-medium">Ditulis: ' . $art['date'] . '</span>
            <a href="' . $wa . '" target="_blank"
               class="font-bold ' . $link . ' transition flex items-center gap-1">
              <span>Konsultasi via WA</span> <span>→</span>
            </a>
          </div>
        </article>' . "\n\n";
}

// Suntikkan ke index.html
if (file_exists($indexPath)) {
    $html = file_get_contents($indexPath);
    $startTag = '<!-- ==================== 8. ARTIKEL & CATATAN EDUKASI ==================== -->';
    $endTag = '<!-- ==================== 9. FAQ / TANYA JAWAB ==================== -->';

    if (strpos($html, $startTag) !== false && strpos($html, $endTag) !== false) {
        $newSec = $startTag . "\n"
            . '  <section id="artikel" class="py-20 bg-[#faf9f6] border-b border-slate-200">' . "\n"
            . '    <div class="max-w-6xl mx-auto px-4 sm:px-6">' . "\n"
            . '      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">' . "\n"
            . '        <div>' . "\n"
            . '          <span class="text-xs font-bold text-emerald-800 uppercase tracking-wider">Artikel &amp; Catatan Edukatif</span>' . "\n"
            . '          <h2 class="serif-heading text-2xl sm:text-3xl font-bold text-slate-900 mt-1">Panduan Praktis &amp; Analisis Terpercaya</h2>' . "\n"
            . '          <p class="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">' . "\n"
            . '            Ditulis langsung oleh <b>Ir. Nor Anisa, S.Kom., M.Kom.</b> untuk memberikan referensi mendalam bagi masyarakat di Kalimantan.' . "\n"
            . '          </p>' . "\n"
            . '        </div>' . "\n"
            . '        <div class="text-xs text-slate-500 font-medium bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm">' . "\n"
            . '          📚 Total: <b>' . count($articles) . ' Artikel Edukasi</b> Terpublikasi' . "\n"
            . '        </div>' . "\n"
            . '      </div>' . "\n\n"
            . '      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">' . "\n"
            . $cardsHtml
            . '      </div>' . "\n"
            . '    </div>' . "\n"
            . '  </section>' . "\n\n  ";

        $before = substr($html, 0, strpos($html, $startTag));
        $after = substr($html, strpos($html, $endTag));
        file_put_contents($indexPath, $before . $newSec . $after);
    }
}

// Perbarui sitemap.xml
if (file_exists($sitemapPath)) {
    $today = date('Y-m-d');
    $sitemapContent = '<?xml version="1.0" encoding="UTF-8"?>' . "\n"
        . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n"
        . '  <url>' . "\n"
        . '    <loc>https://nourastudio.co-id.id/</loc>' . "\n"
        . '    <lastmod>' . $today . '</lastmod>' . "\n"
        . '    <changefreq>daily</changefreq>' . "\n"
        . '    <priority>1.0</priority>' . "\n"
        . '  </url>' . "\n"
        . '</urlset>';
    file_put_contents($sitemapPath, $sitemapContent);
}

// Kirim notifikasi Telegram ke log/chat jika ada
$notifMsg = "📰 *[CLOUD AUTO-PUBLISHER]*\nArtikel baru berhasil terbit langsung dari server cloud:\n\n"
    . "👤 *Penulis:* Ir. Nor Anisa, S.Kom., M.Kom.\n"
    . "📑 *Judul:* " . $newArticle['title'] . "\n"
    . "🏷️ *Kategori:* " . $newArticle['category'] . "\n"
    . "🌐 *Lihat:* https://nourastudio.co-id.id/#artikel\n\n"
    . "✅ *Status:* Server hosting cloud memproses mandiri tanpa laptop menyala.";

echo json_encode([
    "status" => "success",
    "mode" => "100% Cloud Server Autopilot",
    "article" => $newArticle,
    "total_articles" => count($articles),
    "timestamp" => date('Y-m-d H:i:s')
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
