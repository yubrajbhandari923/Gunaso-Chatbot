import os, json, openai, random
from django.shortcuts import render
from django import http
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from fb_services.profile import Profile
from fb_services.config import *
from fb_services.FBAPI import (
    callNLPConfigsAPI,
    callSendAPI,
    sendAPIResponse,
    genericTemplateElement,
    Button,
)
from api.models import GptBot, Hospital, Doctor, Ambulance, Violence, DisasterRelif
from fb_services.payloads import get_started_payload

openai.api_key = OPENAI_API_KEY


def img_url_(name):
    """Turns Image Name to link"""
    return f"{APP_URL}/static/img/{name}.jpg"
class WebHookView(View):
    


    def handleMessage(self, sender_psid, recieved_message):
        sendAPIResponse(sender_psid).sendSenderAction("typing_on").send()

        text = recieved_message.get("text")

        try:
            try:

                g = GptBot.objects.get(psid=sender_psid)
                # print("Foound OBJECT")
            except Exception:
                g = GptBot.objects.create(psid = sender_psid, prompt="Human: Hey, how are you doing?\nAI: I'm good! What would you like to chat about?")
                g.save()
                # print("Created OBJECT")
            
            prompt = g.prompt+f"\nHuman:{text}\nAI:"
            print(f"prompt : {prompt} ")

            response = openai.Completion.create(
                engine="davinci",
                prompt=str(prompt),
                temperature=0.9,
                top_p=1,
                max_tokens=512,
                stop=["\nHuman:"],
                frequency_penalty=0,
                presence_penalty=0.6,
            ).to_dict()["choices"][0]["text"]

            # response = response[(response.find("?") + 1) :]  # remove text before ?
            # response = "".join((response + "aa").split(".")[:-1])  # remove after last .
            
            g.prompt = prompt + response
            g.save()
        except Exception:
            response = "Sorry i didn't understood you"

        sendAPIResponse(sender_psid).sendText(response).send()
        # if recieved_message.get("text"):
        #     text = recieved_message.get("text")

        # if recieved_message.get("attachments"):
        #     url_ = recieved_message.get("attachments")[0]["payload"]["url"]
        #     # res["message"]["text"] = f"URL : {url_} "

        #     res["message"]["attachment"] = {
        #         "type": "template",
        #         "payload": {
        #             "template_type": "generic",
        #             "elements": [
        #                 {
        #                     "title": "Is this the right picture?",
        #                     "subtitle": "Tap a button to answer.",
        #                     "image_url": f"{APP_URL}/static/img/welcome.jpg",
        #                     "buttons": [
        #                         {
        #                             "type": "postback",
        #                             "title": "Yes!",
        #                             "payload": "yes",
        #                         },
        #                         {
        #                             "type": "postback",
        #                             "title": "No!",
        #                             "payload": "no",
        #                         },
        #                     ],
        #                 }
        #             ],
        #         },
        #     }

        # response = callSendAPI(res)

        # print(f"\nHandle Messege\n {response.status_code} : {response.text} ")

    def handlePostback(self, sender_psid, recieved_postback):

        payload = recieved_postback["payload"]

        if payload == "GET_STARTED":
            sendAPIResponse(sender_psid).sendText(
                "Hello, Thank you for reaching out. Hope you are doing well."
            ).send().sendText(
                "Here is the list of services I provide."
            ).send().sendGenericTemplate(
                [
                    genericTemplateElement(
                        "Health Services",
                        "",
                        img_url_("health2"),
                        buttons=[Button("Yes", "SERVICE_1").__dict__],
                    ),
                    genericTemplateElement(
                        "Mental Health Relief",
                        "",
                        img_url_("mental2"),
                        buttons=[Button("Yes", "SERVICE_2").__dict__],
                    ),
                    genericTemplateElement(
                        "Violence Prevention",
                        "",
                        img_url_("violence1"),
                        buttons=[Button("Yes", "SERVICE_3").__dict__],
                    ),
                    genericTemplateElement(
                        "Disaster Rescue",
                        "",
                        img_url_("disaster2"),
                        buttons=[Button("Yes", "SERVICE_4").__dict__],
                    ),
                ],
            ).send()

        if payload[:7] == "SERVICE":
            sendAPIResponse(sender_psid).sendButtonTemplate(
                "Do you want to get connected to Service Providers near you or get help from our ChatBot?",
                [
                    Button("Provide me Service Providers", "SPROVIDER_SERVICE_"+payload.split("_")[1]),
                    Button("I wanna talk", "TALK_SERVICE_"+payload.split("_")[1]),
                ],
            ).send()

        if payload[:4] == "TALK":
            sendAPIResponse(sender_psid).sendText("Hola amigo, I am GPT 3").send()

        if payload[:9] == "SPROVIDER":
            sendAPIResponse(sender_psid).sendText(
                "Please share us your location (with country) so that we can provide you relevant service providers"
            ).send()
            g = GptBot.objects.get(psid=sender_psid)
            g.is_address = True
            g.service_id = payload.split("_")[2]
            g.save()

        return

    def handleAddress(self, sender_psid, recieved_message):
        sendAPIResponse(sender_psid).sendSenderAction("typing_on").send()

        text = recieved_message.get("text")
        g = GptBot.objects.get(psid=sender_psid)
        s = sendAPIResponse(sender_psid)
       
        if g.service_id == 1:
            """Health Service"""
            hospitals_queryset = Hospital.objects.all()
            
            r1, r2, r3 = random.sample(range(0, hospitals_queryset.count()), 3)
            
            for i, j in enumerate([r1, r2, r3]):
                s.sendText(f"Hospitals: \n {j}. {hospitals_queryset[i].name}, {hospitals_queryset[i].address} ").send()

            ambulances = Ambulance.objects.all()

            r1, r2, r3 = random.sample(range(0, ambulances.count()), 3)
            
            for j,i in enumerate([r1, r2, r3]):
                s.sendButtonTemplate(f"Ambulances: \n {j}. {ambulances[i].name}, {ambulances[i].hospital_name}, {ambulances[i].phone} ", buttons = [Button("Call Now", "CALL AMBULANCE")] ).send()

        if g.service_id == 2:
            """Mental Health"""

            hospitals_queryset = Hospital.objects.all()
            doctors = Doctor.objects.all()
            r1, r2, r3 = random.sample(range(0, min(hospitals_queryset.count(), doctors.count())), 3)
            
            for j,i in enumerate([r1, r2, r3]):            
                s.sendText(f"Consult Doctors Available: {j}. {doctors[i].name} at {hospitals_queryset[i].name}, {hospitals_queryset[i].address} ").send()
            
        if g.service_id == 3:
            """ Violence """
            pass
        g.service_id = 0
        g.save()
    
    def get(self, req, format=None):
        """Verify our webhook."""

        challenge = req.GET.get("hub.challenge")
        if (
            req.GET.get("hub.verify_token") == VERIFY_TOKEN
            and req.GET.get("hub.mode") == "subscribe"
        ):
            print(
                f"\n\n WEBHOOK VERIFIED: {challenge} : {req.GET.get('hub.challenge')} \n\n"
            )
            return HttpResponse(challenge)
        return HttpResponseForbidden()

    @csrf_exempt
    def post(self, req, format=None):
        """{"object":"page",
        "entry":[{"id":"102208592487070","time":1651280540163,
            "messaging":[{"sender":{"id":"7623554920995436"},"recipient":{"id":"102208592487070"},
                        "timestamp":1651279490554,
                        "message":{"mid":"m_iYu3nxv5U5_x7Bya7L7WduoUYteJVLlbATqo_SN5H3iXABalKc_KbzpENA-C9B37g8ZtO2UU7rrJx4f_gY8Dcg",
                           "text":"Hello",
                            "nlp":{"intents":[],"entities":{},"traits":{"wit$sentiment":[{"id":"5ac2b50a-44e4-466e-9d49-bad6bd40092c","value":"positive","confidence":0.5435}],
                            "wit$greetings":[{"id":"5900cc2d-41b7-45b2-b21f-b950d3ae3c5c","value":"true","confidence":0.9998}]},
                            "detected_locales":[{"locale":"en_XX","confidence":0.5776}]}}}]}]}"""

        print(f"\n\n Recieved Webhook: {req.body} \n")

        body = json.loads(req.body)
        if body.get("object") == "page":

            for entry in body["entry"]:
                # if "changes" in entry:
                webhook_event = entry["messaging"][0]

                sender_psid = webhook_event["sender"]["id"]

                # Sends Seen and Typing
                sendAPIResponse(sender_psid).sendSenderAction(
                    "mark_seen"
                ).send().sendSenderAction("typing_on")


                # print(f"\n\n\n Address:{address}, service_id: {service_id} \n\n\n")
                if webhook_event.get("message"):
                    message = webhook_event.get("message")
                    try: 
                        try:
                            g = GptBot.objects.get(psid=sender_psid)
                        except Exception:
                            g = GptBot.objects.create(psid=sender_psid, prompt="")
                        if g.is_address:
                            g.is_address = False
                            g.save()
                            self.handleAddress(sender_psid, message)
                        else:
                            self.handleMessage(sender_psid, message)
                    
                    except Exception as E:
                        print( f"\n\n\  Got exception {E} \n\n")


                elif webhook_event.get("postback"):
                    postback = webhook_event.get("postback")
                    self.handlePostback(sender_psid, postback)

            return HttpResponse("EVENT_RECIEVED")

        return HttpResponse("RECIEVED")


