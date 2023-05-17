import openai

import getpass

from cryptography.fernet import Fernet

import json

import requests

# Constants

API_KEY_FILE = "key.token"

LOG_FILE = "logs.log"

API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Load API key from file or prompt user to enter a new key

try:

    with open(API_KEY_FILE, "rb") as key_file:

        encrypted_key = key_file.read()

        cipher_suite = Fernet(getpass.getpass("Enter encryption password: ").encode())

        api_key = cipher_suite.decrypt(encrypted_key).decode()

except FileNotFoundError:

    api_key = getpass.getpass("Enter your OpenAI API key: ")

    cipher_suite = Fernet(getpass.getpass("Enter encryption password: ").encode())

    encrypted_key = cipher_suite.encrypt(api_key.encode())

    with open(API_KEY_FILE, "wb") as key_file:

        key_file.write(encrypted_key)

# Initialize OpenAI API

openai.api_key = api_key

# Game dictionary

games = {

    "ttc": "Play tic-tac-toe",

}





# Web search function

def web_search(prompt):

    response = requests.get(f"https://api.duckduckgo.com/?q={prompt}&format=json").json()

    results = response["RelatedTopics"]

    return " ".join([result["Text"] for result in results])

# Log conversation

def log_conversation(user_input, gpt_response):

    with open(LOG_FILE, "a") as log:

        log.write(f"User: {user_input}\n")

        log.write(f"ChatGPT: {gpt_response}\n\n")

# Main conversation loop

while True:

    user_input = input("You: ")

    if user_input.startswith("!web"):

        web_query = user_input[5:]

        search_results = web_search(web_query)

        prompt = f"{search_results}\n\nYou: "

    elif user_input.startswith("!play"):

        game = user_input[6:].lower()

        if game in games:

            prompt = f"{games[game]}\n\nYou: "

        else:

            print("Invalid game. Available games:")

            for name, description in games.items():

                print(f"- {name}: {description}")

            continue

    elif user_input == "!ver":

        print("ChapALPHA 0b92, copyright owned by What_Should_I_Be")

        continue

    elif user_input == "!quit":

        print("Quitting...")

        break

    else:

        prompt = f"{user_input}\n\nYou: "

    # Generate response from ChatGPT

    response = openai.Completion.create(

        engine="davinci-codex",

        prompt=prompt,

        max_tokens=50,

        n=1,

        stop=None,

    )

    gpt_response = response.choices[0].text.strip()

    # Print and log response

    print("ChatGPT:", gpt_response)

    log_conversation(user_input, gpt_response)

print("Conversation logged in" + LOG_FILE)

# TODO: !music, short helpful commands like !weather, experiment more with !play
