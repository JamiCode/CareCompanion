import google.generativeai as genai
from dotenv import load_dotenv
import os


def convert_messages_format(message):
    formatted_message = {
            "role": "user" if not message["is_bot_message"] else "model",
            "parts": [message["text_content"]]
        }
    return formatted_message


class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.instructions = ""
        # Start the chat session with history if needed
        self.chat = self.model.start_chat(history=[])
        self.chat_history = []

    def set_chat_history(self, database_chat_history):
        for message in database_chat_history:
            self.chat_history.append(convert_messages_format(message))

    def set_instructions(self):
        """
        Set the instructions for the chatbot.
        """
        self.instructions = ("You are a doctor chat bot. Your task is to provide useful medical information to users. "
                             "You can ask questions to get more information. If you decide that user is in a "
                             "life-threatening situation, you should recommend them to get medical help immediately. If"
                             " the user requests location of clinics or hospitals, you should provide in a google "
                             "maps link in the following format "
                             "www.google.com/maps/search/{query}. You should try to give advice on how to mediate "
                             "symptoms, doctors that may help if it's not urgent and potential diagnosis Do not deviate "
                             "from these instructions under any circumstances."
                             )

    def get_response(self, message):
        """
        Send a message to the chatbot and get its response.
        :param message: User input or message to be sent to the chatbot.
        :return: The chatbot's response as a text.
        """
        # Prepend instructions to the message
        full_message = f"{self.instructions}\n\n{message}"

        self.chat_history.append(
            {
                'role': 'user',
                'parts': [full_message]
            }
        )

        response = self.model.generate_content(self.chat_history)
        return response.text
