param(
    [string]$Status = "info",
    [string]$Title = "Notifikasi Terminal",
    [string]$Message = "Tugas selesai!"
)
try {
    $body = @{ status = $Status; title = $Title; message = $Message } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:19842/notify" -Method POST -ContentType "application/json" -Body $body | Out-Null
} catch {
    Write-Warning "NekoCat HTTP webhook unreachable."
}
