from webexteamsbot import TeamsBot
import json
import requests

bot_token = 'Zjk3NTY0MzgtNjI1Mi00MDE1LWFmODEtYWUwYzRiOGNhNTgzODYwNWI3NWQtNDE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
bot_name = 'poppy'
bot_email = 'poppybot@webex.bot'
bot_url = 'https://0b08d2b3.ngrok.io'
bot = TeamsBot(
    bot_name,
    teams_bot_token=bot_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[{"resource":"messages", "event":"created"},
    {"resource":"attachmentActions","event":"created"}])
lunch_card = """
{
    "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.0",
    "body": [
        {
            "type": "TextBlock",
            "text": "Plans for lunch",
            "size": "Large",
            "weight": "Bolder"
        },
        {
            "type": "TextBlock",
            "text": "Atlantis - Paris ILM",
            "isSubtle": true
        },
        {
            "type": "TextBlock",
            "text": "Eat at "
        },
        {
            "type": "Input.ChoiceSet",
            "id": "lunch",
            "value": "1200",
            "choices": [
                {
                    "title": "12:00",
                    "value": "1200"
                },
                {
                    "title": "12:30",
                    "value": "1230"
                },
                {
                    "title": "13:00",
                    "value": "1300"
                }
            ],
            "isMultiSelect": true
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Count me in",
            "data": {
                "x": "lunch"
            }
        },
        {
            "type": "Action.Submit",
            "title": "No thanks",
            "data": {
                "x": "no"
            }
        }
    ]
}
}
"""
def attachment (api, message):
    header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + bot_token
    }
    url = 'https://api.ciscospark.com/v1/attachment/actions/'+message['data']['id']
    get = requests.get(url, headers=header)
    return "id: {} answer :{}".format(get_person_details(get.json()['personId']),get.json()['inputs'])

def get_person_details (id):
    url = 'https://api.ciscospark.com/v1/people/' +id
    header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + bot_token
    }
    get = requests.get(url, headers=header)
    return 'displayName {}'.format(get.json()['displayName'])

def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + bot_token
    }

    url = 'https://api.ciscospark.com/v1/messages'
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def hello (incommingmessage):
    return 'hello world'

def who (message):
    #print(message.text)
    card = create_message_with_attachment(message.roomId,'test',attachment = json.loads(lunch_card))
    print (card)
    return ''


bot.add_command('attachmentActions','*',attachment)

bot.add_command ('who','I will organise lunch',who)
bot.add_command ('/hello','hello world',hello)




bot.run(host='0.0.0.0',port=6000,debug=True)







