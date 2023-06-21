import speech_recognition as sr
from os import path
from pydub import AudioSegment
import glob

class audio2s:
    def __init__(self,make):
        for path in glob.glob("audio/*.mp3"):
            inp=path
            print(inp)
        sound = AudioSegment.from_mp3(path)
        sound.export("audio/transcript.wav", format="wav")

        AUDIO_FILE = "transcript.wav"

        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file                  

            print("Transcription: " + r.recognize_google(audio))


        '''sound = AudioSegment.from_mp3(inp)
        sound.export(output_file, format="wav")
        with file_audio as source:
            audio_text = r.record(source)

        print(type(audio_text)) 
        print(r.recognize_google(audio_text))
        print(f'Time taken {time.time()-start_time}s') '''