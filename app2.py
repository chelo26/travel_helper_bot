import os, sys
import pprint
from flask import Flask, request
from Travel_Chat import *
from pymongo import MongoClient
import creds as CR
from pymessenger import Bot
import re
from datetime import datetime

# TIPICAL GREETINGS:
GREETINGS = set(["salut!","salut","hello","hi","holaa","hola","hey","holas","heyy","hii","hiii"])


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

def generate_post(sender_id,message):
    post = {"sender_id": sender_id,
            #"recipient_id": self.last_recipient_id,
            "message": message,
            "timestamp": datetime.utcnow()}
    return post

def get_message_type(message_event):
    entry = message_event["entry"][0]
    messaging = entry.get("messaging")
    ## ADD POSTBACK type, so we can reply to it!!!!
    print("messaging ", messaging)
    if messaging:
        message = messaging[0].get("message")
        if message:
            print("message" , message)
            if len(message) == 3:
                text = message["text"]
                return text,True
            else:
                return None,False
        elif messaging[0].get("postback"):
            message = messaging[0].get("postback")
            payload = message["payload"]
            return payload,True
        else:
            return None,False
    else:
        return None,False

def parse_message_sent(message_event):
    entry = message_event["entry"][0]
    messaging = entry.get("messaging")
    print("messaging ", messaging)
    if messaging:
        message = messaging[0].get("message")
        if message:
            print("message" , message)
            if len(message) == 3:
                text = message["text"]
                return text,True
            else:
                return None,False
        else:
            return None,False
    else:
        return None,False


# Find an answer:

def answer_to_message(responder_bot,sender_id,last_message_received,last_message_sent):
    # Cleaning message:
    if last_message_sent:
        last_message_sent = clean_message(last_message_sent)
    if last_message_received:
        last_message_received = clean_message(last_message_received)

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
        responder_bot.send_text_message(sender_id,saludo)
        return saludo
    elif "yes" in last_message_received: #and last_message_sent == saludo:
        options_offering = "great, I can offer you:"
        responder_bot.send_button_message(sender_id,options_offering,buttons)
        return options_offering




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
    text,send_back_bool = get_message_type(message)
    if send_back_bool == True:

        pprint.pprint(message)
        # 1. Bot parses the message
        listener_bot.parse_json_message(message)
        # 2. Bot stores the message
        post = listener_bot.generate_post()
        listener_bot.store_message(messages_table,post)
        # 3.Finding the sender_id:
        sender_id = listener_bot.last_sender_id
        # 3.2 Finding last messages:
        last_message_received = listener_bot.find_last_message_received(messages_table,sender_id)
        last_message_sent = listener_bot.find_last_message_sent(messages_table,sender_id)
        # 4. Sending the answer:
        text, send_back_bool = get_message_type(message)
        print("text: ",text)
        print("send_back ? : ",send_back_bool)
        #if send_back_bool == True:
        print("text : ", text)
        thing_sent = answer_to_message(responder_bot,sender_id,last_message_received,last_message_sent)
        post = generate_post(sender_id,thing_sent)
        listener_bot.store_message(messages_table,post)
        #responder_bot.send_text_message(2120553661303424,text)

    else:
        pass

    return "ok", 200


if __name__ == "__main__":
	app.run(debug = True, port = 80)
