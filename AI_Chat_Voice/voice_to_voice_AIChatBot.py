import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import os
import requests
import json
import time
import pygame
import datetime
import glob

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

print("API_KEY:", API_KEY)
print("GEMINI_API_URL:", GEMINI_API_URL)

try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing Pygame mixer: {e}")
    print("Please ensure your audio drivers are up-to-date and Pygame is correctly installed.")

current_sound_object = None
current_sound_file = None

def listen_for_audio(timeout_duration=5, phrase_time_limit_duration=10):
    """
    Listens for audio input from the microphone and converts it to text.
    Args:
        timeout_duration (int): How long to wait for a phrase to start.
        phrase_time_limit_duration (int): How long to listen for a phrase once it starts.
    Returns:
        str: The recognized text, or an empty string if nothing was understood or an error occurred.
    """
    global current_sound_object
    if current_sound_object:
        try:
            if pygame.mixer.get_busy():
                current_sound_object.stop()
                time.sleep(0.1)
        except pygame.error as e:
            print(f"Pygame error stopping sound before listening: {e}")
        finally:
            current_sound_object = None 

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source) 
        try:
            audio = r.listen(source, timeout=timeout_duration, phrase_time_limit=phrase_time_limit_duration)
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
            return ""

def get_ai_response(prompt):
    """
    Sends the prompt to the Gemini API and returns the AI's response.
    Includes system instructions to guide the AI's persona and response style.
    """
    if not prompt.strip():
        return "Please ask a question."

    system_instruction = (
        "You are a friendly and helpful AI assistant named Shiva. "
        "Keep your responses short, concise, and conversational, like a human speaking, not use any type of special characters or formatting. "
        "Do not provide long explanations unless explicitly asked. "
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
    """
    Cleans up old audio files that are no longer being played.
    This function iterates through all .mp3 files in the current directory
    and removes those starting with "response_" that are not the currently playing file.
    This helps prevent accumulation of temporary audio files.
    """
    global current_sound_file
    current_dir = os.getcwd()
    for filename in glob.glob(os.path.join(current_dir, "*.mp3")):
        if filename != current_sound_file and os.path.basename(filename).startswith("response_"):
            try:
                os.remove(filename)
            except OSError as e:
                print(f"Warning: Could not clean up old file {filename} (it might still be in use or permissions issue): {e}")

def speak_text(text):
    """
    Converts text to speech using gTTS and plays it using pygame.
    Manages stopping previous sounds, playing the new sound, and cleaning up audio files.
    Includes robust error handling and timing adjustments.
    """
    global current_sound_object, current_sound_file

    if not text.strip():
        print("Nothing to speak.")
        return

    timestamp = datetime.datetime.now().strftime("response_%Y%m%d%H%M%S%f.mp3")
    audio_file_mp3 = timestamp

    if current_sound_object:
        try:
            if pygame.mixer.get_busy():
                current_sound_object.stop()
                time.sleep(0.1)
        except pygame.error as e:
            print(f"Pygame error stopping previous sound: {e}")
        finally:
            current_sound_object = None

    if current_sound_file and os.path.exists(current_sound_file):
        try:
            os.remove(current_sound_file)
        except OSError as e:
            print(f"Warning: Could not remove previous playing file {current_sound_file} (it might still be in use): {e}")
        finally:
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
        time.sleep(audio_duration + 0.5) 

        try:
            if current_sound_object and pygame.mixer.get_busy():
                 current_sound_object.stop()
            time.sleep(0.1)
        except pygame.error as e:
            print(f"Pygame error stopping current sound after playback: {e}")
        finally:
            current_sound_object = None 

        if os.path.exists(audio_file_mp3):
            try:
                os.remove(audio_file_mp3)
            except OSError as e:
                print(f"Warning: Could not remove audio file {audio_file_mp3} after playback: {e}")
            finally:
                current_sound_file = None

    except Exception as e:
        print(f"Error during text-to-speech or audio playback: {e}")
        if current_sound_object:
            try:
                current_sound_object.stop()
            except pygame.error as err:
                print(f"Error stopping sound on playback error: {err}")
            finally:
                current_sound_object = None
        if audio_file_mp3 and os.path.exists(audio_file_mp3):
            try:
                os.remove(audio_file_mp3)
            except OSError as err:
                print(f"Error during cleanup after playback error for {audio_file_mp3}: {err}")
            finally:
                current_sound_file = None

def run_chatbot():
    """Runs the main voice-to-voice chatbot loop with activation and deactivation."""
    print("AI Voice Chatbot Started! Say 'Hello Shiva' to activate.")
    print("Once active, say 'exit', 'quit', 'ruk jaaw', 'stop', or 'stop the chat' to deactivate.")

    chatbot_active = False 
    global current_sound_object, current_sound_file

    while True:
        cleanup_old_audio_files() 

        if not chatbot_active:
            print("\nWaiting for activation phrase 'Hello Shiva'...")
            activation_phrase = listen_for_audio(timeout_duration=3, phrase_time_limit_duration=3).lower().strip()
            
            if "hello shiva" in activation_phrase:
                chatbot_active = True
                print("Chatbot activated!")
                speak_text("Hello there! How can I help you today?")
            else:
                continue
        
        if chatbot_active:
            print("\nChatbot is active. Please speak your question.")
            user_input = listen_for_audio()
            
            deactivation_phrases = ["exit", "quit", "ruk jaaw", "stop", "stop the chat"]
            if user_input.lower().strip() in deactivation_phrases:
                speak_text("Goodbye! It was nice chatting with you.")
                print("Chatbot deactivated.")
                
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
            else:
                speak_text("I didn't catch that. Can you please repeat?")
            print("-" * 30)

if __name__ == "__main__":
    run_chatbot()
