import requests
import psutil
import json 
import eel

from engine.memory import add_memory, get_memory
from engine.language import detect_language
from engine.router import is_meaning_request, is_translation_request
from engine.hybrid_translate import hybrid_translate

# 🔥 ONLY THIS FOR SPEAK (translation case)
from engine.speech import speak
# from engine.command import speak

# 🔥 STREAMING ENGINE
from engine.streaming import stream_llm

OLLAMA_URL = "http://localhost:11434/api/generate"

_selected_model = None


# ---------------- MODEL SELECT ----------------
def choose_model():
    global _selected_model

    if _selected_model:
        return _selected_model

    mem = psutil.virtual_memory().available / (1024**3)

    if mem >= 6:
        _selected_model = "llama3:8b"
    elif mem >= 3:
        _selected_model = "mistral"
    else:
        _selected_model = "phi3:mini"

    return _selected_model


# ---------------- CLEAN RESPONSE ----------------
def clean_response(text):
    bad_words = [
        "Translated to English:",
        "###",
        "---",
        "Instruction",
        "Jarvis:",
        "SHRI:"
    ]

    for w in bad_words:
        text = text.replace(w, "")

    return text.strip()


# ---------------- EMOTION DETECTOR ----------------
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["great", "awesome", "yes", "done", "success"]):
        return "happy"

    elif any(word in text for word in ["error", "fail", "problem", "sorry"]):
        return "sad"

    elif any(word in text for word in ["wow", "amazing", "cool"]):
        return "excited"

    return "normal"


# ---------------- WARMUP ----------------
def warmup():
    try:
        model = choose_model()

        requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": "hello",
                "stream": False
            },
            timeout=5
        )
    except:
        pass


# ---------------- MAIN CHAT ----------------
def llmChat(query):
    print("🔥 LLM STARTED:", query)

    try:
        eel.ShowHood() 
        eel.receiverText("Thinking...")  
    except:
        pass

    model = choose_model()
    context = get_memory()
    user_lang = detect_language(query)

    # -------- Meaning --------
    if is_meaning_request(query):

        payload = {
            "model": model,
            "prompt": f"Explain in one simple sentence: {query}",
            "stream": True
        }

        # 🔥 STREAMING (SPEAK handled inside stream_llm)
        answer = clean_response(stream_llm(OLLAMA_URL, payload))

        add_memory("User", query)
        add_memory("JARVIS", answer)
        return

    # -------- Translation --------
    if is_translation_request(query):

        translated = hybrid_translate(query, "hi", model)
        translated = clean_response(translated)
        return {
            "text": translated,
            "emotion": detect_emotion(translated)
        }

        # # ✅ Only here speak manually
        # speak(translated, detect_emotion(translated))

        # add_memory("User", query)
        # add_memory("JARVIS", translated)
        # return

    # -------- Normal Chat --------
    prompt = (
        "You are Jarvis, a smart AI assistant.\n"
        "- Speak short and clear.\n"
        "- Give only direct answers.\n"
        "- Do NOT give instructions.\n"
        "- Do NOT explain rules.\n"
        "- Keep answer under 2 lines.\n\n"
        f"User: {query}\n"
        "Jarvis:"
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    # 🔥 STREAMING (auto speak inside streaming.py)
    answer = clean_response(stream_llm(OLLAMA_URL, payload))

    add_memory("User", query)
    add_memory("JARVIS", answer)