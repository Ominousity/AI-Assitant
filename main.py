import speech_recognition as sr
import pyttsx3
import time


recognizer = sr.Recognizer()
key = "Azure key"

def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 200)
    engine.say(command)
    engine.runAndWait()


def callback(recognizer, audio):
    try:
        # Recognize speech using Google Web Speech API
        text = sr.Recognizer().recognize_azure(audio_data=audio, key=key, location="northeurope", language="da-DK", profanity="raw")
        print(f"You said: {text}")
        SpeakText(f"You said: {text}")
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")


# Create a background listener that listens for speech in the background
stop_listening = recognizer.listen_in_background(sr.Microphone(), callback)

# Keep the script running to listen for speech
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    # Stop the background listener when the script is interrupted
    stop_listening(wait_for_stop=False)
    print("Background listener stopped")
