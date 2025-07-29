import google.generativeai as genai
from ..config.settings import settings

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def generate_response(self, chat_history: list[dict]):
        # Gemini API expects a specific format for history
        # [{ "role": "user", "parts": [...]}, {"role": "model", "parts": [...]}]
        
        # The 'assistant' role in our DB maps to 'model' for Gemini API
        formatted_history = [
            {"role": "model" if msg["role"] == "assistant" else "user", "parts": [msg["content"]]}
            for msg in chat_history
        ]
        
        # The last message is the new prompt, which we remove from history
        if not formatted_history:
            return "Hello! How can I help you today?"

        prompt = formatted_history.pop()
        if prompt['role'] != 'user':
             # This should not happen in a normal flow, but as a safeguard:
            return "I can only respond to user messages."

        chat = self.model.start_chat(history=formatted_history)
        
        try:
            response = chat.send_message(prompt['parts'])
            return response.text
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return "I'm sorry, I encountered an error and can't respond right now."


gemini_service = GeminiService(api_key=settings.GEMINI_API_KEY)