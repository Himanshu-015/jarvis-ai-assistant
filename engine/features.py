import os
from urllib.parse import quote
import sqlite3
import subprocess
import time
import webbrowser
import eel
import pyautogui
import pywhatkit as kit
import psutil
import datetime
import wikipedia
from playsound import playsound

from engine.speech import speak
from engine.config import ASSISTANT_NAME
from engine.llm import llmChat
from engine.helper import extract_yt_term, remove_words
from engine.streaming import stop_speaking
from engine.keyboard import volumeup, volumedown
import screen_brightness_control as sbc

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()


# ================= UI RESPONSE =================
def jarvis_reply(text):
    try:
        eel.receiverText(text)
    except:
        pass


# ================= SOUND =================
@eel.expose
def playAssistantSound():
    try:
        music_dir = "www\\assets\\audio\\start_sound.mp3"
        playsound(music_dir)
    except:
        print("Sound file not found")


# ================= FRONTEND TEXT COMMAND =================
@eel.expose
def executeCommandFromUI(query):
    if query:
        executeCommand(query)


# ================= BASIC =================

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "")
    app = query.strip()

    try:
        cursor.execute('SELECT path FROM sys_command WHERE name=?', (app,))
        result = cursor.fetchone()

        if result:
            jarvis_reply(f"Opening {app}")
            speak(f"Opening {app}", "happy")
            time.sleep(0.3)
            os.startfile(result[0])

        else:
            jarvis_reply(f"Opening {app} in browser")
            speak("Opening", "normal")
            time.sleep(0.3)
            webbrowser.open(f"https://www.google.com/search?q={app}")

    except:
        jarvis_reply("Error opening app")
        speak("Error opening", "sad")

def PlayYoutube(query):
    term = extract_yt_term(query)
    jarvis_reply(f"Playing {term} on YouTube")
    speak(f"Playing {term}", "happy")
    kit.playonyt(term)


# ================= CONTACT =================

def findContact(query):
    query = remove_words(query, ["call", "message"])
    cursor.execute("SELECT mobile_no FROM contacts WHERE name LIKE ?", ('%' + query + '%',))
    result = cursor.fetchone()

    if result:
        num = result[0]
        if not num.startswith("+91"):
            num = "+91" + num
        return num, query
    return 0, 0

import csv

import csv

def findContactCSV(query):
    query = query.lower().strip()

    with open("contacts.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # 🔥 safe access + full name support
            name = (
                (row.get("First Name", "") + " " + row.get("Last Name", ""))
                .lower()
                .strip()
            )

            num = row.get("Phone 1 - Value", "").strip()

            # 🔥 strong matching (both directions)
            if name and (name in query or query in name):
                if num and not num.startswith("+91"):
                    num = "+91" + num

                print("✅ MATCH FOUND:", name, num)
                return num, name

    print("❌ NO MATCH FOUND")
    return None, None

def whatsApp(num, msg, flag, name):
    import pywhatkit as kit

    try:
        speak(f"Sending message to {name}")
        jarvis_reply(f"Sending message to {name}")

        kit.sendwhatmsg_instantly(num, msg, wait_time=10, tab_close=True)

    except Exception as e:
        print(e)
        speak("Failed to send message")
        

# ================= SMART FEATURES =================

def smartType(query):
    text = query.replace("type", "").strip()
    if text:
        pyautogui.write(text)
        jarvis_reply("Typing done")
        speak("Typing done", "happy")
    else:
        jarvis_reply("What should I type?")
        speak("What should I type?", "normal")


def systemControl(query):
    if "shutdown" in query:
        jarvis_reply("Shutting down system")
        speak("Shutting down system", "excited")
        os.system("shutdown /s /t 5")

    elif "restart" in query:
        jarvis_reply("Restarting system")
        speak("Restarting system", "excited")
        os.system("shutdown /r /t 5")

    elif "lock" in query:
        jarvis_reply("Locking system")
        speak("Locking system", "normal")
        os.system("rundll32.exe user32.dll,LockWorkStation")


def mouseControl(query):
    if "click" in query:
        pyautogui.click()
        jarvis_reply("Clicked")
        speak("Clicked", "happy")

    elif "right" in query:
        pyautogui.rightClick()
        jarvis_reply("Right click done")
        speak("Right click done", "happy")


def takeScreenshot():
    file = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(file)
    jarvis_reply("Screenshot saved")
    speak("Screenshot saved", "happy")


def systemInfo(query):
    if "time" in query:
        current = datetime.datetime.now().strftime("%H:%M")
        jarvis_reply(current)
        speak(current)

    elif "cpu" in query:
        cpu = f"{psutil.cpu_percent()} percent CPU"
        jarvis_reply(cpu)
        speak(cpu)

    elif "battery" in query:
        battery = psutil.sensors_battery()
        if battery:
            msg = f"Battery is {battery.percent} percent"
            jarvis_reply(msg)
            speak(msg)


def wikiSearch(query):
    try:
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, 2)
        jarvis_reply(result)
        speak(result)
    except:
        jarvis_reply("No result found")
        speak("No result found", "sad")


