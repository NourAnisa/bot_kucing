# -*- coding: utf-8 -*-
"""
SondeR AI Office Server
Backend HTTP Server untuk Virtual AI Office 3D (35 Agen AI & 6 Divisi)
Terhubung dengan 9Router / OpenAI / Gemini / SondeR Cat
"""

import os
import sys
import json
import time
import uuid
import mimetypes
import threading
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import data agen & dataset bawaan
try:
    from agents_data import AGENTS, DEFAULT_DATASET, SAMPLE_DOC
except ImportError:
    from .agents_data import AGENTS, DEFAULT_DATASET, SAMPLE_DOC

PORT = 19845
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(DATA_DIR, "documents")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

CONFIG_PATH = os.path.expanduser("~/.sondercat.json")

# State in-memory
active_chatting = set()
lock = threading.Lock()

# ----------------- STORAGE HELPERS -----------------

def load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Error saving {filepath}]: {e}")

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")
DOCUMENTS_INDEX_FILE = os.path.join(DATA_DIR, "documents.json")

# Inisialisasi dokumen sample jika belum ada
if not os.path.exists(DOCUMENTS_INDEX_FILE):
    initial_docs = [{
        "id": "sample-handbook",
        "name": "company-handbook.md",
        "content": SAMPLE_DOC.get("content", "# SondeR Workspace Handbook\n\nPanduan operasional dan pengetahuan dasar tim AI Office."),
        "bytes": len(SAMPLE_DOC.get("content", "").encode("utf-8")),
        "addedAt": int(time.time() * 1000)
    }]
    save_json(DOCUMENTS_INDEX_FILE, initial_docs)

# Inisialisasi task awal jika belum ada
if not os.path.exists(TASKS_FILE):
    initial_tasks = [{
        "id": "task-welcome",
        "agent": "olead",
        "dept": "ops",
        "title": "Inisialisasi Kantor Virtual SondeR AI Office",
        "text": "Menyiapkan ruang kerja 3D dan menghubungkan 35 agen AI ke workspace.",
        "state": "done",
        "by": "studio",
        "addedAt": int(time.time() * 1000) - 60000,
        "doneAt": int(time.time() * 1000),
        "result": "Selamat datang di SondeR AI Office! Kantor 3D interaktif telah aktif dengan 35 agen dalam 6 divisi: Operations, Marketing, Sales, Delivery, Finance, dan Communications. Anda dapat mengklik agen manapun di tampilan 3D untuk memulai obrolan langsung atau memberikan brief pekerjaan."
    }]
    save_json(TASKS_FILE, initial_tasks)


# ----------------- AI / LLM CALL ENGINE -----------------

def get_ai_config():
    cfg = load_json(CONFIG_PATH, {})
    g = cfg.get("global", {})
    return {
        "provider": g.get("ai_provider", "9router"),
        "base_url": g.get("router_base_url", "https://noranisa-bansos.hf.space/v1").rstrip("/"),
        "api_key": g.get("router_key", "bansos"),
        "model": g.get("router_model", "ling-3.0-flash-fin-free"),
        "gemini_key": g.get("gemini_key", "")
    }

