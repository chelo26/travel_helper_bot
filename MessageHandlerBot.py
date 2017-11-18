# Class that implements the answers to the conversation:
# -*- coding: utf-8 -*-
from utils import wit_response
from datetime import datetime
# Creating a message object that can contain image or text :
class MessageHandlerBot():
    def __init__(self):
        self.sender_id = None #message_event['sender']['id']
        self.recipient_id = None #message_event['recipient']['id']
        self.image_url = None
        self.text = None
        self.timestamp = None#message_event['timestamp']
        #self.parse_message(message_event)
        self.type = None

    def parse_json_message(self,message_event):
        entry = message_event["entry"][0]
        messaging = entry.get("messaging")
        #print("messaging ", messaging)
        if messaging:
            messaging = messaging[0]
            message = messaging.get("message")
            self.sender_id = messaging["sender"]["id"]
            self.recipient_id = messaging["recipient"]["id"]
            if message:
                #print("message" , message)
                if len(message) == 3:
                    text = message["text"]
                    self.text = text
                    #self.type = "text"
                    return text,True
                else:
                    return None,False
            elif messaging.get("postback"):
                message = messaging.get("postback")
                payload = message["payload"]
                self.text = payload
                return payload,True
            else:
                return None,False
        else:
            return None,False

    def generate_post(self):
        post = {"sender_id": self.sender_id,
                "recipient_id": self.recipient_id,
                "message": self.text,
                "timestamp": datetime.utcnow()}
        return post

    def store_message(self,db,post):
        #message_to_post = self.generate_post()
        db.insert(post)

    def find_last_message_received(self,db,sender_id):
        message_entry = db.find({"sender_id":sender_id}).sort("timestamp",-1).limit(1)
        #print("last message received: ")
        #print(message_entry)
        parsed_message = next(message_entry)
        #print(parsed_message)
        return parsed_message["message"]

    def find_last_message_sent(self,db):
        message_entry = db.find({"recipient_id":{"$exists": False}}).sort("timestamp",-1).limit(1)

        #message_entry = db.find({"sender_id":{"$ne" : sender_id}}).sort("timestamp",-1).limit(1)
        #print("last message sent: ")
        #print(message_entry)
        try:
            parsed_message = next(message_entry)
            #print(parsed_message)
        except StopIteration:
            parsed_message = {"message":None}
            #print(parsed_message)
            pass
        return parsed_message["message"]




    #def echo_talk():
    #    bot.send(self.last_sender_id, self.last_message)
                    # Response:
                    # response = self.last_message
                    # bot.send_text_message(self.sender_id, response)

                    # if messaging_event.get('message'):
                    #     self.parse_message(messaging_event)
                    #
    				# 	# Extracting text message
                    #     if 'text' in messaging_event['message']:
                    #         messaging_text = messaging_event['message']['text']
                    #     else:
                    #         messaging_text = 'no text'
                    #
    				# 	# Echo
    				# 	# response = messaging_text
    				# 	# bot.send_text_message(sender_id, response)
                    #     response = None
                    #
                    #     entity, value = wit_response(messaging_text)
                    #     if entity == "location":
                    #         response = "Intersting, so what city in {} you come from? ".format(str(value))
                    #     if response == None:
                    #         respones = "Sorry I don't understand"

    # def get_entity_value():
    #     self.entity
    # def start_conversation():
