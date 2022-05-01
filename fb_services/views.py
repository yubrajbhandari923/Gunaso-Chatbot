import os, json, openai
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

from fb_services.payloads import get_started_payload

openai.api_key = OPENAI_API_KEY


def img_url_(name):
    """Turns Image Name to link"""
    return f"{APP_URL}/static/img/{name}.jpg"


class WebHookView(View):
    def handleMessage(self, sender_psid, recieved_message):
        text = recieved_message.get("text")

        try:
            response = json.loads(

            openai.Completion.create(
                engine="davinci",
                prompt=text,
                temperature=0.9,
                max_tokens=512,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
            )

        )
        except Exception:
            response = "K Bolya vai, K bolya."

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
                        "Health Services", "", img_url_("img2"), default_action={""}
                    )
                ],
            ).send().sendButtonTemplate(
                "",
                [
                    Button("Disaster Rescue", "SERVICE_4"),
                ],
            ).send()

        if payload[:7] == "SERVICE":
            sendAPIResponse(sender_psid).sendButtonTemplate(
                "Do you want to get connected to Service Providers near you or get help from our ChatBot?",
                [
                    Button("Provide me Service Providers", "SPROVIDER_SERVICE_1"),
                    Button("I wanna talk", "TALK_SERVICE_1"),
                ],
            ).send()

        if payload[:4] == "TALK":
            sendAPIResponse(sender_psid).sendText("Hola amigo, I am GPT 3").send()

        if payload[:9] == "SPROVIDER":
            sendAPIResponse(sender_psid).sendText("Call 911").send()

        return

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

                if webhook_event.get("message"):
                    message = webhook_event.get("message")
                    self.handleMessage(sender_psid, message)

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
