import pyaudio
import wave
import numpy as np
import sounddevice as sd
from flask import Flask,url_for,render_template
import speech_recognition as sr 
import pyttsx3  


app = Flask(__name__) 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
frames = []
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
@app.route('/')
def sound_rec():
    return render_template('audio.html')

@app.route('/sound')
def sound():
    print("Recording Started Now")
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # read data-chunks in strings
        data = stream.read(CHUNK)
        #frames.append(data)
        # change the format to numpy int16
        frames.append(np.fromstring(data,dtype=np.int16))
    #newS = np.fromstring(frames,dtype=np.int16)
    stream.stop_stream()
    stream.close()
    p.terminate()
    #print("* done recording")
    return render_template('audio.html')

@app.route('/play_audio')
def play_audio():
    sound = np.array(frames)
    sound = sound.flatten()
    sd.play(sound,44100*2)
    return render_template('audio.html')
@app.route('/speech')
def speech():
    return render_template('audio.html')

@app.route('/speech_recog')
def speech_recog():
    r=sr.Recognizer()
    global text
    text=''
    print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        # r.energy_threshold()

        audio= r.listen(source)
        try:
            text = r.recognize_google(audio)
            #return render_template('speech.html',text=text)
        except:
            print("sorry, could not recognise")
    return render_template('audio.html')
@app.route('/view_text')
def view_text():
    return render_template('audio.html',text=text)
    
        
    
if __name__ == '__main__':
    app.run()
