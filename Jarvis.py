import speech_recognition as sr
import pyttsx3
import wolframalpha
import webbrowser
import os
import datetime
import random
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Inicjalizacja syntezatora mowy
engine = pyttsx3.init()

# Inicjalizacja klienta WolframAlpha
wolfram_app_id = '88LHTQ-R6RPW9RPV3'
client = wolframalpha.Client(wolfram_app_id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Słucham...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="pl-PL")
        print("Ty: " + command + "\n")
    except sr.UnknownValueError:
        speak("Przepraszam, nie zrozumiałem.")
        command = listen()
    return command

def random_chat():
    topics = {
        "Co u Ciebie słychać?": [
            "U mnie wszystko w porządku, a jak u Ciebie?",
            "Cieszę się, że pytasz. A co u Ciebie?"
        ],
        "Jaka jest Twoja ulubiona książka?": [
            "Lubię książki o sztucznej inteligencji. A Ty?",
            "Czytam wiele różnych rzeczy. A Ty?"
        ],
        "Masz jakieś hobby?": [
            "Interesuję się technologią i programowaniem. A Ty?",
            "Moje hobby to pomaganie ludziom. A jakie są Twoje zainteresowania?"
        ],
        "Lubisz muzykę?": [
            "Tak, szczególnie muzykę klasyczną. A Ty?",
            "Muzyka jest dla mnie ważna. A dla Ciebie?"
        ],
        "Jak minął Twój dzień?": [
            "Dzień minął mi na pomaganiu ludziom. A jak Twój?",
            "Dzień był dość intensywny. A jak Ty spędziłeś swój dzień?"
        ],
        "Masz jakieś plany na weekend?": [
            "Nie mam planów, ale mogę pomóc Ci w zaplanowaniu czegoś. A Ty?",
            "Na razie brak planów. A Ty?"
        ]
    }

    question, responses = random.choice(list(topics.items()))
    speak(question)
    user_response = listen()
    follow_up_response = random.choice(responses)
    speak(follow_up_response)

    # Kontynuacja rozmowy
    if "jak" in user_response.lower():
        speak("Cieszę się, że pytasz. Czy jest coś, co chciałbyś omówić?")
        user_response = listen()
        speak("To brzmi interesująco. Opowiedz mi więcej!")
    elif "muzyka" in user_response.lower():
        speak("Jaka jest Twoja ulubiona piosenka?")
        user_response = listen()
        speak(f"{user_response} to świetny wybór!")
    elif "książka" in user_response.lower():
        speak("Kto jest Twoim ulubionym autorem?")
        user_response = listen()
        speak(f"{user_response} napisał wiele wspaniałych książek!")

def respond(command):
    command = command.lower()

    if 'otwórz youtube' in command:
        speak('Otwieram YouTube')
        webbrowser.open("https://www.youtube.com")

    elif 'która jest godzina' in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"Jest {now}")

    elif 'pogadaj ze mną' in command:
        speak('O czym chcesz pogadać?')
        random_chat()

    elif 'wyszukaj' in command:
        search_term = command.replace("wyszukaj", "")
        url = f"https://www.google.com/search?q={search_term}"
        speak(f"Wyszukuję {search_term}")
        webbrowser.open(url)

    elif 'definiuj' in command:
        definition_term = command.replace("definiuj", "")
        res = client.query(definition_term)
        answer = next(res.results).text
        speak(f"Definicja {definition_term} to {answer}")

    elif 'wyłącz się' in command:
        speak("Dobrze, to do poźniej!")
        exit()

    else:
        speak("Przepraszam, nie znam odpowiedzi na to pytanie.")

def create_gui():
    root = tk.Tk()
    root.title("Jarvis - Twoja pomoc głosowa")

    # Wczytaj obraz
    img = Image.open("face.jpg")
    img = img.resize((250, 250), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = Label(root, image=photo)
    label.image = photo  # Zachowaj referencję do obrazu
    label.pack()

    root.mainloop()

def main():
    speak("Witam, Jestem Jarvis, Twoja pomoc głosowa! Jak mogę Ci pomóc?")
    create_gui()
    while True:
        command = listen()
        respond(command)

if __name__ == "__main__":
    main()
