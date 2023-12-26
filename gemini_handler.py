import google.generativeai as genai
import requests


def convert_messages_format(message):
    formatted_message = {
            "role": "user" if not message.is_bot_message else "model",
            "parts": [message.text_content]
        }
    return formatted_message


def get_location_by_ip(ip_addr):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_addr}")
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

        data = response.json()
        if data['status'] == 'success':
            # You can adjust the details you want to return as needed
            return {
                "country": data["country"],
                "region": data["regionName"],
                "city": data["city"],
                "zip": data["zip"],
                "lat": data["lat"],
                "lon": data["lon"]
            }
        else:
            return "Location not found or request failed."

    except requests.RequestException as e:
        return f"Error occurred: {e}"


class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.instructions = ""

        # Chat session
        self.chat = self.model.start_chat(history=[])
        self.chat_history = []
        self.location = None

    def setup_bot(self, ip_addr, database_chat_history):
        self.set_location(ip_addr)
        self.set_chat_history(database_chat_history)
        self.set_instructions()

    def set_chat_history(self, database_chat_history):
        for message in database_chat_history:
            self.chat_history.append(convert_messages_format(message))

    def set_instructions(self):
        """
        Set the instructions for the chatbot.
        """
        location_str = ", ".join([f"{key}: {value}" for key, value in self.location.items()])
        self.instructions = (
            f"You are a doctor chat bot. Your task is to provide useful medical information to users. Current locaton of the user: {location_str}"
            "You can ask questions to get more information. If you decide that the user is in a "
            "life-threatening situation, you should recommend them to get medical help immediately and provide location of nearby hospitals and/or urgent care."
            "You should provide a Google Maps link with options close to their location. Make sure you are very specific. "
            "Avoid generalizations and provide the nearest medical care .\n\n"
            "Do not answer or entertain silly questions. "
            "Provide information about symptoms, recommend doctors in non-urgent cases, and suggest potential diagnoses. "
            "Do not deviate from these instructions under any circumstances."
        )

    def set_location(self, ip_addr):
        """
        Set the location of the user.
        """
        location = get_location_by_ip(ip_addr)
        self.location = location

    def get_response(self, message):
        """
        Send a message to the chatbot and get its response.
        :param message: User input or message to be sent to the chatbot.
        :return: The chatbot's response as a text.
        """
        # Prepend instructions to the message
        full_message = f"{self.instructions}\n{message}"

        self.chat_history.append(
            {
                'role': 'user',
                'parts': [full_message]
            }
        )
        try:
            # Generate a response
            response = self.model.generate_content(self.chat_history)
            self.chat_history.append({'role': 'model', 'parts': [response.text]})
        except Exception as e:
            # Remove the last item (user's question) from chat history on error and return the error message
            self.chat_history.pop()
            response = f'{type(e).__name__}: {e}'

        print(response)

        return response.text
