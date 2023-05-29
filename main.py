import pyaudio
import speech_recognition as sr
import json
import requests
import pyttsx3
import os

def select_microphone():
    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()
    
    # Print available microphones
    print("Available microphones:")
    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
    
    # Select a microphone
    mic_index = int(input("Enter the index of the microphone you want to use: "))
    return mic_index

def press_to_talk(mic_index, ask_func):
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=mic_index)
    
    with mic as source:
        print("Press and hold any key to start recording...")
        input()  # Wait for any key press to start recording
        print("Recording started. Speak your message.")
        audio = r.listen(source)
        print("Recording ended. Recognizing text...")
        
    try:
        text = r.recognize_google(audio)
        ask_func(text)
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def say(message):
    if message == 'exit':
        exit()
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Set the speech rate
    engine.setProperty('rate', 150)

    # Convert text to speech
    engine.say(message)
    print(message)
    engine.runAndWait()

def ask(message):
    print(f'reconized text: {message}')
    data = {
        "prompt": message
    }
    payload = json.dumps(data)

    # Set the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Origin": "https://chatbot.theb.ai",
        "Referer": "https://chatbot.theb.ai/"
    }

    # Send the POST request
    url = "https://chatbot.theb.ai/api/chat-process"
    response = requests.post(url, data=payload, headers=headers)

    # Process the response
    if response.status_code == 200:
        response_text = response.text

        # Find the last JSON string in the response text
        json_strings = response_text.strip().split('\n')
        last_json_string = json_strings[-1]

        response_json = json.loads(last_json_string)
        say(response_json['text'])
    else:
        print("Error:", response.status_code)

def main():
    mic_index = select_microphone()
    os.system('cls')
    while True:
        press_to_talk(mic_index, ask)

if __name__ == "__main__":
    main()
