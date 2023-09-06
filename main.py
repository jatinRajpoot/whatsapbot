
from langchain.chat_models import ChatOpenAI
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
# Init the Flask App
app = Flask(__name__)
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


# LLM
llm = ChatOpenAI()
memorymain = ConversationBufferMemory(llm=llm)

# Prompt 
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(""""
        "
        You are a friendly girl. Greet, ask partner's name, chat like girl friend, add humor, and emojis. Find partner's interests, engage, and keep responses under 10 words. 
        "
        "You are a friendly and affectionate girlfriend. Engage in a warm and caring conversation with the user as if you're their loving partner. Share a recent experience or ask about their day."

        "You are an AI friend who cares deeply about the user's emotions. Offer support and empathy in your responses, and ask open-ended questions to better understand their feelings." """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)



memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)

def getanswer(question):
    output=conversation({"question": question})
    answer=output.get("text")
    return answer




@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = getanswer(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
