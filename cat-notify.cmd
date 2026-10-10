@echo off
set "STATUS=%~1"
set "TITLE=%~2"
set "MSG=%~3"
if "%STATUS%"=="" set "STATUS=info"
if "%TITLE%"=="" set "TITLE=Notifikasi"
if "%MSG%"=="" set "MSG=Pesan selesai!"

powershell -NoProfile -Command "try { $body = @{ status = '%STATUS%'; title = '%TITLE%'; message = '%MSG%' } | ConvertTo-Json; Invoke-RestMethod -Uri 'http://127.0.0.1:19842/notify' -Method POST -ContentType 'application/json' -Body $body | Out-Null } catch {}" >nul 2>&1
