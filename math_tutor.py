from flask import Flask, request
import requests
import json
import traceback
import random
from constants import *
import quiz.py
import learn.py


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