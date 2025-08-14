import whisper
import sounddevice as sd
import numpy as np
import subprocess
from datetime import datetime
import pyttsx3

# Load Whisper model
model = whisper.load_model("small")

# Supported languages
supported_langs = {'en': 'English', 'hi': 'Hindi', 'kn': 'Kannada'}

def process_audio(audio_data, lang_choice="en"):
    result = model.transcribe(audio_data, language=lang_choice)
    return result["text"].strip()

# Text-to-speech
def speak(text):
    print("🗣️", text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Record audio
def record_audio(duration=6, samplerate=16000):
    print("🎤 Speak now...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)

# Language selection
def get_language_choice():
    print("Select language / भाषा / ಭಾಷೆ:")
    for code, name in supported_langs.items():
        print(f"{code}: {name}")
    while True:
        choice = input("Enter language code: ").strip().lower()
        if choice in supported_langs:
            return choice
        print("Invalid. Try again.")

# Open applications
def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe"
    }
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak("App not found.")

# Date & time
def tell_time():
    speak("The time is " + datetime.now().strftime("%I:%M %p"))

def tell_date():
    speak("Today's date is " + datetime.now().strftime("%B %d, %Y"))

# Greetings based on time
def greet_user(lang):
    hour = datetime.now().hour
    if lang == 'en':
        if hour < 12:
            speak("Good morning! How can I help you?")
        elif 12 <= hour < 18:
            speak("Good afternoon! How can I help you?")
        else:
            speak("Good evening! How can I help you?")

    elif lang == 'hi':
        if hour < 12:
            speak("सुप्रभात! मैं आपकी क्या मदद कर सकती हूँ?")
        elif 12 <= hour < 18:
            speak("नमस्कार! मैं आपकी क्या मदद कर सकती हूँ?")
        else:
            speak("शुभ संध्या! मैं आपकी क्या मदद कर सकती हूँ?")

    elif lang == 'kn':
        if hour < 12:
            speak("ಶುಭೋದಯ! ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?")
        elif 12 <= hour < 18:
            speak("ನಮಸ್ಕಾರ! ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?")
        else:
            speak("ಶುಭ ಸಂಜೆ! ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?")

# Command handling
def handle_command(text, lang):
    text = text.lower()

    # English
    if lang == 'en':
        if "time" in text:
            tell_time()
        elif "date" in text:
            tell_date()
        elif "open notepad" in text:
            open_app("notepad")
        elif "open calculator" in text:
            open_app("calculator")
        elif "hello" in text or "hi" in text:
            greet_user(lang)
        elif "bye" in text or "exit" in text:
            speak("Goodbye!")
            return False
        else:
            speak("I didn't understand that.")
    
    # Hindi
    elif lang == 'hi':
        if "समय" in text:
            tell_time()
        elif "तारीख" in text:
            tell_date()
        elif "नोटपैड" in text:
            open_app("notepad")
        elif "कैलकुलेटर" in text:
            open_app("calculator")
        elif "नमस्ते" in text or "हैलो" in text:
            greet_user(lang)
        elif "अलविदा" in text:
            speak("अलविदा!")
            return False
        else:
            speak("माफ कीजिये, मैं समझ नहीं पाई।")
    
    # Kannada
    elif lang == 'kn':
        if "ಸಮಯ" in text:
            tell_time()
        elif "ದಿನಾಂಕ" in text:
            tell_date()
        elif "ನೋಟ್ಪ್ಯಾಡ್" in text:
            open_app("notepad")
        elif "ಕ್ಯಾಲ್ಕ್ಯುಲೇಟರ್" in text:
            open_app("calculator")
        elif "ನಮಸ್ಕಾರ" in text or "ಹಲೋ" in text:
            greet_user(lang)
        elif "ವಿದಾಯ" in text:
            speak("ವಿದಾಯ!")
            return False
        else:
            speak("ಕ್ಷಮಿಸಿ, ನನಗೆ ಅದು ಅರ್ಥವಾಗಲಿಲ್ಲ.")
    
    return True

# Main program
def main():
    lang_choice = get_language_choice()
    greet_user(lang_choice)  # Greet at start

    while True:
        audio = record_audio()
        result = model.transcribe(audio, language=lang_choice)
        user_text = result["text"].strip()
        print("You said:", user_text)

        if not handle_command(user_text, lang_choice):
            break

if __name__ == "__main__":
    main()
