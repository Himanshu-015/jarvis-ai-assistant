from deep_translator import GoogleTranslator
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def online_translate(text, target):
    try:
        return GoogleTranslator(
            source="auto",
            target=target
        ).translate(text)
    except:
        return None


def offline_translate(text, target, model):

    prompt = f"Translate '{text}' to {target}. Reply only translation."

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False   # ✅ FIXED (no streaming parsing)
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=40)
        return r.json().get("response", "").strip()

    except:
        return text


def hybrid_translate(text, target, model):

    # 🔥 try online first
    result = online_translate(text, target)

    if result:
        return result

    # ⚡ fallback to offline
    return offline_translate(text, target, model)