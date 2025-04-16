import sounddevice as sd
import numpy as np
import pyttsx3
import speech_recognition as sr
import pyautogui
import io
import ollama
import time

def record_voice(duration=5, samplerate=16000):
    print("🎙️ Speak now...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return np.squeeze(audio)

def transcribe_audio(audio, samplerate=16000):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def build_prompt(user_input):
    return f"""
Here's the screenshot of the page I'm on...

"{user_input}"

Please Help me out

Instructions:
- Give Short and Straight-forward responses (limit to 40 words max)
- Use simple to understand language
- Give precise answers and don't go off topic

[Use the Stored memory as needed]
"""

def capture_screen():
    print("📸 Capturing screen in 3 seconds...")
    time.sleep(3)
    screenshot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

def query_llava(prompt, image_bytes):
    response = ollama.chat(
        model='llava',
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [image_bytes]
            }
        ]
    )
    return response['message']['content']

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        audio = record_voice()
        user_text = transcribe_audio(audio).strip().lower()

        if not user_text:
            print("❌ Didn't catch that. Try again.")
            continue

        if user_text in ["quit", "exit", "stop"]:
            print("👋 Exiting as requested.")
            break

        final_prompt = build_prompt(user_text)
        image = capture_screen()
        result = query_llava(final_prompt, image)
        print("🤖 LLaVA says:\n", result)
        speak_text(result)

if __name__ == "__main__":
    main()
