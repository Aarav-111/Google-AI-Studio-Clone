import ollama
import pyautogui
import io

# Take a screenshot (in memory, no saving)
screenshot = pyautogui.screenshot()

# Convert image to bytes
image_bytes = io.BytesIO()
screenshot.save(image_bytes, format="PNG")
image_bytes.seek(0)

# Send to LLaVA with your prompt
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

# Print the response
print("LLaVA response:")
print(response['message']['content'])
