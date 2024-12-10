import speech_recognition as sr
import pyttsx3
import time
import os

from llm import ask_llm


recognizer = sr.Recognizer()
key = os.getenv("AzureAPI")


def SpeakText(text: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 200)
    engine.say(text)
    engine.runAndWait()


def recocnize_speech_from_mic(recognizer: sr.Recognizer, audio) -> str:
    text = recognizer.recognize_azure(
        audio_data=audio,
        key=key,
        location="northeurope",
        language="en-US",
        profanity="raw",
    )
    return text[0]


def callback(recognizer: sr.Recognizer, audio):
    try:
        text = recocnize_speech_from_mic(recognizer, audio)
        print(f"You said: {text}")

        if "buddy" in text.casefold():
            llmText = ask_llm(text)
            SpeakText(llmText)

    except sr.UnknownValueError:
        print("Azure could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Azure; {e}")


# Create a background listener that listens for speech in the background
stop_listening = recognizer.listen_in_background(sr.Microphone(), callback)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_listening(wait_for_stop=False)
    print("Background listener stopped")
