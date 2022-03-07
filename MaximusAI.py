#For Speech and Data recognition
import pyttsx3 # == text data into speach
import speech_recognition as sr
from nltk.tokenize import word_tokenize

#For def
import datetime
import smtplib # MAILS
from pywhatkit import playonyt
import wikipedia
from secret import senderemail, email_pwd
from email.message import EmailMessage # subject sender etc
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia as wiki
from requests import get
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import re # (REGULAR EXPRESSIONS OR REGEX)
import os
from decimal import Decimal
import pyperclip
from googletrans import Translator

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id) # SELECTEAZA VOCEA


    #MaximusAI voice setup

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getvoices(voice):
    voices = engine.getProperty('voices')
    if voice ==1:
        engine.setProperty('voice', voices[1].id)  # SELECTEAZA VOCEA
        speak("Modul Romana activat")
    if voice ==2:
        engine.setProperty('voice', voices[2].id)  # SELECTEAZA VOCEA
        speak("English mode on")



    # Backbone for the commands
def time_funct():
    Time = datetime.datetime.now().strftime('%I:%M:%S') # hour = I minutes = M seconds = S
    speak(f'Ora curentă este {Time}')

def date():
    dateX = datetime.datetime.now()
    speak(f'Data curentă este {dateX.day}/{dateX.month}/{dateX.year}')

def greetings():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour <12:
        speak('Bună dimineața domnule!')
    elif hour >= 12 and hour < 18:
        speak('Bună ziua domnule!')
    elif hour >= 18 and hour < 24:
        speak('Bună seara domnule!')
    else:
        speak('Cam târziu nu credeţi domnule?')

def send_email(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587) # this is the server for the GMAIL
    server.starttls() # transmitere securizata
    server.login(senderemail, email_pwd)
    # server.sendmail(senderemail, to, content)
    email = EmailMessage()
    email['From'] = senderemail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def send_whatsapp(phone_no, message):
    Message = message
    wb.open(f'https://web.whatsapp.com/send?phone={phone_no}&text={Message}')
    sleep(10)
    pyautogui.press('enter')

def translate(word_translate): # Traducere in clipboard Google
    translater = Translator()
    translated_words = translater.translate(word_translate, dest='en')

    pyperclip.copy(translated_words.text)
    speak('Am tradus domnule')

def search_google():
    speak('Ce doriți sa caut pe gugăl?')
    search = takeCommandMIC()
    wb.open(f'https://www.google.com/search?q={search}')

def search_trading_view():
    wb.open(f'https://www.tradingview.com')

def screen_shot():
    dateX = datetime.datetime.now()
    name_img = f'./scrennshots/{dateX.strftime("%d.%m.%Y-""%H-%M")}.png'
    img = pyautogui.screenshot(name_img)
    img.show()

def coin_market_cap():
        cmc = CoinMarketCapAPI('575792ad-0824-4b28-84ad-a0eabc54530c')
        btc = cmc.cryptocurrency_info(symbol='BTC')
        b = btc.data
        speak('Calculez informațiile, durează o secundă')
        pattern = re.compile(r'price of (Bitcoin) is (\d+[,.]\d{3})')

        matches = pattern.finditer(b['BTC']['description'])
        for match in matches:
            speak(f"{match.group(1)} are un preț de {match.group(2)}{' Dolari'}")

    # Backbone for the commands


def start_program(): # Start up functions
    greetings()
    speak('Numele meu este MaximusAI şi sunt aici să vă ajut')
    remember_fileX = open('remember_data.txt', 'r', encoding='utf-8')
    file_size = os.stat('remember_data.txt').st_size
    if file_size == 0:
        speak('Nu aveți nimic programat pentru astăzi')
    else:
        speak(f'Pentru astăzi aveți programate următoarele, {remember_fileX.read()}')



def takeCommandMIC():    # Taking Orders and execute it
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        # r.dynamic_energy_threshold = 3000
        # r.adjust_for_ambient_noise(source, duration=1.5)
        audio = r.listen(source)

    try:
        print('Recognizning...')
        query = r.recognize_google(audio, language='ro')
        print(query)
    except Exception as e:
        print(e)
        # speak('Repetă te rog...')
        query = ''
    return query



