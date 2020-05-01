import random

questions = {} #initiaize a dictionary
score=0

#randomly pick a math problem from 1 to 10
for i in range(10):
    int_a = random.randint(0,10)
    int_b = random.randint(0,10)
    operators = ['+','-','*']
    operator_value = random.choice(operators)
    question = str(int_a)+" "+operator_value+" "+str(int_b)
    answer = str(eval(question))
    question+=": "
    
    #adds the question to questions
    questions.update({question:answer})


for k in questions.keys():
    user_answer=input(k)
    if questions.get(k)==user_answer:
        print("Answer correct")
        score+=1
    else:
        print("Wrong answer")
#show score
print("You got "+str(score)+"points!")
print("good job")