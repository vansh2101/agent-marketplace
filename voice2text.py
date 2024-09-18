import pyaudio
import wave
import speech_recognition as sr
FORMAT = pyaudio.paInt16  #
CHANNELS = 1              
RATE = 44100              
CHUNK = 1024             
RECORD_SECONDS = 30        

def record_audio(filename="output.wav"):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio(filename="output.wav"):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            print("Transcription: " + text)
        except sr.UnknownValueError:
            print("fail")
        except sr.RequestError as e:
            print("fail")

if __name__ == "__main__":
    filename = "output.wav"
    record_audio(filename)
    transcribe_audio(filename)
