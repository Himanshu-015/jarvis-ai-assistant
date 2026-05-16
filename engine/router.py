import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


# ---------- FAST KEYWORD ROUTERS ----------

def is_meaning_request(text):
    keywords = ["meaning", "matlab", "means", "ka matlab"]
    text = text.lower()
    return any(k in text for k in keywords)


def is_translation_request(text):
    keywords = ["translate", "anuvad", "translation"]
    text = text.lower()
    return any(k in text for k in keywords)


# ---------- QUESTION DETECTOR ----------

def is_question(text):
    question_words = [
        "what", "who", "where", "when", "why", "how",
        "define", "explain", "kaise", "kya", "kyu"
    ]
    text = text.lower()
    return any(q in text for q in question_words)


# ---------- FAST SYSTEM COMMAND DETECTOR ----------

def is_system_command(text):
    system_words = [
        "shutdown", "restart", "sleep", "lock",
        "volume", "brightness",
        "time","cpu", "battery", "charge",
        "screenshot","click", "type",
        "message", "whatsapp", "send",
        "open", "close"
    ]
    text = text.lower()
    return any(word in text for word in system_words)


# ---------- APP CONTROL DETECTOR ----------

def is_app_command(text):
    app_words = [
        "open", "start", "launch", "run",
        "message", "whatsapp"  
    ]
    text = text.lower()
    return any(word in text for word in app_words)


# ---------- WEB SEARCH DETECTOR ----------

def is_web_search(text):
    web_words = [
        "search", "google", "youtube", "find"
    ]
    text = text.lower()
    return any(word in text for word in web_words)


# ---------- SMART INTENT ROUTER ----------

def detect_intent(query, model=None):

    q = query.lower()

    # ⚡ priority routing (fast, no AI call)

    if is_meaning_request(q):
        return "meaning"

    if is_translation_request(q):
        return "translation"

    if is_system_command(q):
        return "system"

    if is_app_command(q):
        return "app"

    if is_web_search(q):
        return "web"

    if is_question(q):
        return "ai"

    # ---------- LLM fallback (only if needed) ----------

    if model:
        prompt = f"""
Reply ONLY one word:

ai
system
app
web

Query: {query}
"""

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=10)
            ans = r.json().get("response", "").lower().strip()

            if ans in ["ai", "system", "app", "web"]:
                return ans

        except:
            pass

    # default fallback
    return "ai"