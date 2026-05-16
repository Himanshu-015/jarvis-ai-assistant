import struct
import speech_recognition as sr

#from engine.speech import speak
from engine.command import speak
from engine.features import executeCommand

# 🔥 TRY IMPORT PORCUPINE
try:
    import pvporcupine
    import pyaudio
    PORCUPINE_AVAILABLE = True
except:
    PORCUPINE_AVAILABLE = False


# ---------------- COMMAND LISTENER ----------------
def listen_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening command...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio).lower()
        print("You:", query)
        return query
    except:
        return ""


# ---------------- FALLBACK WAKE WORD ----------------
def fallback_wake_word():

    r = sr.Recognizer()
    print("🔥 Fallback mode: Say 'jarvis'")

    while True:
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            text = r.recognize_google(audio).lower()
            print("Heard:", text)

            if "jarvis" in text:
                speak("Yes sir, I'm listening", "excited")

                cmd = listen_command()
                if cmd:
                    executeCommand(cmd)

        except:
            pass


# ---------------- MAIN HOTWORD ----------------
def start_hotword():

    if PORCUPINE_AVAILABLE:
        try:
            print("🔥 Trying Porcupine Wake Word...")

            # ❗ agar access_key nahi hai to error aayega
            porcupine = pvporcupine.create(
                keywords=["jarvis"]
                # access_key="YOUR_KEY"  ← agar future me use karna ho
            )

            pa = pyaudio.PyAudio()

            stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            print("🔥 Say 'Jarvis' to activate...")

            while True:
                pcm = stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("🔥 Wake word detected!")
                    speak("Yes sir, I'm listening", "excited")

                    query = listen_command()
                    if query:
                        executeCommand(query)

        except Exception as e:
            print("❌ Porcupine failed:", e)
            print("➡ Switching to fallback mode...")

            fallback_wake_word()

    else:
        print("❌ Porcupine not installed")
        print("➡ Using fallback wake word")

        fallback_wake_word()