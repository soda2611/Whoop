import requests, base64

GEMINI_API_KEY = "AIzaSyDcpFwp8JuuYoUkYvmmz0yyw2wbPCjqdzc"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-exp-03-25:generateContent?key={GEMINI_API_KEY}"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def whoop_ai(user_input, conversation_history, image=None):
    conversation_history.append({"role": "user" ,"parts": [{"text": user_input}]})
    if image:
        image_data = encode_image(image)
        conversation_history[-1]["parts"].append({"inline_data": {"mime_type": "image/jpeg", "data": image_data}})
    data = {"contents": conversation_history}
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        bot_reply = result["candidates"][0]["content"]["parts"][0]["text"]
        conversation_history.append({"role": "model", "parts": [{"text": bot_reply}]})
        return bot_reply, conversation_history
    else:
        return f"Lỗi: {response.status_code} - {response.text}"
