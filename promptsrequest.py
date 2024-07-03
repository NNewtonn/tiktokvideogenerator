import openai
import apis
import random

# API keys
API_KEY_OPENAI = apis.api_key_openai

openai.api_key = API_KEY_OPENAI
good_emotions = ["Happiness", "Joy", "Love", "Gratitude", "Contentment", "Peace", "Excitement", "Hope", "Satisfaction", "Amusement", "Inspiration", "Pride", "Empathy", "Compassion", "Trust", "Optimism", "Relief", "Enthusiasm", "Affection"]
daily_emotion = random.choice(good_emotions)
print("hola")
print(daily_emotion)
#Asking openai
def request_chatgpt():
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Give me a 250 character poem that relates to the feeling of: " + daily_emotion,
        max_tokens=150
    )
    print("Respuesta de ChatGPT:")
    print(response.choices[0].text.strip())

