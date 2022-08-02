import pyttsx3
import speech_recognition as sr
import datetime
import os
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import time
import pyjokes
import requests
from bs4 import BeautifulSoup
import pyautogui
import os.path
import subprocess
from pynput import keyboard
import pyautogui
from pynput.keyboard import Controller
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from saaraUi import Ui_saaraUi
keyboard=Controller()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("i am saara... please tell me how may i help you")

def close(app):
    os.system(f'taskkill /f /im {app}')

def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ab7679a0dcfa42b685b5bbaf7b4991a4'
    main_page = requests.get(main_url).json()
    article = main_page["articles"]
    head = []
    day=["first","second","third","fourth","fifth"]
    for ar in article:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.TaskExecution()
    
    def  takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=5,phrase_time_limit=8)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            speak("Say that again please...")
            return "none"
        return query
    
    def TaskExecution(self):

        def typeandsave():
            while True:
                speak('shall i save this file??')
                ty=self.takecommand()
                if ty in ['yes save','yes save this file','ok save','ok','ya save it']:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('s')
                    pyautogui.keyUp('ctrl')
                    speak('tell me the name of the file')
                    ty=self.takecommand()                    
                    for i in ty:
                        keyboard.type(i)
                        time.sleep(0.05)
                    pyautogui.press('enter')
                    break
                elif ty in ['no i can save','i can save','no thanks']:
                    type()
                    break

        def type():            
            speak('tell me what to type')
            while True: 
                ty=self.takecommand()
                if "stop" in ty:
                    speak('typing stopped')
                    break
                elif ty in ['yes enter','senter']:
                    pyautogui.press('enter')
                    continue
                else:            
                    for i in ty:
                        keyboard.type(i)
                        time.sleep(0.05)
                    keyboard.type(" ")
            
        wish()    
        while True:
            self.query = self.takecommand().lower()
        
            if "open camera" in self.query:
                try:
                    subprocess.run('start microsoft.windows.camera:', shell=True)
                except:speak("camera counldn't found")
            
            elif "play music" in self.query:
                music_dir = "C:\\Users\\Public\\Music"
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching ....")
                self.self.query = self.self.query.replace("wikipedia","")
                results = wikipedia.summary(self.self.query, sentences=2)
                speak("according to wikipedia")
                speak(results)

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open instagram" in self.query:
                webbrowser.open("www.instagram.com")

            elif "open google" in self.query:
                speak("opening..")
                time.sleep(3)
                speak("sir, what should i search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")
                speak("here is what i found sir..")

            elif "play song on youtube" in self.query:
                speak("tell me which song to play sir..")
                cm=self.takecommand().lower()
                if cm is not None:
                    kit.playonyt(cm)
                else:
                    speak('say that again please')
                    self.takecommand().lower()
                
            elif 'timer' in self.query or 'stopwatch' in self.query:
                speak("For how many minutes?")
                timing = self.takecommand()
                timing =timing.replace('minutes', '')
                timing = timing.replace('minute', '')
                timing = timing.replace('for', '')
                timing = float(timing)
                timing = timing * 60
                speak(f'I will remind you in {timing} seconds')
                time.sleep(timing)
                speak('Your time has been finished sir')                        

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif self.query in ["tell me today's news","tell me news","what are today's headlines"]:
                speak("please wait sir, fetcheing the latest news")
                news()

            elif "what's the weather" in self.query or 'tell me the temperature' in self.query or "what's the temperature" in self.query:
                    speak("Getting weather details ...please wait sir.")
                    ipadd=requests.get('https://api.ipify.org').text
                    url='https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'
                    geo_requests=requests.get(url)
                    geo_data=geo_requests.json()
                    city=geo_data['city']
                    search=f"temperature in {city}"
                    url=f"https://www.google.com/search?q={search}"
                    r=requests.get(url)
                    data=BeautifulSoup(r.text,"html.parser")
                    temp=data.find("div",class_="BNeawe").text
                    speak(f"current {search} is {temp}")
                    if temp < '20°':
                        speak("It will be better if you wear woolen clothes, sir.")
                    elif temp <= '14°':
                        speak("Sir, it is very cold outside. If you want to go outside, wear woolen clothes.")
                    elif temp >= '25°':
                        speak("Sir, you can wear cotton clothes as it is somewhat hot today..")

            elif "where am i" in self.query or "find my location" in self.query or "where are we" in self.query:
                speak("wait sir.., let me check")
                try:
                    ipadd=requests.get('https://api.ipify.org').text
                    print(ipadd)
                    url='https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'
                    geo_requests=requests.get(url)
                    geo_data=geo_requests.json()
                    city=geo_data['city']
                    
                    country=geo_data['country']
                    speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir, due to network issue i am not able find location")

            elif "are you there" in self.query:
                speak("yess boss... tell me")            
            
            elif "thanks" in self.query or "thank you" in self.query:
                speak("it's my pleasure boss..")
            
            elif "shutdown" in self.query:
                while True:
                    speak("are you sure to shutdown the system")
                    ye=self.takecommand()
                    if "yes" in ye:
                        speak('shutting down the system')
                        os.system('shutdown /s /t 5')
                        break
                    elif "no" in ye:
                        speak("ok as you wish")
                        break
                    else:
                        continue
            
            elif "restart" in self.query:
                while True:
                    speak("are you sure to restart the system")
                    ye=self.takecommand()
                    if "yes" in ye:
                        speak('restarting the system')
                        os.system('shutdown /r /t 5')
                        break
                    elif "no" in ye:
                        speak("ok as you wish")
                        break
                    else:
                        continue
            
            elif "open notepad" in self.query:
                os.startfile('C:\\Windows\\system32\\notepad.exe')
                while True:
                    speak("do you want me to type anything??")
                    ye=self.takecommand()
                    if "yes" in ye:
                        typeandsave()
                        break
                    elif "no" in ye:
                        speak('ok')
                        break
                    else:
                        continue
                        
            elif "close notepad" in self.query:
                close('notepad.exe')
            
            elif "open word" in self.query:
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE')
                speak("opening")
            elif "close word" in self.query:
                close('WINWORD.EXE')
            
            elif "open powerpoint" in self.query:
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')
                speak("opening")
            elif "close powerpoint" in self.query:
                close('POWERPNT.EXE')
            
            elif "excel" in self.query:
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE')
                speak("opening")
            elif "close excel" in self.query:
                close('EXCEL.EXE')
            
            elif "open browser" in self.query:
                os.startfile('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
                time.sleep(1)
                while True: 
                    speak('do you want me to search anything??')
                    ye=self.takecommand()   
                    if "yes" in ye:
                        speak("tell me what to search")
                        ty=self.takecommand()
                        for i in ty:
                            keyboard.type(i)
                            time.sleep(0.05)
                        keyboard.press(" ")
                        pyautogui.press('enter') 
                        break   
                    elif ye in ['no','no thanks','no need']:
                        speak('ok')
                        break
                    else:
                        continue                
                
            elif "close browser" in self.query:
                close('msedge.exe')                
            
            elif "open command prompt" in self.query:
                os.system("start cmd")
                speak("opening")                
            
            elif "close command prompt" in self.query:
                close('cmd.exe')  

            elif "open c drive" in self.query:
                os.startfile("C:\\")
                speak("opening")                    
        
            elif "open d drive" in self.query:
                os.startfile("D:\\")
                speak("opening")                
        
            elif "open e drive" in self.query:
                os.startfile("E:\\")
                speak("opening")                
        
            elif "open f drive" in self.query:
                os.startfile("F:\\")
                speak("opening")                

            elif "open settings" in self.query:
                pyautogui.keyDown('win')
                pyautogui.press('i')
                pyautogui.keyUp('win')  
                speak("opening")    
            
            elif "show start menu" in self.query:
                pyautogui.press('win')
            
            elif "close start menu" in self.query:
                pyautogui.press('win')

            elif "take screenshot" in self.query:
                mysc=pyautogui.screenshot()
                mysc.save(r'D:\\screenshot.png')
                speak("screenshot taken and saved in d drive")                            
            
            elif self.query in ['change window','switch window','next window']:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')
            
            elif "minimise all" in self.query:
                pyautogui.keyDown('win')
                pyautogui.press('m')
                pyautogui.keyUp('win')
            
            elif "restore windows" in self.query:
                pyautogui.keyDown('win')
                pyautogui.keyDown('shiftleft')
                pyautogui.press('m')
                pyautogui.keyUp('shiftleft')
                pyautogui.keyUp('win')
            
            elif self.query in ['maximise','maximize','full screen']:
                pyautogui.keyDown('win')
                pyautogui.press('up')
                pyautogui.keyUp('win')
            
            elif self.query in ['minimise','minimize']:
                pyautogui.keyDown('win')
                pyautogui.press('down')
                pyautogui.keyUp('win')
            
            elif self.query in ['new tab','open new tab']:
                pyautogui.keyDown('ctrl')
                pyautogui.press('T')
                pyautogui.keyUp('ctrl')
            
            elif self.query in ['switch to previous tab','previous tab','move to previous tab']:
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shiftleft')
                pyautogui.press('tab')
                pyautogui.keyUp('shiftleft')
                pyautogui.keyUp('ctrl')

            elif self.query in ['switch to next tab','next tab','move to next tab']:
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')
            
            elif self.query in ['close tab','close this tab']:
                pyautogui.keyDown('ctrl')
                pyautogui.press('W')
                pyautogui.keyUp('ctrl')
            
            elif "create new file" in self.query or "new file" in self.query:
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shiftleft')
                pyautogui.press('n')
                pyautogui.keyUp('shiftleft')
                pyautogui.keyUp('ctrl')

            elif "open file" in self.query:
                pyautogui.keyDown('ctrl')
                pyautogui.press('o')
                pyautogui.keyUp('ctrl')
        
            elif "my files" in self.query:
                pyautogui.keyDown('win')
                pyautogui.press('e')
                pyautogui.keyUp('win')
            
            elif "save" in self.query:                
                pyautogui.keyDown('ctrl')
                pyautogui.press('s')
                pyautogui.keyUp('ctrl')
            
            elif self.query in ["don't save"]:
                pyautogui.press('tab')
                pyautogui.press('enter')
            
            elif self.query in ['cancel']:
                pyautogui.press('tab',presses=2)
                pyautogui.press('enter')

            elif "delete" in self.query:
                pyautogui.press('delete')

            elif self.query in ['new window','open new window']:
                pyautogui.keyDown('ctrl')
                pyautogui.press('n')
                pyautogui.keyUp('ctrl')
            
            elif "rename" in self.query:
                pyautogui.press('f2')
                    
            elif self.query in ['refresh browser']:
                pyautogui.press('browserrefresh')
            
            elif self.query in ['add to favorites']:            
                pyautogui.keyDown('ctrl')
                pyautogui.press('d')
                pyautogui.keyUp('ctrl')
            
            elif "open favorites" in self.query:
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shiftleft')
                pyautogui.press('o')
                pyautogui.keyUp('shiftleft')
                pyautogui.keyUp('ctrl')
        
            elif "escape" in self.query:
                pyautogui.press('esc')
            
            elif self.query in ['volume up','increase volume']:
                pyautogui.press('volumeup')
            
            elif self.query in ['volume down','decrease volume']:
                pyautogui.press('volumedown')
            
            elif self.query in ['mute','mute volume']:
                pyautogui.press('volumemute')   
            
            elif self.query in ['unmute']:
                pyautogui.press('volumemute') 
            
            elif "restore closed tabs" in self.query:
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shiftleft')
                pyautogui.press('t')
                pyautogui.keyUp('shiftleft')
                pyautogui.keyUp('ctrl')
            
            elif "tab" in self.query:
                pyautogui.press('tab')
            
            elif "enter" in self.query:
                pyautogui.press('enter')
            
            elif "up" in self.query:
                pyautogui.press('up')
            
            elif "down" in self.query:
                pyautogui.press('down')
            
            elif "left" in self.query:
                pyautogui.press('left')
            
            elif "right" in self.query:
                pyautogui.press('right')
            
            elif 'backspace' in self.query:
                pyautogui.press('backspace')

            elif 'select all' in self.query:
                pyautogui.keyDown('ctrl')
                pyautogui.press('a')
                pyautogui.keyUp('ctrl')
            elif "close this window" in self.query:
                pyautogui.KeyDown('alt')
                pyautogui.press('f4')
                pyautogui.KeyUp('alt')            

            elif "goodbye" in self.query:
                speak("Ok sir..thanks for using me..")
                os.sys.exit(0)

startExecution=MainThread()
            
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_saaraUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        self.ui.movie=QtGui.QMovie("{Your gif location}\\middle_loading.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie=QtGui.QMovie("{Your gif location}\\top_loading.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()    
    
    def showTime(self):
        current_time=QTime.currentTime()
        current_date=QDate.currentDate()
        label_time=current_time.toString('hh:mm:ss')
        label_date=current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText(label_date)

app=QApplication(sys.argv)
sara=Main()
sara.show()
exit(app.exec_()) 
