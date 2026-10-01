To use this application (noranisa/bansos: Chat with AI‑powered service bot via WhatsApp & Telegram):
API schema: GET https://noranisa-bansos.hf.space/gradio_api/info
Call endpoint: POST https://noranisa-bansos.hf.space/gradio_api/call/v2/{endpoint} {"param_name": value, ...}
Poll result: GET https://noranisa-bansos.hf.space/gradio_api/call/{endpoint}/{event_id}
File inputs: POST https://noranisa-bansos.hf.space/gradio_api/upload -F "files=@file.ext", use as: {"path": "<returned-path>", "meta": {"_type": "gradio.FileData"}, "orig_name": "file.ext"}
Auth: Bearer $HF_TOKEN (https://huggingface.co/settings/tokens)