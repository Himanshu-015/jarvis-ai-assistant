import os
import eel
import subprocess
import threading
import time
from engine.features import playAssistantSound, executeCommand
# from engine.speech import speak
from engine.command import *
from engine.llm import warmup
from engine.auth import recoganize
from engine.listener import start_hotword
from engine.streaming import stop_speaking


face_done = False


def start():

    warmup()
    
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        global face_done

        #RUN ONLY ONCE
        if face_done:
            return

        face_done = True
        eel.ShowHood() 

        subprocess.call([r'device.bat'])

        eel.hideLoader()
        speak("Ready for Face Authentication")

        flag = recoganize.AuthenticateFace()

        if flag == 1:

            #IMPORTANT FIX (CLEAR OLD SPEECH)
            stop_speaking()

            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            time.sleep(1)

            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir")
            time.sleep(1)

            eel.hideStart()
            playAssistantSound()

            threading.Thread(target=start_hotword, daemon=True).start()


        else:
            speak("Face Authentication Fail")

    # ✅ USER COMMAND HANDLER
    @eel.expose
    def takeCommand(query):

        # RESET BEFORE EVERY COMMAND
        stop_speaking()

        print("User said:", query)
        executeCommand(query)

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)