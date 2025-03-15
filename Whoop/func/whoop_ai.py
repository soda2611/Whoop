import requests

GEMINI_API_KEY = "AIzaSyDcpFwp8JuuYoUkYvmmz0yyw2wbPCjqdzc"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def whoop_ai(user_input, conversation_history):
    conversation_history.append({"role": "user" ,"parts": [{"text": user_input}]})
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