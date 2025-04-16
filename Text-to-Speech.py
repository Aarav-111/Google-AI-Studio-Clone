import ollama
import pyautogui
import io
import pyttsx3

# Step 1: Capture screenshot in memory
screenshot = pyautogui.screenshot()
image_bytes = io.BytesIO()
screenshot.save(image_bytes, format="PNG")
image_bytes.seek(0)

# Step 2: Send to LLaVA via Ollama
response = ollama.chat(
    model='llava',
    messages=[
        {
            'role': 'user',
            'content': 'Please give me a short explanation about the following image.',
            'images': [image_bytes.read()]
        }
    ]
)

# Step 3: Print and speak the response
response_text = response['message']['content']
print("LLaVA response:\n", response_text)

# Step 4: Speak it using pyttsx3
engine = pyttsx3.init()
engine.say(response_text)
engine.runAndWait()