def smartSearch(query):
    webbrowser.open(f"https://google.com/search?q={query}")
    jarvis_reply("Searching on Google")
    speak("Searching", "normal")

# ================= EXTRA CONTROL FEATURES =================

# 🔆 Brightness
def brightness_up():
    sbc.set_brightness("+10")

def brightness_down():
    sbc.set_brightness("-10")


# 🎵 Media Control
def play_pause():
    pyautogui.press("playpause")

def next_track():
    pyautogui.press("nexttrack")

def prev_track():
    pyautogui.press("prevtrack")


# 🪟 App Control
def close_app():
    pyautogui.hotkey("alt", "f4")

def switch_app():
    pyautogui.hotkey("alt", "tab")

def minimize_all():
    pyautogui.hotkey("win", "d")


# 📁 File System
def open_downloads():
    os.startfile("C:\\Users\\om\\Downloads")

def create_folder(name="NewFolder"):
    try:
        os.mkdir(name)
        speak("Folder created")
    except:
        speak("Error creating folder")




# 🗣️ Dictation Mode
def dictation_mode():
    from main import takecommand   # ⚠️ lazy import (important)

    speak("Dictation mode started")

    while True:
        text = takecommand()

        if not text:
            continue

        if "stop typing" in text:
            speak("Dictation stopped")
            break

        pyautogui.write(text + " ")


# ================= MULTI COMMAND SUPPORT =================

def split_commands(query):
    separators = [" and ", " then ", ",", " also "]
    commands = [query]

    for sep in separators:
        temp = []
        for cmd in commands:
            temp.extend(cmd.split(sep))
        commands = temp

    return [c.strip() for c in commands if c.strip()]


# ================= MAIN EXECUTION =================

def execute_single(query):

    if "stop" in query:
        stop_speaking()
        jarvis_reply("Stopped")
        return

    elif "open" in query:
        openCommand(query)

    elif "youtube" in query:
        PlayYoutube(query)

    elif "type" in query:
        smartType(query)

    # 🔆 Brightness
    elif "brightness up" in query:
        brightness_up()
        speak("Brightness increased")

    elif "brightness down" in query:
        brightness_down()
        speak("Brightness decreased")

    # 🎵 Media
    elif "play music" in query or "pause" in query:
        play_pause()

    elif "next song" in query:
        next_track()

    elif "previous song" in query:
        prev_track()

    # 🪟 App control
    elif "close app" in query:
        close_app()

    elif "switch app" in query:
        switch_app()

    elif "minimize" in query:
        minimize_all()

    # 📁 File system
    elif "open downloads" in query:
        open_downloads()

    elif "create folder" in query:
        create_folder()

    # 🗣️ Dictation
    elif "start typing" in query:
        dictation_mode()
     

    elif "volume up" in query:
        volumeup()
        jarvis_reply("Volume increased")
        speak("Volume increased", "happy")

    elif "volume down" in query:
        volumedown()
        jarvis_reply("Volume decreased")
        speak("Volume decreased", "normal")

    elif "mute" in query:
        for _ in range(50):
            volumedown()
        jarvis_reply("Volume muted")
        speak("Volume muted", "normal")

    elif any(word in query for word in ["shutdown", "restart", "lock"]):
        systemControl(query)

    elif any(word in query for word in ["click", "right"]):
        mouseControl(query)

    elif "screenshot" in query:
        takeScreenshot()

    elif any(word in query for word in ["cpu", "time", "battery"]):
        systemInfo(query)

    elif "wikipedia" in query:
        wikiSearch(query)

    elif "search" in query or "google" in query:
        smartSearch(query)

    elif "message" in query or "send" in query:
        num, name = findContactCSV(query)

        if num:
            speak(f"What should I send to {name}?")
        
            from main import takecommand
            msg = takecommand()

            if msg and msg.strip():
                whatsApp(num, msg, None, name)
            else:
                speak("Message not received")
        else:
            speak("Contact not found")


def executeCommand(query):
    from engine.streaming import stop_speaking

    stop_speaking() 

    query = query.lower().replace(ASSISTANT_NAME.lower(), "").strip()

    commands = split_commands(query)

    for cmd in commands:
        print("Executing:", cmd)
        execute_single(cmd)
        time.sleep(0.5)
    try:
        eel.ShowHood()   # wave → off, oval → on
    except:
        pass