if __name__ == '__main__':
    start_program()
    wake_word = 'max'
    while True:
        query = takeCommandMIC().lower() # Taking orders with lower cases
        query = word_tokenize(query)
        if wake_word in query:
            if 'ceasul' in query: ##########################################-----------TIME
                time_funct()
            if 'calculează' in query or 'cât face' in query: ##########################################-----------CALCULATOR
                try:
                    test = query
                    test1, test2 = test.remove('max'), test.remove('calculează')
                    if 'la' in test:
                        test.remove('la')
                    if 3 == len(test):
                        if 'ori' in test[1]:
                            rez = float(test[0]) * float(test[2])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'împărțit' in test[1]:
                            rez = float(test[0]) / float(test[2])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'minus' in test[1]:
                            rez = float(test[0]) - float(test[2])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'plus' in test[1]:
                            rez = float(test[0]) + float(test[2])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                    if 5 == len(test):
                        if 'ori' in test[1] and 'minus' in test[3]:
                            rez = float(test[0]) * float(test[2]) - float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'ori' in test[1] and 'ori' in test[3]:
                            rez = float(test[0]) * float(test[2]) * float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'ori' in test[1] and 'împărțit' in test[3]:
                            rez = float(test[0]) * float(test[2]) / float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'ori' in test[1] and 'plus' in test[3]:
                            rez = float(test[0]) * float(test[2]) + float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)

                        if 'împărțit' in test[1] and 'minus' in test[3]:
                            rez = float(test[0]) / float(test[2]) - float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'împărțit' in test[1] and 'împărțit' in test[3]:
                            rez = float(test[0]) / float(test[2]) / float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'împărțit' in test[1] and 'ori' in test[3]:
                            rez = float(test[0]) / float(test[2]) * float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'împărțit' in test[1] and 'plus' in test[3]:
                            rez = float(test[0]) / float(test[2]) + float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)

                        if 'minus' in test[1] and 'minus' in test[3]:
                            rez = float(test[0]) - float(test[2]) - float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'minus' in test[1] and 'împărțit' in test[3]:
                            rez = float(test[0]) - float(test[2]) / float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'minus' in test[1] and 'ori' in test[3]:
                            rez = float(test[0]) - float(test[2]) * float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'minus' in test[1] and 'plus' in test[3]:
                            rez = float(test[0]) - float(test[2]) + float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        if 'plus' in test[1] and 'minus' in test[3]:
                            rez = float(test[0]) + float(test[2]) - float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'plus' in test[1] and 'împărțit' in test[3]:
                            rez = float(test[0]) + float(test[2]) / float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'plus' in test[1] and 'ori' in test[3]:
                            rez = float(test[0]) + float(test[2]) * float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                        elif 'plus' in test[1] and 'plus' in test[3]:
                            rez = float(test[0]) + float(test[2]) + float(test[4])
                            calc_str = str(round(Decimal(rez), 2))
                            speak(calc_str.replace('.', 'punct'))
                            pyperclip.copy(calc_str)
                except:
                    speak('Repetați vă rog')

            elif 'notează' in query: # ------------------------------- CREATE NOTES
                speak('Ce doriți să notez domnule?')
                data = takeCommandMIC()
                remember_file = open('remember_data.txt','a+',encoding='utf-8')
                remember_file.write('\n'+data)
                remember_file.close()
                speak('Am notat!')
            elif 'amintește' in query or 'amintești' in query or 'programat' in query: #-----------REMEMBER NOTES
                remember_fileX = open('remember_data.txt','r',encoding='utf-8')
                speak(remember_fileX.read())
            elif 'șterge' in query or 'ștergi' in query: #-------------------------DELETE NOTES
                try:
                    strfx = ''.join(query)
                    nr_x = int()
                    if 'zero' in strfx or '0' in query:
                        nr_x = 0
                    if 'unu' in strfx or '1' in query:
                        nr_x = 1
                    if 'doi' in strfx or '2' in query:
                        nr_x = 2
                    if 'trei' in strfx or '3' in query:
                        nr_x = 3
                    if 'patru' in strfx or '4' in query:
                        nr_x = 4
                    if 'cinci' in strfx or '5' in query:
                        nr_x = 5
                    if 'șase' in strfx or '6' in query:
                        nr_x = 6
                    if 'șapte' in strfx or '7' in query:
                        nr_x = 7
                    if 'opt' in strfx or '8' in query:
                        nr_x = 8
                    if 'nouă' in strfx or '9' in query:
                        nr_x = 9
                    if 'zece' in strfx or '10' in query:
                        nr_x = 10
                    with open('remember_data.txt', 'r') as fr:
                        # reading line by line
                        lines = fr.readlines()

                        # pointer for position
                        ptr = 1

                        # opening in writing mode
                        with open('remember_data.txt', 'w') as fw:
                            for line in lines:

                                # remove the selected line
                                if ptr != nr_x:
                                    fw.write(line)
                                ptr += 1

                    speak('Ștergerea a fost efectuată cu success!')
                except:
                    speak('Nu s-a putut efectua ștergerea!')

            elif 'trading' in query: #-----------WEB SITE TRADINGVIEW
                search_trading_view()

            elif 'descărcări' in query: #-----------FOLDER SEARCH
                os.startfile(f'C:\\Users\\{os.getlogin()}\\Downloads') # oslogin iti ia usernameul automat

            elif 'principal' in query:  #-----------FOLDER SEARCH
                os.startfile(f'C:\\Users\\{os.getlogin()}')

            elif 'bitcoin' in query: #-----------CRYPTO PRICE
                coin_market_cap()

            elif 'digi24' in query or 'știre' in query: #-----------NEWS
                wb.open(f'https://www.digi24.ro/')

            elif 'screenshot' in query: #-----------SCREENSHOT
                screen_shot()

            elif 'youtube' in query: #-----------YOUTUBE
                speak('Ce video doriți să vizionați')
                topic = takeCommandMIC()
                playonyt(topic)

            elif 'traduce' in query or 'tradu' in query or 'traducere' in query: #-------------Google Translate
                speak('Ce vreți să traduc?')
                word_translate = takeCommandMIC()
                translate(word_translate)

            elif 'wikipedia' in query: #-----------WIKIPEDIA
                speak('am înțeles domnule, lucrez la asta')
                wiki.set_lang('ro')
                result = wiki.summary(query[2], sentences=3)
                speak(result)

            elif 'google' in query: #-----------GOOGLE
                search_google()

            elif 'whatsapp' in query:#-----------WHATSAPP
                user_name = {
                    'Lorena':'+40740303333',
                    'Alex':'+40751353333',
                }
                try:
                    speak('Desigur domnule, la cine vreți să trimiteți pe Wațap')
                    name = takeCommandMIC()
                    phone_number = user_name[name]
                    speak('Ce doriți să conțină mesajul domnule?')
                    message = takeCommandMIC()
                    send_whatsapp(phone_number, message)
                    speak('Mesajul a fost trimis cu succes!')
                except Exception as e:
                    print(e)
                    speak('Nu pot trimite mesajul')

            elif 'data' in query or 'dată' in query: #---------DATA
                date()

            elif 'email' in query or 'mesaj' in query: #-------EMAIL
                email_list = {
                    'Lorena':'lorena_example@gmail.com',
                    'Daniel':'daniel.mail@gmail.com'
                }
                try:
                    speak('Desigur domnule, la cine vreți să trimiteți')
                    name = takeCommandMIC()
                    receiver = email_list[name]
                    speak('Care este subiectul mesajului')
                    subject = takeCommandMIC()
                    speak('Ce doriți să conțină mesajul domnule?')
                    content = takeCommandMIC()
                    send_email(receiver,subject,content)
                    speak('Mesajul a fost trimis cu succes!')
                except Exception as e:
                    print(e)
                    speak('Nu pot trimite mailul')

            elif 'închide' in query or 'shutdown' in query: #--------SHUTDOWN COMPUTER
                speak('Închidere activată')
                os.system("shutdown /s /t 1")

            elif 'restart' in query: #--------RESTART COMPUTER
                speak('Restart activat')
                os.system("shutdown /r /t 1")

            elif 'pa' in query: #--------QUIT PROGRAM
                speak('Închidere activată')
                quit()
