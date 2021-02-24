import geocoder as gc
import gtts
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.util import pr
from numpy.lib import type_check
stemmer = LancasterStemmer()
import random
import webbrowser as wb
import numpy
import tflearn
import json
import keyboard
from datetime import datetime
import pickle
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import requests
from os import path
from calculator.simple import SimpleCalculator
cal = SimpleCalculator()
import os.path
bad_responce = ['I could not understand the question','I dont know how to respond', "I do not know the answer to that"]
first_run = True
with open('intents.json') as file:
    data = json.load(file)

try:
   
    with open('data.pickle', 'rb') as f:
        words, lables, training, output = pickle.load(f)
    first_run = False
except:
    
    words = []
    lables = []
    docs_x = []
    docs_y = []
    training = []
    output = []


    for intent in data['intents']:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent['tag'] not in lables:
            lables.append(intent['tag'])
    print(lables)
    words = [stemmer.stem(w.lower()) for w in words if w not in '?']
    
    words = sorted(list(set(words)))
    
    lables = sorted(lables)
    out_empty = [0 for _ in range(len(lables))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds =[stemmer.stem(w) for w in doc]
        #for p in wrds :
            #p = str(p)
    
            #if len(p) > 4:
                #x = random.randrange(0,len(p))

                #wrds = res_str = p[:x-1] +  p[x+1:] 
       

        for w in words:
            if w in wrds:
                i = 1
                #u = len(w)
                #print(u)
            #if w in wrds:
                #i = 1
                #i = i + 1
            else:
                i = 0
                #u = 0
            bag.append(i)
            #bag.append(u)
           
            
                
        output_row = out_empty[:]
        output_row[lables.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row) 

    training = numpy.array(training)
    output = numpy.array(output)
    
    with open('data.pickle', 'wb') as f:
        pickle.dump((words, lables, training, output), f) 
    



net = tflearn.input_data(shape=[None, len(training[0])])
#net = tflearn.fully_connected(net, 512)
#net = tflearn.fully_connected(net, 448)
#net = tflearn.fully_connected(net, 384)
#net = tflearn.fully_connected(net, 320)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)

net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net)
try:
    model.load('model.tflearn.TFL')
except:
    model.fit(training, output, n_epoch=10000, batch_size=1024 ,show_metric=True)
    model.save('model.tflearn.TFL')
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True





def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]    

    for se in s_words:
        for i,w in enumerate(words):
            u = 0
            if w == se:
                
                bag[i] = 1
                #bag[i+1] = len(w)
            #for w in se:
                #u = u + 1
                #bag[i] = u
            
            
    return numpy.array(bag)

def chat(inp):
    if inp == None:
        
        x = 'could not under stand the questoin'
    else:
        bow = bag_of_words(inp, words)
        if 1 in bow:

            results = model.predict([bag_of_words(inp, words)])
            #print(results)
            results_index = numpy.argmax(results)
            tag = lables[results_index]
        
            
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            x = random.choice(responses)
        else:
            x = random.choice(bad_responce)
        if x == 'show_weather':
            g = gc.ip('me')
            
            lat = g.lat
            lon = g.lng
            url = 'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat) + '&lon='+ str(lon) + '&appid=22592c15c610c3a1c10c7e1f104615a5&units=imperial&mode=json'
            
            response = requests.get(url)
            weather_json = json.loads(response.text)
            
            main_weather = weather_json["main"]
            temp = str(main_weather["temp"])
            low = str(main_weather["temp_min"])
            high = str(main_weather["temp_max"])
            city = str(weather_json["name"])
            x = ('in '+ str(city) + " it is " + str(temp) + ' degrees, with a low of ' + str(low), " degrees ,and a high of " + str(high) + " degrees")
            
           
        if x == 'time':
            now = datetime.now()
            x = now.strftime("%H:%M")
        if x == "math":
            try:
                cal.run(inp)
                x = str(cal.lcd)
            except:
                x = 'math is still a beta function and we could not understand the question'
        if x == 'take_note':
            tts = gTTS('what do you want your note to be')
            tts.save('responce.mp3')
            playsound('responce.mp3')
            os.remove('responce.mp3')
            with sr.Microphone() as source:
        
                audio = r.listen(source)

            try:
                note_num = 1
                note = r.recognize_google(audio)
                while True:
                    if path.exists("notes/note" + str(note_num) + ".txt") == True:
                        note_num = note_num + 1
                    else:
                        break
                f = open('notes/note'+ str(note_num) + '.txt' , 'x')
                f.write(note)
                f.close
                f = 'notes/note' + str(note_num) + 'txt'
                print('note saved at:', os.path.abspath(f))
                x = 'note saved'              
            except:
                x = 'an error occurred'
            
    tts = gTTS(str(x))
    print(x)
    tts.save('responce.mp3')
    playsound('responce.mp3')
    os.remove('responce.mp3')
    #print(random.choice(responses))
if first_run == True:
    tts = gTTS('Hello welcome to Sapphire 1.2 We have added many new commands. first off we have added typing just say type followed by what you want to type. secondly we have added the ability to look things up on google and youtube say look up to look something up and say look up blank on youtube to look something up on youtube. lastly we have added the ability to open programs just say open followed by the program name to pen the program')
else:
    tts = gTTS('Welcome Back')
tts.save('responce.mp3')
playsound('responce.mp3')
os.remove('responce.mp3')
print('start')      
while True:
    if keyboard.is_pressed(('ctrl','f1')):
       
        run = True
        inp = ''
        r = sr.Recognizer() 
        
        with sr.Microphone() as source:
            
            audio = r.listen(source)

        try:

            inp = r.recognize_google(audio)
            print(inp)
            if r.recognize_google(audio) == 'quit':
                break
            if str(inp)[0:5] == 'type ' or str(inp)[0:5] == 'Type ' :
                
                inp = str(inp)[5:]
                
                keyboard.write(inp)
                run = False
            if str(inp)[0:5] == 'open ' or str(inp)[0:5] == 'Open ':
                inp = inp[5:]
                try:
                    try:
                        os.startfile('C:/ProgramData/Microsoft/Windows/Start Menu/Programs/'+ str(inp)+ '.lnk')
                    except:
                        homedir = os.path.expanduser("~")
                        os.startfile(str(homedir) + '/desktop/' +  str(inp)+ '.lnk')
                except:
                    tts = gTTS('Sapphire could not luanch the desiered program')
                    tts.save('responce.mp3')
                    playsound('responce.mp3')
                    os.remove('responce.mp3')

                run = False
            if 'look up' in str(inp)[:7]:
                
                inp = str(inp)
            
                
                if 'on YouTube' in str(inp): 
                    
                    list = str(inp).split(' ')
                    list.remove('look')
                    list.remove('up')
                    list.remove('on')
                    list.remove('YouTube')
                    inp = ' '.join(list)
                
                    wb.open("https://www.youtube.com/results?search_query="+ str(inp))
                    run = False
                else:
                    
                    list = str(inp).split(' ')
                    list.remove('look')
                    list.remove('up')
                    inp = ' '.join(list)
                    
                    wb.open("https://www.google.com/search?q="+ str(inp))
                    run = False
            if 'nevermind' in str(inp):
                tts = gTTS('Ok')
                tts.save('responce.mp3')
                playsound('responce.mp3')
                os.remove('responce.mp3')

            if run == True:
                chat(inp)
        except:
            pass
    
    
    
