import requests
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
    return f"Error: {res.status_code}, {res.text}"


def getPersonaAPI():
    res = requests.get(f"{API_URL}/me/personas?access_token{PAGE_ACCESS_TOKEN}")

    if res.status_code == 200:
        return json.loads(res.text)
    return {"_Error": f"{res.status_code} {res.text}"}


def postPersonaAPI(name, picture_url):
    params = {"name": name, "profile_picture_url": picture_url}

    res = requests.post(
        f"{API_URL}/me/personas?access_token={PAGE_ACCESS_TOKEN}", params=params
    )

    if res.status_code == 200:
        return json.load(res.text)["id"]
    return "Error Occured"


def callNLPConfigsAPI():

    res = requests.post(
        f"{API_URL}/me/nlp_configs?access_token={PAGE_ACCESS_TOKEN}&nlp_enabled=true"
    )

    if res.status_code == 200:
        return "Request Successful"
    return "Error"


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

