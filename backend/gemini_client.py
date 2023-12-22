import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_response(self, message):
        chat = self.model.start_chat(history=[])
        response = chat.send_message(message)
        return response.text
