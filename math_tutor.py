
"""
import os
from util import *
from pymongo import MongoClient
from flask import render_template


app = Flask(__name__)

client = MongoClient(CONNECTION)
db = client.mathman
    

@app.route('/webhook', methods=['GET'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge', '')
        else:
            return render_template("privacy.html")


@app.route('/webhook', methods=['POST'])
def handle_message():
    try:
        data = request.json 
        if get_message(data):
            message_t , sed_id = get_message(data)
            if "solve" in message_t.lower(): 
                showResults(sed_id , message_t)
            print message_t
    except:
        pass               
    try:
        user = None
        payload = request.get_data()
        sender, message = messaging_events(payload)
        user = db.user.find_one({"fbId": sender})
        if user is None:
            db.user.insert(
                {"fbId": sender, "level": "Expert", "isFirstTime": True, "correctQuestions" : 3})
            user = db.user.find_one({"fbId": sender})

        if message == "Start":
            send_button_template_message(
                sender,
                "Great, What do you want to do ?",
                [
                    generate_button("Learn & Practice", "LEARN"),
                    generate_button("Ask Doubts", "USER_DEFINED_PAYLOAD")
                ]
            )
        elif message == "LEARN":
            send_carasol_items(
                sender,
                [
                    generate_carasol_items(
                        "Operation on numbers",
                        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Arithmetic_symbols.svg/2000px-Arithmetic_symbols.svg.png",
                        "ON"),
                    generate_carasol_items(
                        "Linear Equations in two varaibles",
                        "http://www.mycompasstest.com/wp-content/uploads/2011/01/BBlintwo.png",
                        "LINEAR"),
                    generate_carasol_items(
                        "Quadratic Equations",
                        "https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/Quadratic-equation.svg/769px-Quadratic-equation.svg.png",
                        "QUAD"),
                    generate_carasol_items(
                        "Basic Trignometry",
                        "https://www.mathsisfun.com/images/adjacent-opposite-hypotenuse.gif",
                        "BT")])

        elif message == "ON":
            if user["isFirstTime"]:
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"isFirstTime": False}})
                send_text_message(
                    sender,
                    "Hey! Let's start with some questions so we can know how good you are with particular topic.")
                questionToAsk = medium_operation()
                send_text_message(sender, questionToAsk["question"])
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"lastQuestion": questionToAsk["question"]}})
                buttons = [
                    generate_button("A " + str(questionToAsk["option1"]), payload='incorrect1'),
                    generate_button("B " + str(questionToAsk["option2"]), payload='incorrect2'),
                    generate_button("C " + str(questionToAsk["option3"]), payload='incorrect3')
                ]
                buttons[questionToAsk["answer"]]["payload"] = 'correct'
                send_button_template_message(
                    sender,
                    "Select Your Choice",
                    buttons
                )
            else:
                askQuestion(sender, message)

        elif message == "LINEAR":
            if user["isFirstTime"]:
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"isFirstTime": False}})
                send_text_message(
                    sender,
                    "Hey! Let's start with some questions so we can know how good you are with particular topic.")
                questionToAsk = linear_hard()
                send_text_message(sender, questionToAsk["question"])
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"lastQuestion": questionToAsk["question"]}})
                buttons = [
                    generate_button("A " + str(questionToAsk["option1"]), payload='incorrect1'),
                    generate_button("B " + str(questionToAsk["option2"]), payload='incorrect2'),
                    generate_button("C " + str(questionToAsk["option3"]), payload='incorrect3')
                ]
                buttons[questionToAsk["answer"]]["payload"] = 'correct'
                send_button_template_message(
                    sender,
                    "Select Your Choice",
                    buttons
                )
            else:
                askQuestion(sender, message)


        elif message == 'QUAD':
            if user["isFirstTime"]:
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"isFirstTime": False}})
                send_text_message(
                    sender,
                    "Hey! Let's start with some questions so we can know how good you are with particular topic.")
                questionToAsk = quadhard()
                send_text_message(sender, questionToAsk["question"])
                db.user.update({"fbId": user["fbId"]}, {
                               "$set": {"lastQuestion": questionToAsk["question"]}})
                buttons = [
                    generate_button("A " + str(questionToAsk["option1"]), payload='incorrect1'),
                    generate_button("B " + str(questionToAsk["option2"]), payload='incorrect2'),
                    generate_button("C " + str(questionToAsk["option3"]), payload='incorrect3')
                ]
                buttons[questionToAsk["answer"]]["payload"] = 'correct'
                send_button_template_message(
                    sender,
                    "Select Your Choice",
                    buttons
                )
            else:
                askQuestion(sender, message)

        elif message == "correct":
            send_text_message(sender, "Congralutions you are correct :D")
            showResults(sender, user["lastQuestion"])
            db.user.update({"fbId" : sender}, {"$inc" : {'correctQuestions' : 1}})
            user = db.user.find_one({"fbId" : sender})
            if user["correctQuestions"] == 3:
                db.user.update({"fbId" : sender}, {"$set" : {'correctQuestions' : 0}})
                if user["level"] == "medium":
                    db.user.update({"fbId" : sender}, {"$set" : {'level' : "Expert"}})
                elif user["level"] == "noob":
                    db.user.update({"fbId" : sender}, {"$set" : {'level' : "medium"}})
            askQuestion(sender, message)

        elif message in "incorrect":
            send_text_message(sender, "Oops sounds like you made a mistake :(")
            send_image(sender, "Here is a video tutorial which can help you to learn better")
            showResults(sender, user["lastQuestion"])
            db.user.update({"fbId" : sender}, {"$set" : {'correctQuestions' : 0}})
            user = db.user.find_one({"fbId" : sender})
            if user["correctQuestions"] == 0 or user["correctQuestions"] == -3:
                if user["level"] == "Expert":
                    db.user.update({"fbId" : sender}, {"$set" : {'level' : "medium"}})
                elif user["level"] == "medium":
                    db.user.update({"fbId" : sender}, {"$set" : {'level' : "noob"}})
            askQuestion(sender, message)
        elif message == 'help':
            send_text_message(sender, "You can use our bot to practise questions of certain topics. We will keep adding the topics and improving the bot for better.")    
            
        return "ok" 
    except:
        print "message with shit"
        return "Hello World"


def askQuestion(recipent, chapter):
    user = db.user.find_one({"fbId" : recipent})
    questionToAsk = linear_hard()
    if user["level"] == 'Expert':
        if chapter == 'ON':
            questionToAsk = advacned_operation()
        elif chapter == 'Linear':
            questionToAsk = linear_hard()
        elif chapter == 'QUAD':
            questionToAsk = quadhard()

    elif user["level"] == "medium":
        if chapter == 'ON':
            questionToAsk = medium_operation()
        elif chapter == 'Linear':
            questionToAsk = linear_medium()
        elif chapter == 'QUAD':
            questionToAsk = quadmedium()

    elif user["level"] == "noob":
        if chapter == 'ON':
            questionToAsk = easy_multiply()
        elif chapter == 'Linear':
            questionToAsk = linear_easy()
        elif chapter == 'QUAD':
            questionToAsk = quadeasy()


    send_text_message(recipent, questionToAsk["question"])
    db.user.update({"fbId": user["fbId"]}, {
                   "$set": {"lastQuestion": questionToAsk["question"]}})
    buttons = [
        generate_button("A " + str(questionToAsk["option1"]), payload='incorrect'),
        generate_button("B " + str(questionToAsk["option2"]), payload='incorrect'),
        generate_button("C " + str(questionToAsk["option3"]), payload='incorrect')
    ]
    buttons[questionToAsk["answer"]]["payload"] = 'correct'
    send_button_template_message(
        recipent,
        "Select Your Choice",
        buttons
    )




def init():
    r = requests.post(THREAD_URL,
                      params={"access_token": PAT},
                      data=json.dumps({
                          "setting_type": "call_to_actions",
                          "thread_state": "new_thread",
                          "call_to_actions": [
                              {
                                  "type": "postback",
                                  "title": "Start",
                                  "payload": "Start"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'}
                      )
    print r.text

    r = requests.post(THREAD_URL,
                      params={"access_token": PAT},
                      data=json.dumps({
                          "setting_type": "call_to_actions",
                          "thread_state": "existing_thread",
                          "call_to_actions": [
                              {
                                  "type": "postback",
                                  "title": "Learn & Practice",
                                  "payload": "LEARN"
                              },
                              {
                                  "type": "postback",
                                  "title": "Help",
                                  "payload": "help"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'}
                      )
    print r.text




if __name__ == '__main__':
    init()
    port = int(os.environ.get('PORT', 33507))
    app.run(host="0.0.0.0", port=port, debug=True)
"""

                                  "type": "postback",
