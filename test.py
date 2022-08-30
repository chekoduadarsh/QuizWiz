import json
import random   

inp = dict([('labelQuizName', 'a'), ('labelQuizTopic', 'b'), ('labelGrade', 'v'), ('labelSubGrde', ''), ('labelQuizShare', ''),('quizDisc', 'test'),('owner', 'chekodu.adarsh@gmail.com'), ('labelMinute', '30'), ('question2', '1+1?'), ('q2Score', '1') , ('q2op1', '1'), ('q2op2', '2'), ('q2answer2', 'on'), ('q2op3', '3'), ('q2op4', '4'), ('question3', '2+2 = 4?'), ('q3Score', '1'), ('q3op1', 'True'), ('q3answer1', 'on'), ('q3op2', 'False')])


f = open('static/Quizes/chekoduadarsh_1.json')
data = json.load(f)
data = {"quizName": inp["labelQuizName"],
        "grade": inp["labelGrade"],
        "quizID": "0"if len(data)== 0 else str(int(data[len(data)-1]["quizID"])),
        "subGrade": inp["labelSubGrde"],
        "topic": inp["labelQuizTopic"],
        "quizDisc": inp["quizDisc"],
        "quizHour": "0",
        "quizMinutes": inp["labelMinute"],
        "quizOwner": inp["owner"],
        "quizTarget": ["all"] if inp["labelQuizShare"] == "" else inp["labelQuizShare"].split(",")}


questions = []
qids = []

for x in inp:
    if 'question' in  x:
        qids.append(str(x[-1]))

for qid in qids:
    question = {}
    question["question"] = inp['question'+qid]
    question["selected"] = inp['q'+qid+'Score']
    question["selected"] = []
    options = []
    correct = []
    for x in inp:
        if "q"+qid in x:
            if 'q'+qid+'op' in x:
                options.append(inp[x])
            
            if 'q'+qid+'answer' in x:
                correct.append(inp['q'+qid+'op'+str(x[-1])])

    question["options"] = options
    question["correctAnswer"] = correct

    questions.append(question)

    print(questions)

data["questions"] = questions