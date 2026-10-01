$action = New-ScheduledTaskAction -Execute 'python.exe' -Argument '"C:\Users\Nor Anisa\Downloads\SondeR-Cat-main\ai_office\morning_report.py"' -WorkingDirectory 'C:\Users\Nor Anisa\Downloads\SondeR-Cat-main\ai_office'
$trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM
Register-ScheduledTask -TaskName 'SondeR_Morning_Report' -Action $action -Trigger $trigger -Description 'Laporan Harian Pagi AI Office & WhatsApp Nor Anisa' -Force
Write-Host "Task SondeR_Morning_Report registered successfully!"
