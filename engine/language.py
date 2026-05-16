from langdetect import detect

def detect_language(text):

    text = text.lower().strip()

    # 🇮🇳 Strong Hindi indicators
    hindi_keywords = [
        "kya", "kaise", "hai", "tum", "mera",
        "naam", "kyun", "matlab", "haan", "nahi"
    ]

    # ✅ Exact word match (better than 'in')
    words = text.split()

    for word in words:
        if word in hindi_keywords:
            return "hi"

    # ✅ Very short text handling
    if len(text) <= 3:
        return "en"

    try:
        lang = detect(text)

        if lang == "hi":
            return "hi"
        else:
            return "en"

    except:
        return "en"