from webexteamsbot import TeamsBot
import json
import requests
from tinydb import TinyDB, Query
from datetime import datetime

db= TinyDB('DB/db.json')

bot_token = 'Zjk3NTY0MzgtNjI1Mi00MDE1LWFmODEtYWUwYzRiOGNhNTgzODYwNWI3NWQtNDE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
bot_name = 'poppy'
bot_email = 'poppybot@webex.bot'
bot_url = 'https://f957cf12.ngrok.io'
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
    inputs = get.json()['inputs']
    db.insert({
	"date": datetime.now().timetuple().tm_yday,
	"user": get_person_details(get.json()['personId']),
	"userId": get.json()['personId'],
	"userAction": inputs['x'],
	"lunchtime": inputs ['lunch'],
	"roomId": get.json()['roomId'],
    })
    return ""
    #return "id: {} answer :{}".format(get_person_details(get.json()['personId']),get.json()['inputs'])

def get_person_details (id):
    url = 'https://api.ciscospark.com/v1/people/' +id
    header = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + bot_token
    }
    get = requests.get(url, headers=header)
    return '{}'.format(get.json()['displayName'])

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

def eat (message):
    #print(message.text)
    card = create_message_with_attachment(message.roomId,'test',attachment = json.loads(lunch_card))
    print (card)
    return ''

def who (message):
    Lunch = Query()
    result = db.search((Lunch.date==datetime.now().timetuple().tm_yday) & (Lunch.userAction=='lunch'))
    lunchtime = {}

    for person in result :
        for time in person["lunchtime"].split(","):
            if time in lunchtime:
                if not (person["user"] in lunchtime[time]):
                    lunchtime[time].append(person["user"])
            else:
                lunchtime[time]=[person["user"]]
    answer = ""
    for item in lunchtime :
        if len(lunchtime[item])>1:
            user = ", ".join(lunchtime[item])
            answer += "{} want to eat at {}h{} \n".format(user,item[0:2],item[2:])
        else:
            user = lunchtime[item][0]
            answer += "{} wants to eat at {}h{} \n".format(user,item[0:2],item[2:])
      
    Lunch = Query()
    result = db.search((Lunch.date==str(datetime.now().timetuple().tm_yday)) & (Lunch.userAction=='no'))
    
    return answer

bot.add_command('attachmentActions','*',attachment)

bot.add_command ("eat",'I will organise lunch',eat)
bot.add_command ('/hello','hello world',hello)
bot.add_command ('who','users eat', who)



bot.run(host='0.0.0.0',port=6000,debug=True)







