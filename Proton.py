import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from threading import Thread
import subprocess
import app

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")

    reply("I am Proton, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your internet connection.')
        except sr.UnknownValueError:
            print('Cannot recognize voice input')
            pass
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.replace('proton', '')
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found.')
        except:
            reply('Please check your Internet connection.')

    elif 'location' in voice_data:
        reply('Which place are you looking for?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found.')
        except:
            reply('Please check your Internet connection.')

    elif 'bye' in voice_data:
        reply("Goodbye! Have a nice day.")
        is_awake = False

    elif 'exit' in voice_data or 'terminate' in voice_data:
        app.ChatBot.close()
        sys.exit()

    # DYNAMIC CONTROLS
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')

    elif 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')

    elif 'move' in voice_data:
        direction = voice_data.split('move')[1].strip()
        if 'right' in direction:
            pyautogui.moveRel(200, 0)
            reply("Mouse moved right")
        elif 'left' in direction:
            pyautogui.moveRel(-200, 0)
            reply("Mouse moved left")
        elif 'up' in direction:
            pyautogui.moveRel(0, -200)
            reply("Mouse moved up")
        elif 'down' in direction:
            pyautogui.moveRel(0, 200)
            reply("Mouse moved down")

    elif 'click' in voice_data:
        direction = voice_data.split('click')[1].strip()
        if 'right' in direction:
            pyautogui.click(button='right')
            reply("Right click performed")
        elif 'left' in direction:
            pyautogui.click(button='left')
            reply("Left click performed")
        elif 'double' in direction:
            pyautogui.doubleClick()
            reply("Double click performed")

    elif 'scroll' in voice_data:
        if 'up' in voice_data:
        
            pyautogui.scroll(100)
            reply("Scrolled up")
        elif 'down' in voice_data:
            pyautogui.scroll(-100)
            reply("Scrolled down")

    elif 'press' in voice_data:
        key_action = voice_data.split('press')[1].strip()

        # Arrow keys
        if 'up arrow' in key_action:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            reply('Up arrow pressed')
        elif 'down arrow' in key_action:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            reply('Down arrow pressed')
        elif 'left arrow' in key_action:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            reply('Left arrow pressed')
        elif 'right arrow' in key_action:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            reply('Right arrow pressed')

        # Backspace
        elif 'backspace' in key_action:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            reply('Backspace pressed')

        # Space
        elif 'space' in key_action:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            reply('Space key pressed')

        # Enter
        elif 'enter' in key_action:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            reply('Enter key pressed')
        else:
            reply(f'Key action "{key_action}" is not supported')

    elif 'open file' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('o')
            keyboard.release('o')
        reply("Opened file menu in VS Code. Please speak the file name to open.")

        # Wait for voice input for the file name
        file_name = record_audio()

        # Type the file name
        keyboard.type(file_name)
        reply(f"Searching and opening file: {file_name}")

    elif 'open folder' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('k')
            keyboard.release('k')
        time.sleep(0.1)
        with keyboard.pressed(Key.ctrl):
            keyboard.press('o')
            keyboard.release('o')
        reply("Opened folder menu in VS Code. Please speak the folder name to open.")

        # Wait for voice input for the folder name
        folder_name = record_audio()

        # Type the folder name
        keyboard.type(folder_name)
        reply(f"Searching and opening folder: {folder_name}")

    elif 'find text' in voice_data:
        # Triggering Ctrl + F to open the search dialog in VS Code
        with keyboard.pressed(Key.ctrl):
            keyboard.press('f')
            keyboard.release('f')
        reply("Opened find dialog in VS Code. Please speak the text to search for.")
        
        # Wait for voice input for the search query
        search_query = record_audio()
        
        # Once search query is received, type it into the find field
        with keyboard.pressed(Key.ctrl):
            keyboard.press('f')
            keyboard.release('f')
        time.sleep(1)  # Allow time for the input to be registered
        keyboard.type(search_query)
        
        reply(f"Searching for '{search_query}' in VS Code interface")



    elif 'open current folder' in voice_data:
        current_folder = os.getcwd()
        if os.path.isdir(current_folder):
            subprocess.Popen(f'explorer "{current_folder}"')
            reply(f"Opened the current folder: {current_folder}")
        else:
            reply("The current folder does not exist.")

    elif 'open new window' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press(Key.shift)
            keyboard.press('n')
            keyboard.release('n')
            keyboard.release(Key.shift)
        reply("Opened a new window in VS Code.")

    elif 'close folder' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('k')
            keyboard.release('k')
        time.sleep(0.1)
        keyboard.press('f')
        keyboard.release('f')
        reply("Closed the current folder in VS Code.")

    elif 'close window' in voice_data:
        with keyboard.pressed(Key.alt):
            keyboard.press(Key.f4)
            keyboard.release(Key.f4)
        reply("Closed the current window.")

    elif 'close vs code' in voice_data:
        os.system("taskkill /f /im Code.exe")
        reply("VS Code closed")

    elif 'enter text' in voice_data:
        reply("Activating voice typing.")
        with keyboard.pressed(Key.cmd):
            keyboard.press('h')
            keyboard.release('h')
        reply("Voice typing enabled. Please start speaking.")

    else:
        reply('I am not programmed to do this!')

# ------------------Driver Code--------------------
t1 = Thread(target=app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()

    if 'proton' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful")
            break
        except Exception as e:
            print(f"EXCEPTION raised: {e}")
            break
