<?php
/**
 * Cloud WA Auth Session Backup & Restore for Noura Studio
 * Menyimpan backup sesi Baileys WhatsApp secara permanen di hosting LiteSpeed.
 */
header('Content-Type: application/json');

$SECRET_TOKEN = 'noranisa_content_secret_2026';
$BACKUP_FILE = __DIR__ . '/wa_auth_backup.json';

// GET: Cek status atau download backup
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($BACKUP_FILE)) {
        $data = json_decode(file_get_contents($BACKUP_FILE), true);
        if (isset($_GET['token']) && $_GET['token'] === $SECRET_TOKEN) {
            echo json_encode($data);
        } else {
            echo json_encode([
                'status' => 'exists',
                'file_count' => isset($data['files']) ? count($data['files']) : 0,
                'updated_at' => $data['updated_at'] ?? 'unknown'
            ]);
        }
    } else {
        echo json_encode(['status' => 'none']);
    }
    exit;
}

// POST: Simpan backup sesi
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw = file_get_contents('php://input');
    $payload = json_decode($raw, true);

    if (!isset($payload['token']) || $payload['token'] !== $SECRET_TOKEN) {
        http_response_code(403);
        echo json_encode(['error' => 'Unauthorized']);
        exit;
    }

    if (empty($payload['files'])) {
        http_response_code(400);
        echo json_encode(['error' => 'No files provided']);
        exit;
    }

    $backupData = [
        'updated_at' => date('Y-m-d H:i:s'),
        'files' => $payload['files']
    ];

    file_put_contents($BACKUP_FILE, json_encode($backupData));
    echo json_encode(['ok' => true, 'saved_files' => count($payload['files'])]);
    exit;
}
