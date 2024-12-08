import speech_recognition as sr
import pyttsx3
import time
import os

from llm import ask_llm


recognizer = sr.Recognizer()
key = os.getenv("AzureAPI")


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 200)
    engine.say(command)
    engine.runAndWait()


def recognize_speech_from_mic(recognizer: sr.Recognizer, audio):
    return recognizer.recognize_azure(
        audio_data=audio,
        key=key,
        location="northeurope",
        language="en-US",
        profanity="raw",
    )


def callback(recognizer: sr.Recognizer, audio):
    try:
        # Recognize speech using Azure API
        text = recognize_speech_from_mic(recognizer, audio)
        print(f"You said: {text[0]}")

        # Check if the user wants to initiate a conversation
        if "hey buddy" in text[0].casefold():
            # Initiate the chat
            llm_generator = ask_llm(text[0])
            next(llm_generator)  # Start the generator

            # Keep the chat open for continuous conversation
            while True:
                # Listen for the next user input
                with sr.Microphone() as source:
                    print("Listening for your next message...")
                    audio = recognizer.listen(source)

                # Recognize the next user input
                next_text = recognize_speech_from_mic(recognizer, audio)
                print(f"You said: {next_text[0]}")

                # Check for termination command
                if next_text[0].strip().lower() == "exit":
                    SpeakText("Goodbye!")
                    break

                # Send the user message to the assistant and get the response
                llmText = llm_generator.send(next_text[0])
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
    # Stop the background listener when the script is interrupted
    stop_listening(wait_for_stop=False)
    print("Background listener stopped")
