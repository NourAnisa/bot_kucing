<?php
header('Content-Type: text/plain; charset=utf-8');

$sourceDir = __DIR__; // /home/ub639ap0/public_html/nourastudio.co-id.id/public
$targetDir = dirname(dirname($sourceDir)); // /home/ub639ap0/public_html

echo "Source Dir: " . $sourceDir . "\n";
echo "Target Dir: " . $targetDir . "\n\n";

if (!is_dir($targetDir)) {
    echo "ERROR: Target directory does not exist!\n";
    exit;
}

$filesToSync = [
    'index.html',
    'robots.txt',
    'sitemap.xml',
    'telegram_webhook.php',
    'sync_wa_auth.php',
    'google1bfaed16ab67c926.html',
    'qris_bit_bean.png'
];

// Otomatis deteksi file verifikasi dan gambar
foreach (glob($sourceDir . '/google*.html') as $gfile) {
    $bname = basename($gfile);
    if (!in_array($bname, $filesToSync)) {
        $filesToSync[] = $bname;
    }
}
foreach (glob($sourceDir . '/*.{png,jpg,jpeg,svg,ico}', GLOB_BRACE) as $imgfile) {
    $bname = basename($imgfile);
    if (!in_array($bname, $filesToSync)) {
        $filesToSync[] = $bname;
    }
}

foreach ($filesToSync as $file) {
    $src = $sourceDir . '/' . $file;
    $dst = $targetDir . '/' . $file;
    if (file_exists($src)) {
        if (copy($src, $dst)) {
            echo "[SUCCESS] Copied {$file} (" . filesize($dst) . " bytes)\n";
        } else {
            echo "[FAILED] Could not copy {$file}\n";
        }
    } else {
        echo "[WARNING] Source file {$file} not found\n";
    }
}

// Juga buat .htaccess di public_html untuk memastikan DirectoryIndex mengutamakan index.html
$htaccessContent = "DirectoryIndex index.html index.php\n";
$htaccessTarget = $targetDir . '/.htaccess';
if (!file_exists($htaccessTarget)) {
    file_put_contents($htaccessTarget, $htaccessContent);
    echo "[SUCCESS] Created .htaccess with DirectoryIndex index.html\n";
} else {
    $existingHt = file_get_contents($htaccessTarget);
    if (strpos($existingHt, 'DirectoryIndex') === false) {
        file_put_contents($htaccessTarget, $htaccessContent . $existingHt);
        echo "[SUCCESS] Prepend DirectoryIndex to existing .htaccess\n";
    }
}

echo "\nFiles currently in target " . $targetDir . ":\n";
$currentFiles = scandir($targetDir);
foreach ($currentFiles as $f) {
    if ($f !== '.' && $f !== '..') {
        echo " - " . $f . " (" . (is_dir($targetDir . '/' . $f) ? 'DIR' : filesize($targetDir . '/' . $f) . ' bytes') . ")\n";
    }
}

echo "\nSYNC COMPLETE! Visit https://nourastudio.co-id.id/ to verify.\n";
