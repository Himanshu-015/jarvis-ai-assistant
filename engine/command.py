import pyttsx3
import speech_recognition as sr
import eel
import threading
import os 

from engine.router import detect_intent
from engine.speech import speak
from engine.features import executeCommand



# ✅ VOICE INPUT (FASTER + STABLE)
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")

        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.5

        # 🔥 stability boost
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except:
            return ""

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")

        query = r.recognize_google(audio, language='en-in')
        print("User:", query)

    except:
        return ""

    return query.lower()


# 🔥 NEW: SMART COMMAND HANDLER
def process_query(query):

    try:
        from engine.llm import choose_model , llmChat
        model = choose_model()
    except:
        model = None

    intent = detect_intent(query, model)

    print("Detected Intent:", intent)

    # ⚡ SYSTEM / APP / WEB
    if intent in ["system", "app", "web"]:
        result = executeCommand(query)

        try:
            eel.ShowHood()   # 🔥 AFTER execution
        except:
            pass

        return result

    # 🤖 LLM CASE
    elif intent in ["meaning", "translation", "ai"]:
        print("🔥 CALLING LLM...")
        return llmChat(query)   

    # 🤖 DEFAULT LLM
    else:
        return llmChat(query)


# 🎯 MAIN ENTRY (EEL)
@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)

        if query:
            eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    # 🔥 FIX: NO INPUT HANDLE (MOST IMPORTANT)
    if not query:
        print("❌ No input detected")

        try:
            eel.ShowHood()   # 🔥 wave → off, normal UI
        except:
            pass

        speak("Say something", "normal")  # optional

        return

    try:
        process_query(query)

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong", "sad")
        try:
            eel.ShowHood()
        except:
            pass
