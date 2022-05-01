import requests
import random
import json
from .config import *


def callSubscriptionAPI(customFields=None):
    fields = "messages, messaging_postbacks, messaging_optins, message_deliveries, messaging_referrals"

    if customFields:
        fields = fields + " " + customFields

    params = {
        "access_token": PAGE_ACCESS_TOKEN,
        "object": "page",
        "callback_url": WEBHOOK_URL,
        "verify_token": VERIFY_TOKEN,
        "fields": fields,
        "include_values": "true",
    }
    res = requests.get(f"{API_URL}/{APP_ID}/subscriptions ", params=params)

    if res.status_code == 200:
        return "Successfully called Subscription API"
    return "Error on Subscription API \n Error Text:" + res.text


def callSubscribedApps(customFields=None):
    fields = "messages, messaging_postbacks, messaging_optins,message_deliveries, messaging_referrals"
    if customFields:
        fields = fields + " " + customFields

    params = {"access_token": PAGE_ACCESS_TOKEN, "subscribed_fields": fields}
    res = requests.post(f"{API_URL}/{PAGE_ID}/subscribed_apps", params=params)

    if res.status_code == 200:
        return "Successfully call subscribed apps API"
    return "Error while calling subscribed apps API \n Error: " + res.text


def callMessengerProfileAPI(reqBody):

    res = requests.post(
        f"{API_URL}/me/messenger_profile?access_token={PAGE_ACCESS_TOKEN}",
        headers={'Content-Type':'application/json'},
        data=json.dumps(reqBody),
    )

    if res.status_code == 200:
        return "Messenger Profile API called"
    return f"Error while calling Messenger Profile API : {res.status_code}, {res.text}"


def getPersonaAPI():
    res = requests.get(f"{API_URL}/me/personas?access_token{PAGE_ACCESS_TOKEN}")

    if res.status_code == 200:
        return json.loads(res.text)
    return {"_Error": f"{res.status_code} : {res.text}"}


def postPersonaAPI(name, picture_url):
    params = {"name": name, "profile_picture_url": picture_url}

    res = requests.post(
        f"{API_URL}/me/personas?access_token={PAGE_ACCESS_TOKEN}", params=params
    )

    if res.status_code == 200:
        return json.load(res.text)["id"]
    return "Error Occured on POST Persona API"


def callNLPConfigsAPI():

    res = requests.post(
        f"{API_URL}/me/nlp_configs?access_token={PAGE_ACCESS_TOKEN}&nlp_enabled=true"
    )

    if res.status_code == 200:
        return "Request Successful call to NLP Configs API"
    return "Error on calling NLP Configs API"


def callSendAPI(reqBody):

    print(f"Call Send API -> requestBody:{reqBody} ")
    
    res = requests.post(
        f"{API_URL}/me/messages?access_token={PAGE_ACCESS_TOKEN}",
        headers={'Content-Type' : 'application/json'},
        data=json.dumps(reqBody)
        )
    return res


def getUserProfile(senderIGSID):
    res = requests.get(
        f"{API_URL}/{senderIGSID}",
        params={
            "fields": "first_name, last_name, gender, locale, timezone",
            "access_token": PAGE_ACCESS_TOKEN,
        },
    )
    data = json.loads(res.text)
    if res.status_code == 200:

        return {
            "firstName" : data["first_name"],
            "lastName" : data["last_name"],
            "gender" : data["gender"],
            "locale" : data["locale"],
            "timezone": data["timezone"]   
        }
    return {
        "Error" : res.text
    }


class quickReply():

    def __init__(self, title,  content_type=None, payload=None, image_url=None):
        if image_url:
            self.image_url = image_url

        self.content_type = content_type if content_type else "text"
        
        if self.content_type == "text": # To support send email and phone number as quick reply
            self.title = title
            self.payload = payload if payload else (str(title).toUpper()+str(random.randint(100,1000)))

# class Template:
#     def __init__ (self,template_type):
#         self.template_type = template_type

class genericTemplateElement:

    def __init__(self,title, subtitle,image_url, default_action=None,buttons=None):
        
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        if default_action:
            self.default_action = default_action
        if buttons:
            self.buttons = buttons


# class buttonTemplateElement:
#     """ """
#     def __init__(self, text, buttons):
#         self.text = text
#         self.buttons = buttons


class Button:
    def __init__(self, title, postback_or_url, type="postback"):

        self.title = title
        self.type = "postback" if not type == "web_url" else "web_url"
        if self.type == "web_url":
            self.url = postback_or_url
        else:
            self.payload = postback_or_url
            
class sendAPIResponse():
    
    def __init__(self, sender_psid ):

        self.requestDict = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": str(sender_psid)},
            
        }


    def sendText(self, text, quickReplies=None):
        """ Send Text Message 
            quickReplies must be a List of quickReplies object or similiar format """
        self.clearRequestDict()
        self.requestDict["message"] = {}
        self.requestDict["message"]["text"] = text
        if quickReplies:
            self.requestDict["message"]["quick_replies"] = []
            
            # Go through every and turn to then to dictionary
         
            for quickR in quickReplies:
                self.requestDict["message"]["quick_replies"].append(quickR.__dict__ if type(quickR) == quickReply else quickR )
            


        return self

    def sendGenericTemplate(self, elements):
        self.clearRequestDict()
        self.requestDict["message"] = {}
        elements_ = list()
        for ele in elements:
            if type(ele) == dict:
                elements_.append(ele)
            else:
                elements_.append(ele.__dict__)

        self.requestDict["message"]["attachment"] = {
            "type" : "template",
            "payload": {
                "template_type": "generic",
                "elements" : elements_
            }
        }


        return self

    def sendButtonTemplate(self, text, buttons):
        self.clearRequestDict() 
        self.requestDict["message"] = {}

        buttons_ = list()
        for button in buttons:
            if type(button) == dict:
                buttons_.append(button)
            else:
                buttons_.append(button.__dict__)


        self.requestDict["message"]["attachment"] = {
            "type" : "template",
            "payload" : {
                "template_type": "button",
                "text": text,
                "buttons": buttons_
            }
        }

        return self

    def sendSenderAction(self, action):
        """ action may be  mark_seen, typing_on, typing_off"""
        self.clearRequestDict()

        self.requestDict["sender_action"] = action
        return self

    def clearRequestDict(self):
        self.requestDict.pop("message", None)
        self.requestDict.pop("sender_action", None)

        return self

    def send(self):
        response = callSendAPI(self.requestDict)
        if response.status_code != 200:
            print(f"\n\n Send API Error Response {response.status_code} : {response.text} ")
        
        return self