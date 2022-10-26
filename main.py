import os
import playsound
import speech_recognition as sr
from gtts import gTTS
from functions import *
import random


r = sr.Recognizer()

isOk = False

# Wake AI :
WAKE = "ok assistant"

OK = ["Oui?", "Que puis-je pour vous?"]

while True:
    if (isOk):
        print("Listening")
        audio = Get_Audio().lower()

        if audio.count(WAKE) > 0:
            Speak(OK[random.randrange(0, len(OK))])
            audio = Get_Audio().lower()

            Detect_ActionToDO(audio)
    else:
        test = input("Mettez votre nom : ")
        if (test != ""):
            isOk = True
            Speak("Bonjour " + test)
