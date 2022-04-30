from .FBAPI import *
from .config import *
from .payloads import get_started_payload
import json
class Profile:
    def setWebhook(self):
        print(callSubscriptionAPI())
        print(callSubscribedApps())

    @property
    def getGetStarted(self):
        """ """
        return {"payload": "GET_STARTED"}

    @property
    def getGreeting(self):
        """JS Implementation has some complex transaltion with locales.
        TODO: Make this function similiar to JS(original-coast-clothing demo app) to enable translations
        """
        return [
            {"locale": "default", "text": "Welcome to Veggies App Chatbot"},
        ]

    @property
    def getPersistanceMenu(self):
        return [
            {
                "locale": "default",
                "composer_input_disabled": True, # Disables Typing field
                "call_to_actions": [
                    {
                        "title": "Restart",
                        "type": "postback",
                        "payload": "GET_STARTED",
                    },
                ]
            }
        ]

    def setThread(self):
        """Sets the profile like Get Started page, Default Greeting when get started is clicked and Persistent Menu"""
        profilePayload = {
            "get_started": self.getGetStarted,
        }

        print (f"ProfilePayload : {profilePayload}")
        print(callMessengerProfileAPI(profilePayload))
            
        profilePayload = {
            "greeting" : self.getGreeting,
        }
        print (f"ProfilePayload : {profilePayload}")
        print(callMessengerProfileAPI(profilePayload))
        profilePayload = {
            "persistent_menu": self.getPersistanceMenu
        }
        print (f"ProfilePayload : {profilePayload}")
        print(callMessengerProfileAPI(profilePayload))

    def setPersonas(self):
        newPersonas = NEW_PERSONAS

        personas = getPersonaAPI()

        if not personas.get("_Error", None):
            for persona in personas:
                PUSH_PERSONA({"name":persona["name"], "id": persona["id"]})
        
            existingPersonas = PERSONAS

            for persona in newPersonas:
                if not (persona["name"] in existingPersonas):
                    personaID = postPersonaAPI(persona["name"], persona["picture"])

                    if type(personaID) == int:
                        PUSH_PERSONA({"name": persona["name"], "id": personaID})

    def setWhitelistedDomains(self):
        payload = {"whitelisted_domains": WHITELISTED_DOMAINS}

        callMessengerProfileAPI(payload)

    def setPageFeedWebhook(self):
        callSubscriptionAPI('feeds')
        callSubscribedApps('feeds')