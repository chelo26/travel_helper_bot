# Class that implements the answers to the conversation:
from utils import wit_response
from datetime import datetime
# Creating a message object that can contain image or text :
class Message():
    def __init__(self,message_event):
        self.sender_id = message_event['sender']['id']
        self.recipient_id = message_event['recipient']['id']
        self.image_url = None
        self.text = None
        self.timestamp = message_event['timestamp']
        self.parse_message(message_event)
        self.type = None

    def parse_message(self,message_event):
        message = message_event['message']
        if message.get("text"):
            self.text = str(message['text'])
        elif message.get("attachments"):
            for element in message["attachments"]:
                self.image_url = str(element["payload"]["url"])
                self.type = str(element["type"])

# The Bot recieves a message stored as json and it answers accordingly
class Conversational_Bot():
    def __init__(self):
        self.conversation_level = 0
        self.entity = None
        self.value = None
        self.last_message_text = None
        self.last_sender_id = None
        self.last_recipient_id = None
        self.last_message = None
        self.last_message_time = None
    # Parsing the json received
    def parse_json_message(self,data):
        if  data.get('object') == 'page':
            entry = data.get("entry")[0]
            messaging = entry.get("messaging")
            if messaging:
                messaging = messaging[0]
                if messaging.get("message"):
                    # creating the message object:
                    current_message = self.last_message = Message(messaging)
                    #self.last_message = Message(messaging_event)
                    # IDs
                    #sender_id = self.last_sender_id = current_message.sender_id
                    self.last_sender_id = current_message.sender_id
                    #recipient_id = self.last_recipient_id= current_message.recipient_id
                    self.last_recipient_id = current_message.recipient_id

                    # Message:
                    self.last_message_text = current_message.text
                    # Timestamp:
                    self.last_message_time = current_message.timestamp


    def generate_post(self):
        post = {"sender_id": self.last_sender_id,
                "recipient_id": self.last_recipient_id,
                "message": self.last_message_text,
                "timestamp": datetime.utcnow()}
        return post
    def store_message(self,db,post):
        #message_to_post = self.generate_post()
        db.insert(post)

    def find_last_message_received(self,db,sender_id):
        message_entry = db.find({"sender_id":sender_id}).sort("timestamp",-1).limit(1)
        print("last message received: ")
        #print(message_entry)
        parsed_message = next(message_entry)
        #print(parsed_message)
        return parsed_message["message"]

    def find_last_message_sent(self,db,sender_id):
        message_entry = db.find({"sender_id":{"$ne" : sender_id}}).sort("timestamp",-1).limit(1)
        print("last message sent: ")
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
