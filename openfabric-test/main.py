from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText
from typing import Optional
import re
import json
import random_responses

def load_json(file):
    with open(file) as bot_responses:
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:
    output = []
    for question in request.text:
        split_message = re.split(r'\s+|[,;?!.-]\s*', question.lower())
        score_list = []

        # Check all the responses
        for response in response_data:
            bot_response_score = 0
            req_score = 0
            req_words = response["required_words"]

            # Check if there are any required words
            if req_words:
                for word in split_message:
                    if word in req_words:
                        req_score += 1

            # Amount of required words should match the required score
            if req_score == len(req_words):
                # Check each word the user has typed
                for word in split_message:
                    # If the word is in the response, add to the score
                    if word in response["user_input"]:
                        bot_response_score += 1

            # Add score to list
            score_list.append(bot_response_score)

        # Find the best response and return it if they're not all 0
        best_bot_response = max(score_list)
        bot_response_index = score_list.index(best_bot_response)

        # Check if input is empty
        if question == "":
            bot_response = "Please type something so we can chat :("
        # If there is no good response, return a random one.
        elif best_bot_response == 0:
            bot_response = random_responses.random_string()
        else:
            bot_response = response_data[bot_response_index]["bot_response"]    

        output.append(bot_response)

    return SimpleText({"text": output})

while True:
    user_question = input("You: ")
    if user_question == "exit":
        break
    input_text = SimpleText({"text": [user_question]})
    output_text = execute(input_text, None)
    bot_response = output_text.text[0] 
    print("Bot: ", bot_response)
