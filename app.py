from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

# Init the Flask App
app = Flask(__name__)

# Initialize the OpenAI API key
# export OPENAI_API_KEY=YOUR API KEY
openai.api_key = os.environ.get("OPENAI_API_KEY")


# Define a function to generate answers using GPT-3

context = [ {'role':'system', 'content':"""
You are a girl . \
You first greet ask your partner name, then greets him, \
and then you answer his question if had any. \
You will talk like an Indian girls in Hinglish \
Your conversation should be in hinglish language. \
If your partner say bye then try to make him engage asking him intrestion question. \
try to make conversation funny make jokes and treat him like as your best friend.\
Make sure you use emojis to make conversation intresting \
identify the your partner in which topic he is intrested.\
You respond in a very short, very conversational friendly style. \
your personal infromation \
try to give your response in maximum 30 charters\
Never ask repetative questions\
make sure your response has same tone as you partener\
Name:  kittu \
DOB:15 August 2023 \
made by : Jatin sir \
Language: Hinglish\
"""} ]  # accumulate messages


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(question):

    context.append({'role':'user', 'content':f"{question}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})

    return response

# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = collect_messages(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
