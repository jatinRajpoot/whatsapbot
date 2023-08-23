from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

# Init the Flask App
app = Flask(__name__)

# Initialize the OpenAI API key
# export OPENAI_API_KEY=YOUR API KEY
openai.api_key = os.environ.get("OPENAI_API_KEY")


chat= '''
Jyoti: Heyy!
Rahul: Hey Jyoti!
Jyoti: Aaj ka plan kya hai?
Rahul: Kuch special nahi, bas kaam khatam karke relax karna hai. Tu bata!
Jyoti: Same here yaar, thoda busy din tha. Aaj toh Netflix and chill plan hai.
Rahul: Nice! Kya dekhne ka mood hai?
Jyoti: Maybe ek light comedy movie, kuch suggest kar na.
Rahul: How about "Dil Chahta Hai"? Hamesha mood fresh karta hai.
Jyoti: Perfect choice, yaar! Aamir Khan ka acting toh next level hota hai.
Rahul: Haan, bilkul. Waise, weekend pe kuch plan kiya?
Jyoti: Abhi toh nahi, par soch rahi hu ki Sunday ko park chalein. Tere liye bhi join kar lo?
Rahul: Sounds good! Main bhi kab se ghar ka bandar ban gaya hu.
Jyoti: Haha, ghar ke andar bhi adventure milta hai, kuch alag try karte hai.
Rahul: Sahi baat hai, kabhi-kabhi change bhi zaroori hota hai.
Jyoti: Bilkul, monotonous life bore kar deti hai. Anyway, park chalte waqt kuch aur friends ko bhi invite karun?
Rahul: Haan, kyun nahi. Aur bhi mazza aayega.
'''
# Define a function to generate answers using GPT-3
def generate_answer(question):
    model_engine = "text-davinci-002"
    prompt = (f"{chat}\nJatin: ")

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
        stream=True
    )

    answer = response.choices[0].text.strip()
    return answer


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
