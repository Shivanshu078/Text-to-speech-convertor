import os
import subprocess
import speech_recognition as sr
from gtts import gTTS
from gtts.lang import tts_langs
from tkinter import *
from tkinter import messagebox

def text_to_speech():
    """Convert text to speech and play it."""
    text = text_entry.get("1.0", "end-1c").strip()
    language = accent_entry.get().strip()
    
    if not text or not language:
        messagebox.showerror("Error", "Enter both text and language code.")
        return
    
    try: 
        speech = gTTS(text=text, lang=language, slow=False)
        speech.save("text.mp3")
        
        # Play audio file
        if os.name == "nt":  # Windows
            os.system("start text.mp3")
        else:  # Linux/macOS
            os.system("mpg123 text.mp3")
    except ValueError:
        messagebox.showerror("Error", "Invalid language code! Click 'List languages' to check supported ones.")

def list_languages():
    """Show available language codes for gTTS."""
    langs = tts_langs()
    messagebox.showinfo("Supported Languages", "\n".join([f"{k}: {v}" for k, v in langs.items()]))

def speech_to_text():
    """Convert speech to text and display it."""
    recognizer = sr.Recognizer()
    
    try:
        duration = int(duration_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid duration (numeric value).")
        return
    
    messagebox.showinfo("Recording", "Speak into the microphone now...")
    
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            audio_input = recognizer.listen(mic, timeout=duration)
            text_output = recognizer.recognize_google(audio_input)
            messagebox.showinfo("You Said:", text_output)
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the audio. Try again.")
    except sr.RequestError:
        messagebox.showerror("Error", "Speech recognition service is unavailable.")
    except OSError:
        messagebox.showerror("Error", "No microphone detected. Ensure your microphone is connected and working.")

# GUI Setup
window = Tk()
window.geometry("500x300")
window.title("Speech to Text & Text to Speech Converter")
Label(window, text="Convert Speech to Text and Text to Speech", font=("Arial", 12)).pack(pady=5)

# Text input
Label(window, text="Text:").place(x=10, y=40)
text_entry = Text(window, width=40, height=3)
text_entry.place(x=80, y=40)

# Accent input
Label(window, text="Accent (Language Code):").place(x=10, y=120)
accent_entry = Entry(window, width=30)
accent_entry.place(x=150, y=120)

# Duration input
Label(window, text="Duration (secs):").place(x=10, y=150)
duration_entry = Entry(window, width=10)
duration_entry.place(x=150, y=150)

# Buttons
Button(window, text='List languages', bg='Turquoise', fg='Red', command=list_languages).place(x=10, y=190)
Button(window, text='Text to Speech', bg='Turquoise', fg='Red', command=text_to_speech).place(x=130, y=190)
Button(window, text='Speech to Text', bg='Turquoise', fg='Red', command=speech_to_text).place(x=260, y=190)

window.mainloop()
