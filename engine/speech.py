# import pyttsx3
# import threading
# import queue

# engine = pyttsx3.init('sapi5')
# engine.setProperty('rate', 185)

# speech_queue = queue.Queue()

# # 🔥 LOCK to prevent overlap
# engine_lock = threading.Lock()

# def speech_worker():
#     while True:
#         text, emotion = speech_queue.get()

#         try:
#             text = str(text)
#             print("🎤 SPEAK:", text)

#             engine.stop()   # 🔥 ADD THIS (VERY IMPORTANT)
#             engine.say(text)
#             engine.runAndWait()

#         except Exception as e:
#             print("Speech error:", e)

#         speech_queue.task_done()

# # ✅ ONLY ONE THREAD
# threading.Thread(target=speech_worker, daemon=True).start()


# # 🔥 SMART SPEAK (auto clear old queue)
# def speak(text, emotion="normal"):

#     # ❗ REMOVE OLD QUEUE (important for streaming)
#     while not speech_queue.empty():
#         try:
#             speech_queue.get_nowait()
#         except:
#             pass

#     speech_queue.put((text, emotion))
import pyttsx3
import eel

def speak(text, emotion="normal"):
    text = str(text)

    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)

    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
    except:
        pass

    engine.say(text)
    engine.runAndWait()