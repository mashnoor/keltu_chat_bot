from flask import Flask, request

from fbmq import Page, QuickReply

from parser import parse_text

import json

PAGE_ACCESS_TOKEN = "EAADcjGUXFQIBAIzPrTw5Hoarh5epWN9q8KR0pxHoWAR38f2Ah1tFxYFLitJVWGHpeVTiYQbZBbvgBw5PhMdFloZBexfHPEB3lfSZBuSgTN8MkKb2gIcuhnIkvdIiDQuXnrE11AEWYZC7NaAe4xf9ORBJAvB3hcd6ap3vTsv7BQZDZD"
page = Page(PAGE_ACCESS_TOKEN)
sender_ids = []
students = []

class Student(object):
    name = ""
    semester = ""
    dept = ""
    academy = ""
    subject = ""
    def __init__(self, sender_id):
        self.sender_id = sender_id

name = ""
semester = ""
dept = ""
academy = ""
subject = ""

app = Flask(__name__)

'''--------------------- REPLIES--------------------------------'''
greeting_replies = "Hello There! What do you want? Chotha, Book or Lab Report?"
goodbye_replies = "Bye bye! Study hard :D"
academy_replies = 'What do you'

@app.route('/', methods=['GET'])
def reply():
    return request.args.get('hub.challenge')

@app.route('/', methods=['POST'])
def webhook():
  print "Requested"

  page.handle_webhook(request.get_data(as_text=True))
  return "ok", 200


def get_reply(text):
    parsed_text = parse_text(text)
    if parsed_text=="" or parsed_text is None:
        return "Sorry, I can't understand what are you saying"
    result = json.loads(parsed_text)
    global semester
    global dept
    global academy
    global subject
    print result
    if result['intent_type'] == 'GreetingIntent':
        return greeting_replies

    elif result['intent_type'] =='GoodbyeIntent':
        return goodbye_replies

    elif result['intent_type'] == 'AcademyIntent':
        academy = result['AcademyKeyword']
        reply = "Niceee! You are looking for " + str(academy) + "."
        if subject=="":
            reply += " What subject " + academy + " do you need?"
            return reply
        elif semester=="":
            reply+= " Which semester do you read in?"
            return reply
        elif dept=="":
            reply+= " Which dept. do you read in?"
            return reply
        else:
            return "Here is what I found for you"

    elif result['intent_type'] == 'DepartmentIntent':
        reply = "Awesome! You are a " + str(result['DepartmentKeyword']) + " student."
        dept = result['DepartmentKeyword']
        if subject == "":
            reply += " Which subject?"
            return reply
        elif semester == "":
            reply += " Which semester do you read in?"
            return reply
        elif academy == "":
            reply += " What do you need? Chotha, Book or Lab Report?"
            return reply
        else:
            return "Here is what I found for you"

    elif result['intent_type'] == 'SubjectIntent':
        reply = ""
        if academy!= "":
            reply = "Cool! You need a " + str(result['SubjectKeyword']) + academy

        subject = result['SubjectKeyword']
        if academy == "":
            reply += " What subject " + academy + " do you need?"
            return reply
        elif semester == "":
            reply += " Which semester do you read in?"
            return reply
        elif dept == "":
            reply += " Which dept. do you read in?"
            return reply
        else:
            return "Here is what I found for you"

    elif result['intent_type'] == 'SemesterIntent':
        reply = "I see! You are a student of " + str(result['SemesterKeyword'])

        semester = result['SemesterKeyword']
        if academy == "":
            reply += " What subject " + academy + " do you need?"
            return reply
        elif subject == "":
            reply += " Which subject?"
            return reply
        elif dept == "":
            reply += " Which dept. do you read in?"
            return reply
        else:
            return "Here is what I found for you"


@page.handle_message
def message_handler(event):

  sender_id = event.sender_id
  if str(sender_id) not in sender_ids:
      sender_ids.append(str(sender_id))
      s = Student(str(sender_id))
      students.append(s)

  message = event.message_text
  print message
  page.send(sender_id, str(get_reply(message)))

if __name__=="__main__":
  app.run(port=9876)