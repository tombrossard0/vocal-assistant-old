import os
import playsound
import datetime
import speech_recognition as sr
from gtts import gTTS
import subprocess
import webbrowser
from pynput.keyboard import Key, Controller
import time
import wikipedia
from translate import Translator
import locale
import sympy


locale.setlocale(locale.LC_TIME,'')


keyboard = Controller()


HOW_ARE_YOU = ["comment ca va"]
HELLO = ["salut", "hey"]
TAKE_NOTE = ["crée une note"]
OPEN_NOTE = ["ouvre une note"]
OPEN_GOOGLE = ["ouvre google", "lance google"]
OPEN_YOUTUBE = ["ouvre youtube", "lance youtube"]
OPEN_ROCKET_LEAGUE = ["ouvre rocket league", "lance rocket league"]
OPEN_MINECRAFT = ["ouvre minecraft", "lance minecraft"]
WRITE_SENTENCE = ["écris"]
YOUTUBE_FULLSCREEN = ["mets youtube en plein écran"]
WIKIPEDIA_SEARCH = ["recherche sur wikipédia", "recherches sur wikipédia"]
GOOGLE_SEARCH = ["recherche sur google", "recherches sur google"]
GOOGLE_TRANSLATE = ["traduit", "traduire", "traduis"]
TIME = ["heure"]
DAY = ["jour"]
CALCUL = ["calcul"]


def Speak(text, langue = "fr"):
    tts = gTTS(text=text, lang=langue)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("le fichier n'existe pas")


def Get_Audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language = "fr-FR")
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
    return said.lower()


def Note(text, myFilename):
    date = datetime.datetime.now()
    file_name = str(myFilename) + ".txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def Detect_ActionToDO(audio):
    for phrase in HOW_ARE_YOU:
        if phrase in audio:
            Speak("Bien et toi?")

    for phrase in HELLO:
        if phrase in audio:
            Speak("Bonjour!")

    for phrase in TAKE_NOTE:
        if phrase in audio:
            Speak("Donnez moi un nom pour le fichier")
            filename = Get_Audio()

            Speak("Je vous écoutes")
            text = Get_Audio()

            Note(text, filename)

    for phrase in OPEN_NOTE:
        if phrase in audio:
            Speak("Donnez moi un nom pour le fichier")
            filename = Get_Audio()

            Speak("voilà!")            
            subprocess.Popen(["notepad.exe", str(filename) + ".txt"])

    for phrase in OPEN_GOOGLE:
        if phrase in audio:
            Speak("voilà !")
            webbrowser.open("www.google.com")

    for phrase in OPEN_YOUTUBE:
        if phrase in audio:
            Speak("voilà !")
            webbrowser.open("https://www.youtube.com/?gl=FR&hl=fr")

    for phrase in OPEN_ROCKET_LEAGUE:
        if phrase in audio:
            Speak("voilà !")
            os.startfile('C:/Users/Tom/Desktop/Rocket League.url')

    for phrase in OPEN_MINECRAFT:
        if phrase in audio:
            Speak("voilà !")
            os.startfile('C:/Users/Public/Desktop/Minecraft.lnk')

    for phrase in WRITE_SENTENCE:
        if phrase in audio:
            Speak("Je vous écoutes")
            text = Get_Audio()
            
            Speak("voilà !") 
            keyboard.type(text)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

    for phrase in YOUTUBE_FULLSCREEN:
        if phrase in audio:
            Speak("voilà !")
            keyboard.press('f')
            keyboard.release('f')

    for phrase in WIKIPEDIA_SEARCH:
        if phrase in audio:
            Speak("Que voulez vous rechercher?")
            recherche = Get_Audio()
            wikipedia.set_lang("fr")
            text = str(wikipedia.summary(recherche, sentences = 1))
            Speak(text)

    for phrase in GOOGLE_SEARCH:
        if phrase in audio:
            Speak("Que voulez vous rechercher?")
            recherche = Get_Audio()
            webbrowser.open("www.google.com/search?q=" + str(recherche))

    for phrase in DAY:
        if phrase in audio:
            day = str("Nous sommes le " + time.strftime("%A %d %B %Y"))
            print(day)
            Speak(day)

    for phrase in TIME:
        if phrase in audio:
            heure = str("Il est " + time.strftime("%H:%M"))
            print(heure)
            Speak(heure)

    for phrase in CALCUL:
        if phrase in audio:
            Speak("Quel calcul voulez-vous faire ?")
            calculToDo = Get_Audio()
            calculToDo = calculToDo.replace("x", "*")
            calculToDo = calculToDo.replace("divisé par", "/")
            calcul = sympy.sympify(str(calculToDo))
            calculToDo = calculToDo.replace("*", "fois")
            calculToDo = calculToDo.replace("/", "divisé par")
            print(str(calcul))
            Speak(calculToDo + " égale " + str(calcul))

    for phrase in GOOGLE_TRANSLATE:
        if phrase in audio:
            phraseB = str(audio)
            output = ""
            index = 0

            listeMots = phraseB.split(" ")

            for i in range(len(listeMots)):
                if (listeMots[i]) == "en":
                    index = i

            output = listeMots[index+1:]

            try:
                langue = output[0]
            except:
                Speak("Désolé je n'ai pas compris, essayez la structure langue puis mot, ou phrase à traduire")
                print("Désolé je n'ai pas compris, essayez la structure langue puis mot, ou phrase à traduire")
                break
            
            toTranslateL = output[1:]
            toTranslate = ""
            langue2 = ""

            for i in range(len(toTranslateL)):
                toTranslate += " " + toTranslateL[i]

            if (toTranslate == "" or toTranslate == " "):
                Speak("Désolé je n'ai pas compris, essayez la structure langue puis mot, ou phrase à traduire")
                print("Désolé je n'ai pas compris, essayez la structure langue puis mot, ou phrase à traduire")
                break

            if (langue == "anglais"):
                langue2 = "en"
            if (langue == "allemand"):
                langue2 = "de"

            Speak("Je vous traduis ca tout de suite")
            trad = Translator(from_lang="fr", to_lang=langue2)
            Speak("En " + langue + "," + toTranslate + " ce traduit par")
            Speak(trad.translate(toTranslate[1:]), langue2)
            print(trad.translate(toTranslate[1:]))

