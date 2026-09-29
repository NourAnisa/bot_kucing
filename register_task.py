import subprocess
import sys
from pathlib import Path

python_exe = sys.executable
script_path = str(Path(r"c:\Users\Nor Anisa\Downloads\SondeR-Cat-main\auto_content_engine.py").resolve())
task_cmd = f'"{python_exe}" "{script_path}"'

cmd = [
    "schtasks", "/create",
    "/tn", "SondeR_Auto_Content",
    "/tr", task_cmd,
    "/sc", "WEEKLY",
    "/d", "MON,THU",
    "/st", "06:30",
    "/f"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout.strip())
print("STDERR:", res.stderr.strip())
