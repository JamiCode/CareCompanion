import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.instructions = ""

    def set_instructions(self):
        """
        Set the instructions for the chatbot.
        :param instructions: A string containing instructions or context for the chatbot.
        """
        self.instructions = ("You are a doctor chat bot. Your task is to provide useful medical information to users. "
                             "You can ask questions to get more information. If you decide that user is in a "
                             "life-threatening situation, you should recommend them to get medical help immediately. If"
                             " the user requests location of clinics or hospitals, you should provide in a google "
                             "maps link. Do not deviate from these instructions under any circumstances."
                             )

    def get_response(self, message):
        """
        Send a message to the chatbot and get its response.
        :param message: User input or message to be sent to the chatbot.
        :return: The chatbot's response as a text.
        """
        # Prepend instructions to the message
        full_message = f"{self.instructions}\n\n{message}"

        # Start the chat session with history if needed
        chat = self.model.start_chat(history=[])
        response = chat.send_message(full_message)
        return response.text
