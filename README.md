# Travel Helper Chatbot
This chatbot gives recommendations about restaurants, events, bars, news, and
activities about Bolivia.

<!--
import os, sys
import pprint
from flask import Flask, request
from Travel_Chat import *
from pymongo import MongoClient
import creds as CR
from pymessenger import Bot
import re

# TIPICAL GREETINGS:
GREETINGS = set(["hello","hi","holaa","hola","hey","holas","heyy","hii","hiii"])


# Initialize database:
def point_collection():
    client = MongoClient(CR.mongo_host,CR.mongo_port)
    db = client[CR.mongo_db]
    collection = db.messages
    return collection

def clean_message(message):
    message = message.lower()
    message = re.sub(r'[^\w]', '', message)
    return message

# Find an answer:

def answer_to_message(bot,sender_id,last_message_received,last_message_sent):
    # Cleaning message:
    last_message_received = clean_message(last_message_received)
    last_message_sent = clean_message(last_message_sent)

    # Different messages:
    saludo = "hi! are you traveling in Bolivia?"
    buttons = [
          {
            "type":"web_url",
            "url":"http://www.paginasiete.bo/",
            "title":"Bolivian News"
            },
          {
            "type": "postback",
            "title": "otro",
            "payload": "otro"
            }]

    if last_message_received in GREETINGS:
        bot.send_text_message(sender_id,saludo)
    elif "yes" in last_message_received: #and last_message_sent == saludo:
        bot.send_button_message(sender_id,"great, I can offer you:",buttons)



# Messages database:
messages_table = point_collection()
# Bots:
listener_bot = Conversational_Bot()
responder_bot = Bot(CR.PAGE_ACCESS_TOKEN)


# App:
app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    #print(request.args)
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    # Get the message in Json format:

    message = request.get_json()
    #print("message event received: ")
    pprint.pprint(message)
    try:
        # 1. Bot parses the message
        print("parsing message")
        listener_bot.parse_json_message(message)

        # 2. Bot stores the message
        print("storing message:")
        listener_bot.store_message(messages_table)

        # 3.Finding the last_message:
        sender_id = listener_bot.last_sender_id

        # 3.1 Pretending to write:
        #responder_bot.send_action(sender_id, "typing on")

        # 3.2 Finding last messages:
        last_message_received = listener_bot.find_last_message_received(messages_table,sender_id)
        last_message_sent = listener_bot.find_last_message_sent(messages_table,sender_id)
        #answer= get_answer(last_message)
        print("last message received: ",last_message_received)
        print("last message sent: ",last_message_sent)

        # 4. Sending the answer:
        answer_to_message(responder_bot,sender_id,last_message_received,last_message_sent)
        #responder_bot.send_action(sender_id, "typing off")

    except KeyError:
        #pprint.pprint(message)
        pass
    #print()






    #handle_message(listener_bot,message,messages_table)

    return "ok", 200

# # Handle a message:
# def handle_message(bot,message,messages_table):
#     # 1. Bot parses the message
#     listener_bot.parse_json_message(message)
#
#     # 2. Bot stores the message
#     listener_bot.store_message(messages_table)
#
#     # 3.Finding the last_message:
#     sender_id = listener_bot.last_sender_id
#
#     last_message = listener_bot.last_message_text
#
#     #answer= get_answer(last_message)
#     print("last message: ",last_message)
#     # 4. Sending the answer:
#     answer_to_message(responder_bot,sender_id,last_message)
#     print("here")
#     #print()
#
#     #sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80) -->