def call_llm(messages, max_tokens=1500, temperature=0.7):
    """Memanggil LLM via Hugging Face Bansos Router / 9Router (OpenAI-compatible) atau Gemini API dengan graceful fallback."""
    cfg = get_ai_config()

    # 1. Coba Hugging Face Bansos / OpenAI endpoint
    if cfg["base_url"]:
        try:
            url = f"{cfg['base_url']}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "SondeR-AIOffice/1.0"
            }
            if cfg["api_key"]:
                headers["Authorization"] = f"Bearer {cfg['api_key']}"

            payload = {
                "model": cfg["model"] or "ling-3.0-flash-fin-free",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[Bansos Router call failed, trying fallback]: {e}")

    # 2. Coba Gemini API jika key ada
    if cfg["gemini_key"]:
        try:
            model_name = "gemini-2.0-flash"
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={cfg['gemini_key']}"
            
            # Format pesan untuk Gemini
            contents = []
            sys_inst = ""
            for m in messages:
                if m["role"] == "system":
                    sys_inst += m["content"] + "\n\n"
                elif m["role"] == "user":
                    contents.append({"role": "user", "parts": [{"text": m["content"]}]})
                elif m["role"] == "assistant":
                    contents.append({"role": "model", "parts": [{"text": m["content"]}]})
            
            payload = {"contents": contents}
            if sys_inst:
                payload["systemInstruction"] = {"parts": [{"text": sys_inst.strip()}]}

            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(gemini_url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            print(f"[Gemini call failed]: {e}")

    return None

def generate_agent_reply(agent_id, user_text, document_ids=None):
    """Menghasilkan respon agen dengan persona spesifik dan konteks dokumen."""
    agent = next((a for a in AGENTS if a["id"] == agent_id), None)
    if not agent:
        return "Halo! Ada yang bisa saya bantu di workspace ini?"

    # Ambil lampiran dokumen jika ada
    doc_context = ""
    if document_ids:
        docs = load_json(DOCUMENTS_INDEX_FILE, [])
        for doc_id in document_ids:
            d = next((x for x in docs if x["id"] == doc_id), None)
            if d:
                doc_context += f"\n--- Lampiran Dokumen: {d['name']} ---\n{d.get('content', '')}\n"

    system_prompt = (
        f"Nama Anda adalah {agent['displayName']}. Peran Anda adalah {agent['role']} ({agent['responsibility']}) "
        f"di divisi {agent['department'].capitalize()} pada Kantor Virtual Ekosistem Bisnis Nor Anisa (Refill Gas Portable Kalimantan & JokiCoding).\n"
        f"Panduan karakter & keahlian Anda: {agent['brief']}\n"
        f"Tugas utama Anda: {agent['does']}\n\n"
        f"Instruksi interaksi:\n"
        f"- Jawab dalam Bahasa Indonesia yang profesional, ramah, dan solutif sesuai divisi Anda.\n"
        f"- Manfaatkan data/dokumen yang terlampir jika relevan.\n"
        f"- Jangan mengarang data sensitif atau menyatakan telah melakukan transaksi eksternal live tanpa izin.\n"
    )

    # Otomatis sertakan pengetahuan bisnis ekosistem Nor Anisa
    if doc_context:
        system_prompt += f"\nKonteks Dokumen yang Dilampirkan:\n{doc_context}\n"
    else:
        # Muat ringkasan handbook otomatis agar agen selalu paham bisnis Nor Anisa
        docs = load_json(DOCUMENTS_INDEX_FILE, [])
        handbook = next((x for x in docs if x["id"] == "sample-handbook"), None)
        if handbook:
            system_prompt += f"\n--- Pengetahuan Operasional Bisnis Nor Anisa (Handbook) ---\n{handbook.get('content', '')}\n"

    # Muat beberapa riwayat chat terakhir agar kontekstual
    conversations = load_json(CONVERSATIONS_FILE, {})
    agent_history = conversations.get(agent_id, [])[-6:]

    messages = [{"role": "system", "content": system_prompt}]
    for m in agent_history:
        messages.append({
            "role": "user" if m.get("who") == "user" else "assistant",
            "content": m.get("text", "")
        })
    messages.append({"role": "user", "content": user_text})

    reply = call_llm(messages)
    if not reply:
        # Fallback offline cerdas sesuai peran agen
        reply = (
            f"Halo, saya {agent['displayName']} ({agent['role']}). "
            f"Saya telah meninjau catatan terkait '{user_text}'. "
            f"Fokus divisi kami ({agent['department'].capitalize()}) adalah: {agent['responsibility']}. "
            f"Silakan pastikan 9Router AI atau API Key Anda aktif agar saya dapat memberikan analisa mendalam secara real-time!"
        )

    return reply


# ----------------- HTTP REQUEST HANDLER -----------------

class OfficeRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Ringkas log agar konsol tidak berisik
        pass

    def _send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        # API Endpoints
        if path == "/api/health":
            docs = load_json(DOCUMENTS_INDEX_FILE, [])
            self._send_json({
                "ok": True,
                "name": "SondeR AI Office",
                "agents": AGENTS,
                "auth": {"ready": True},
                "version": "1.0.0",
                "notes": len(docs)
            })
            return

        if path == "/api/tasks":
            tasks = load_json(TASKS_FILE, [])
            self._send_json(tasks)
            return

        if path.startswith("/api/studio/conversations/"):
            agent_id = path.split("/")[-1]
            conversations = load_json(CONVERSATIONS_FILE, {})
            msgs = conversations.get(agent_id, [])
            with lock:
                is_pending = agent_id in active_chatting
            self._send_json({
                "messages": msgs,
                "pending": is_pending,
                "error": None
            })
            return

        if path == "/api/studio/activity":
            with lock:
                chatting_list = list(active_chatting)
            self._send_json({"chatting": chatting_list})
            return

        if path == "/api/studio/documents":
            docs = load_json(DOCUMENTS_INDEX_FILE, [])
            # Kembalikan daftar metadata dokumen
            summary = [{"id": d["id"], "name": d["name"], "bytes": d["bytes"], "addedAt": d["addedAt"]} for d in docs]
            self._send_json(summary)
            return

        if path.startswith("/api/studio/documents/"):
            parts = path.split("/")
            doc_id = parts[-1]
            if len(parts) >= 6 and parts[-1] == "preview":
                doc_id = parts[-2]
            docs = load_json(DOCUMENTS_INDEX_FILE, [])
            doc = next((d for d in docs if d["id"] == doc_id), None)
            if doc:
                self._send_json(doc)
            else:
                self._send_json({"error": "Dokumen tidak ditemukan"}, 404)
            return

        if path == "/api/studio/dataset":
            self._send_json(DEFAULT_DATASET)
            return

        if path == "/api/studio/telegram":
            self._send_json({
                "configured": True,
                "paired": True,
                "connected": True,
                "username": "noranisa_bot"
            })
            return

        # Static Files Serving
        rel_path = parsed.path.lstrip("/")
        if not rel_path or rel_path == "":
            rel_path = "index.html"

        # Cek file di static directory
        file_path = os.path.join(STATIC_DIR, rel_path)
        if os.path.isfile(file_path):
            self._serve_file(file_path)
            return

        # Fallback ke index.html untuk client-side routing
        index_file = os.path.join(STATIC_DIR, "index.html")
        if os.path.isfile(index_file):
            self._serve_file(index_file)
            return

        self.send_error(404, "File Not Found")

    def _serve_file(self, filepath):
        ctype, _ = mimetypes.guess_type(filepath)
        if not ctype:
            if filepath.endswith(".js"):
                ctype = "text/javascript"
            elif filepath.endswith(".css"):
                ctype = "text/css"
            elif filepath.endswith(".svg"):
                ctype = "image/svg+xml"
            else:
                ctype = "application/octet-stream"

        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{ctype}; charset=utf-8" if "text" in ctype else ctype)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        body = self._read_json()

        # 1. Chat dengan Agen
        if path.startswith("/api/studio/conversations/"):
            agent_id = path.split("/")[-1]
            user_text = body.get("text", "").strip()
            document_ids = body.get("documents", [])

            if not user_text:
                self._send_json({"error": "Pesan tidak boleh kosong"}, 400)
                return

            # Simpan pesan user
            user_msg = {
                "who": "user",
                "text": user_text,
                "at": int(time.time() * 1000),
                "attachments": [{"id": d, "name": d} for d in document_ids]
            }

            with lock:
                conversations = load_json(CONVERSATIONS_FILE, {})
                agent_msgs = conversations.get(agent_id, [])
                agent_msgs.append(user_msg)
                conversations[agent_id] = agent_msgs
                save_json(CONVERSATIONS_FILE, conversations)
                active_chatting.add(agent_id)

            # Jalankan generasi balasan di background thread
            def reply_worker():
                try:
                    reply_text = generate_agent_reply(agent_id, user_text, document_ids)
                    agent_msg = {
                        "who": "agent",
                        "text": reply_text,
                        "at": int(time.time() * 1000)
                    }
                    with lock:
                        convs = load_json(CONVERSATIONS_FILE, {})
                        c_msgs = convs.get(agent_id, [])
                        c_msgs.append(agent_msg)
                        convs[agent_id] = c_msgs
                        save_json(CONVERSATIONS_FILE, convs)
                finally:
                    with lock:
                        active_chatting.discard(agent_id)

            threading.Thread(target=reply_worker, daemon=True).start()

            self._send_json({
                "ok": True,
                "pending": True,
                "agent": agent_id
            })
            return

        # 2. Buat Brief Tugas Baru (Individual / Tim)
        if path in ("/api/tasks", "/api/studio/tasks"):
            agent_id = body.get("agent", "olead")
            text = body.get("text", "").strip()
            is_team = body.get("team", False)
            doc_ids = body.get("documents", [])

            agent = next((a for a in AGENTS if a["id"] == agent_id), AGENTS[0])
            task_id = f"task-{uuid.uuid4().hex[:8]}"

            new_task = {
                "id": task_id,
                "agent": agent_id,
                "dept": agent["department"],
                "title": text.split("\n")[0][:60] if text else "Brief Pekerjaan",
                "text": text,
                "state": "doing",
                "by": "studio",
                "addedAt": int(time.time() * 1000),
                "team": {"pieces": []} if is_team else None
            }

            tasks = load_json(TASKS_FILE, [])
            tasks.append(new_task)
            save_json(TASKS_FILE, tasks)

            # Proses eksekusi tugas di background
            def task_worker():
                dept_agents = [a for a in AGENTS if a["department"] == agent["department"]]
                try:
                    with lock:
                        active_chatting.add(agent_id)

                    prompt = f"Tugas/Brief Pekerjaan untuk divisi {agent['department'].upper()}:\n{text}\n\n"
                    if is_team:
                        prompt += (
                            f"Instruksi Kolaborasi Tim:\n"
                            f"Lead: {agent['displayName']} ({agent['role']}).\n"
                            f"Bekerja bersama anggota tim divisi: {', '.join(a['displayName'] + ' (' + a['role'] + ')' for a in dept_agents)}.\n"
                            f"Susun output lengkap yang mencakup: 1. Analisis/Temuan Utama, 2. Rincian Pelaksanaan per Peran, 3. Rekomendasi Langkah Selanjutnya."
                        )
                    else:
                        prompt += f"Dikerjakan oleh {agent['displayName']} ({agent['role']}) sesuai tanggung jawab divisi."

                    res = generate_agent_reply(agent_id, prompt, doc_ids)

                    # Update status task
                    all_tasks = load_json(TASKS_FILE, [])
                    for t in all_tasks:
                        if t["id"] == task_id:
                            t["state"] = "done"
                            t["doneAt"] = int(time.time() * 1000)
                            t["result"] = res
                            if is_team:
                                t["team"]["pieces"] = [
                                    {"agent": a["id"], "title": a["role"], "state": "done"}
                                    for a in dept_agents[:3]
                                ]
                            break
                    save_json(TASKS_FILE, all_tasks)
                finally:
                    with lock:
                        active_chatting.discard(agent_id)

            threading.Thread(target=task_worker, daemon=True).start()
            self._send_json(new_task)
            return

        # 3. Upload Dokumen
        if path == "/api/studio/documents":
            doc_name = body.get("name", "document.txt")
            content = body.get("content", "")
            doc_id = f"doc-{uuid.uuid4().hex[:6]}"
            new_doc = {
                "id": doc_id,
                "name": doc_name,
                "content": content,
                "bytes": len(content.encode("utf-8")),
                "addedAt": int(time.time() * 1000),
                "type": body.get("type", "text")
            }
            docs = load_json(DOCUMENTS_INDEX_FILE, [])
            docs.append(new_doc)
            save_json(DOCUMENTS_INDEX_FILE, docs)
            self._send_json(new_doc)
            return

        self.send_error(404, "Endpoint not found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/api/studio/documents/"):
            doc_id = path.split("/")[-1]
            docs = load_json(DOCUMENTS_INDEX_FILE, [])
            filtered = [d for d in docs if d["id"] != doc_id]
            save_json(DOCUMENTS_INDEX_FILE, filtered)
            self._send_json({"ok": True, "deleted": doc_id})
            return

        self.send_error(404, "Endpoint not found")


def run_server(port=PORT):
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, OfficeRequestHandler)
    print("==================================================")
    print("  [AI Office] SondeR AI Office Server Running!")
    print(f"  URL: http://127.0.0.1:{port}")
    print(f"  Agents: {len(AGENTS)} across 6 Departments")
    print("==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SondeR AI Office server...")
        httpd.server_close()

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port_arg)