class ProfileView(View):
    def get(self, req, format=None):
        """/profile?"""

        token = req.GET.get("verify_token", None)
        mode = req.GET.get("mode", None)

        profile = Profile()
        responseBody = ""
        if mode and token:
            if token == os.environ.get("VERIFY_TOKEN"):
                if mode == "webhook" or mode == "all":
                    profile.setWebhook()
                    print("\n\n Web Hook Set \n\n")
                    responseBody += f"Set App {APP_ID} set to {WEBHOOK_URL} \n"
                if mode == "profile" or mode == "all":
                    profile.setThread()
                    print("\n\n Profile thread Set \n\n")
                    responseBody += f"Set Messenger Profile of PAGE {PAGE_ID} \n"
                if mode == "persona" or mode == "all":
                    profile.setPersonas()
                    print("\n\n Set Persona \n\n")
                    responseBody += f"Set Personas for {APP_ID} \n"
                if mode == "nlp" or mode == "all":
                    callNLPConfigsAPI()
                    print("\n\n Set NLP \n\n")
                    responseBody += f"Enabled Build in NLP for {PAGE_ID} \n "
                if mode == "domains" or mode == "all":
                    profile.setWhitelistedDomains()
                    print("\n\n Set Domains \n\n")
                    responseBody += f"WhitListed Domains Set for {PAGE_ID} \n"
                if mode == "private-reply":
                    profile.setPageFeedWebhook()
                    print("\n\n Set Privaet reply \n\n")
                    responseBody += f"Set Page Body WebHook"

                return HttpResponse(responseBody)
            return HttpResponseForbidden()
        return HttpResponseNotFound()