from flask import Flask, request
import requests
import json
import traceback
import random
from constants import *
import quiz.py
import learn.py
import contact.py

def mode_switch(message):
    if message == "start":
        name = input("Hello,what's your name?")
        printf("You can learn, quiz or see the teacher")
        printf("Please choose from learn quiz and tutor to get into to our study")
        message = input("what do you want to do?")
        if message == "learn":
            learn()
        else if message == "quiz":
            quiz()
        else:
            contact_tutor()
    
    else if message  == "hold":
        printf("Please have a break"+name)
    
    else:
        printf("Quit math tutor bot, have a good day!"+name)


def contact_tutor():
    T = {'0':'6635','1':'6493','2':'6489','3':'6893'.'4':'6679'}#phone_number dicctionary
    tutor_num = random.randint(0,4)
    if tutor_num:
        Tutor_phone = T[tutor_num]
    else:
        printf("You could learn by yourself")
        
def askques():
    cat = input("which part are you confused about")
    Qus = input("what are you going to ask?")
    if cat == "linear":
        tutor(0,Qus)
    else if cat == "quad":
        tutor(1,Qus)
    else if cat == "hard":
        tutor(2,Qus)
    else if cat == "simple" 
        tutor(3,Qus)
    else:
        tutor(4,Qus)   

def tutor(n,Qus):
    T_Q = {'0':"linear",'1':"quad",'2':"hard",'3':"simple",'4':'other'};
    printf("Hello"+name+", I am your teacher today")
    printf("Do u have any other question?")
    try :
        pass

    except:
        printf("Have a good day")
        pass

if __name__ == '__main__':
    
    message = ("Let us start studying math together")
    mode_switch(message)


"""

def showResults(sender, question):
    try:
        data = get_solution_from_wolfarmAlpha(question)
        items = []
        for item in data:
            send_image(sender, item["img"])
    except:
        pass

"""