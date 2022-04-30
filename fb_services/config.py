import os

API_URL= "https://graph.facebook.com/v13.0"
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
SHOP_URL = os.environ.get("SHOP_URL")
APP_URL = os.environ.get("APP_URL") #heroku website link
WEBHOOK_URL = APP_URL +'/webhook'
PERSONAS = dict()
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

NEW_PERSONAS = [
    {
        "name" : "Hari",
        "picture" : f"{APP_URL}/personas/sales.jpg"
    },
    {
        "name" : "Sita",
        "picture" : f"{APP_URL}/personas/care.jpg"
    }
]

def PUSH_PERSONA(persona):
    PERSONAs[persona['name']] = persona['id']

WHITELISTED_DOMAINS =[APP_URL, SHOP_URL]