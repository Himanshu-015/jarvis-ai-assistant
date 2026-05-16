import requests
import json
import time
from engine.speech import speak #  speech_queue
# from engine.command import speak
import eel

STOP_FLAG = False


def stop_speaking():
    global STOP_FLAG
    STOP_FLAG = True

    # 🔥 CLEAR SPEECH QUEUE (VERY IMPORTANT)
    # while not speech_queue.empty():
    #     try:
    #         speech_queue.get_nowait()
    #     except:
    #         pass


def stream_llm(url, payload):

    global STOP_FLAG
    STOP_FLAG = False

    try:
        eel.resetJarvisMsg()
    except:
        pass

    try:
        r = requests.post(url, json=payload, stream=True)
    except Exception as e:
        print("Connection error:", e)
        return ""

    buffer = ""
    full_answer = ""
    max_chars = 300 

    for line in r.iter_lines():

        if STOP_FLAG:
            print("⛔ Stopped")
            break

        if line:
            try:
                data = json.loads(line.decode("utf-8"))

                # 🔥 CHUNK PARSER (SAFE)
                chunk = ""

                if "response" in data:
                    chunk = data["response"]
                elif "message" in data:
                    chunk = data["message"].get("content", "")
                elif "content" in data:
                    chunk = data["content"]

                if chunk:
                    print("📦 CHUNK:", chunk)

                    buffer += chunk
                    full_answer += chunk

                    # ✅ UI LIVE UPDATE
                    try:
                        eel.receiverText(full_answer)
                    except:
                        pass

                    clean = buffer.strip()

                    # 🔥 ONLY SPEAK WHEN SENTENCE COMPLETE
                    if (
                        clean.endswith(".") or
                        clean.endswith("!") or
                        clean.endswith("?")
                    ):
                        print("🔊 SPEAK:", clean)
                        speak(clean, "normal")
                        buffer = ""
                        time.sleep(0.05)
                        
                    # 1️⃣ Length limit
                    if len(full_answer) > max_chars:
                        print("⛔ STOP: Max length reached")
                        break

                    # 2️⃣ First sentence complete
                    if "." in full_answer:
                        print("⛔ STOP: Sentence complete")
                        break

                    # 3️⃣ Garbage filter
                    if (
                        "expanded" in full_answer.lower()
                        or "instruction" in full_answer.lower()
                        or "example" in full_answer.lower()
                    ):
                        print("⛔ STOP: Garbage detected")
                        break


            except Exception as e:
                print("Stream error:", e)

    # 🔊 LAST LEFT TEXT
    if buffer.strip() and not STOP_FLAG:
        print("🔊 FINAL:", buffer.strip())
        speak(buffer.strip(), "normal")

    # ✅ UI RESET (VERY IMPORTANT)
    try:
        eel.ShowHood()
    except:
        pass

    return full_answer.strip()