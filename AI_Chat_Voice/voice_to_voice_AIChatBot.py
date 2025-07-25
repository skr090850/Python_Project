import speech_recognition as sr
from gtts import gTTS
import os
import requests
import json
import time
import pygame
import datetime
import glob

# Configuration
API_KEY = "AIzaSyCCG_pgKySvWHPhralDRwSOL08lzp44pE0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Initialize Pygame Mixer
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing Pygame mixer: {e}")
    print("Please ensure your audio drivers are up-to-date and Pygame is correctly installed.")

# Global variables to track the currently playing Sound object and its file
current_sound_object = None
current_sound_file = None

def listen_for_audio():
    """Listens for audio input from the microphone and converts it to text."""
    global current_sound_object
    if current_sound_object:
        if current_sound_object.get_num_channels() > 0 and current_sound_object.get_channels()[0].get_busy():
            current_sound_object.stop()
            time.sleep(0.1)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak your question.")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing audio...")
            text = r.recognize_google(audio, language='en-US')
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

def get_ai_response(prompt):
    """Sends the prompt to the Gemini API and returns the AI's response."""
    if not prompt.strip():
        return "Please ask a question."

    # Instructions for short, conversational, human-like responses
    system_instruction = (
        "You are a friendly and helpful AI assistant. "
        "Keep your responses short, concise, and conversational, like a human speaking, not use any type of special characters or formatting. "
        "Do not provide long explanations unless explicitly asked. "
        "If the user says a general greeting like 'hello' or 'hi' then you can respond with a greeting and ask 'How are you?' and if anyone not responded then you ask 'How can I help you today?'"
        "If the user asks a question, if you feel like it is a question that requires a long answer, you can say 'I can provide a detailed answer, but I will keep it short and to the point.' "
    )

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": system_instruction + "\nUser: " + prompt}]
            }
        ]
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Unexpected API response structure:", result)
            return "I'm sorry, I couldn't get a clear response from the AI."
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the Gemini API: {e}")
        return "I'm sorry, I'm having trouble connecting to the AI right now."
    except json.JSONDecodeError:
        print("Error decoding JSON response from API.")
        return "I'm sorry, there was an issue processing the AI's response."

def cleanup_old_audio_files():
    """Cleans up old audio files that are no longer being played."""
    global current_sound_file
    current_dir = os.getcwd()
    for filename in glob.glob(os.path.join(current_dir, "*.mp3")):
        if filename != current_sound_file and os.path.basename(filename).startswith("response_"):
            try:
                os.remove(filename)
            except OSError as e:
                print(f"Warning: Could not clean up old file {filename} (it might still be in use): {e}")

def speak_text(text):
    """Converts text to speech and plays it using pygame."""
    global current_sound_object, current_sound_file

    if not text.strip():
        print("Nothing to speak.")
        return

    timestamp = datetime.datetime.now().strftime("response_%Y%m%d%H%M%S%f.mp3")
    audio_file_mp3 = timestamp

    if current_sound_object:
        if current_sound_object.get_num_channels() > 0 and current_sound_object.get_channels()[0].get_busy():
            current_sound_object.stop()
            time.sleep(0.1)
        
        if current_sound_file and os.path.exists(current_sound_file):
            try:
                os.remove(current_sound_file)
            except OSError as e:
                print(f"Warning: Could not remove previous playing file {current_sound_file} (it might still be in use): {e}")
        
        current_sound_object = None
        current_sound_file = None

    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_file_mp3)

        print(f"Speaking: {text}")
        sound = pygame.mixer.Sound(audio_file_mp3)
        sound.play()
        
        current_sound_object = sound
        current_sound_file = audio_file_mp3

        audio_duration = sound.get_length()
        time.sleep(audio_duration + 0.2)

        sound.stop()
        time.sleep(0.1)
        if os.path.exists(audio_file_mp3):
            try:
                os.remove(audio_file_mp3)
            except OSError as e:
                print(f"Warning: Could not remove audio file {audio_file_mp3} after playback: {e}")
        
        current_sound_object = None
        current_sound_file = None

    except Exception as e:
        print(f"Error during text-to-speech or audio playback: {e}")
        if current_sound_object:
            current_sound_object.stop()
            time.sleep(0.1)
        if audio_file_mp3 and os.path.exists(audio_file_mp3):
            try:
                os.remove(audio_file_mp3)
            except OSError as err:
                print(f"Error during cleanup after playback error for {audio_file_mp3}: {err}")
        current_sound_object = None
        current_sound_file = None

def run_chatbot():
    """Runs the main voice-to-voice chatbot loop."""
    print("AI Voice Chatbot Started! Say 'exit' or 'quit' to end the conversation.")
    # Initial greeting for a new conversation
    speak_text("Hello there! How can I help you today? How are you?")

    global current_sound_object, current_sound_file

    while True:
        cleanup_old_audio_files()

        user_input = listen_for_audio()
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            speak_text("Goodbye! It was nice chatting with you.")
            print("Chatbot ended.")
            
            # Final cleanup on exit
            if current_sound_object:
                current_sound_object.stop()
                time.sleep(0.1)
            if current_sound_file and os.path.exists(current_sound_file):
                try:
                    os.remove(current_sound_file)
                except OSError as e:
                    print(f"Error during final cleanup of {current_sound_file}: {e}")
            
            cleanup_old_audio_files()
            pygame.mixer.quit()
            break
        elif user_input:
            ai_response = get_ai_response(user_input)
            speak_text(ai_response)
        print("-" * 30)

if __name__ == "__main__":
    run_chatbot()
