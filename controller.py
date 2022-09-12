from flask import Flask, render_template, request
import json

app=Flask( __name__ , template_folder="templates")

emailList=[]
passwordList=[]
wholeCredentials=[]
email = ""
password = ""
name = ""
authentic = ""

class Question:
    question= ""
    option1= ""
    option2= ""
    option3= ""
    option4= ""
    correct= ""
    qnum= ""

class Score:
    name= ""
    email= ""
    score= ""
    
    
#function to spearate username and password     
def getField(line,field): #separating username and password field
    
    storedField=""
    c=''
    idx=0
    commaFound=0   
    #storing the particular field in "storedField"
    #after certain existing commas
    while ( commaFound < field+1 and idx < len(line)):
        
        c=line[idx]
        
        if c == ',':
            commaFound+=1
        elif commaFound == field:
            storedField=storedField+c
        idx+=1    
    return storedField

def making_objects(listElement ,number):
    
    p=Question()
    p.question= getField(listElement, 0)
    p.option1= getField(listElement, 1)
    p.option2= getField(listElement, 2)
    p.option3= getField(listElement, 3)
    p.option4= getField(listElement, 4)
    p.correct= getField(listElement, 5)
    p.qnum= number
    
    return p


def making_marks(listElement):
    s= Score()
    s.name= getField(listElement , 0)
    s.email= getField(listElement , 1)
    s.score= getField(listElement , 3)
    return s
    
@app.route("/quiz" , methods=["POST","GET"])
def quiz():
    qno = 0
    whole_quiz = []
    questions = []
    myFile=open("questions.txt" , "r")
    questions = myFile.read().splitlines()
    myFile.close()
    
    for element in questions:
        qno+=1
        obj= making_objects(element, qno)
        whole_quiz.append(obj)
    
    qno=0
    return render_template("quiz.html" , array=whole_quiz)


@app.route("/index")
def home():
    
    global email
    global password
    
    if email=="admin@host.local" and password == "12789":
        return render_template("admin.html")
    return render_template("profile.html" )

    return render_template("index.html")

#return render_template("showProd.html" , list= objects_list)

@app.route("/onsignup", methods=["POST","GET"])
def submit():
    
    global email
    global password
    global name
    
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    complete= str(name)+ "," +str(email)+ "," +str(password)+ "," +"0"+","+"0"+","+"0"
    
    myFile=open("dataCSV.txt" , "a")
    print(complete , file= myFile , sep="\n")
    myFile.close()
    return render_template("index.html")

@app.route("/onlogin" , methods=["POST","GET"])
def userVerify():
    
    global email
    global password
    global wholeCredentials
    global authentic
    email=request.form.get('email')
    name=request.form.get('name')
    password=str(request.form.get('password'))
    
    myFile=open("dataCSV.txt" , "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()
    
    if email=="admin@host.local" and password== "12789":
        return render_template("admin.html")

    with open('Quizes/chekoduadarsh_1.json', 'r') as f:
        data = json.load(f)
    return render_template("profile.html" , var=name, quizdata =data)

    
def verify( email , pw ):
    
    emailList = []
    passwordList = []
    global authentic
    
    wholeCredentials = []
    
    myFile=open("dataCSV.txt" , "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()
    
    for idx in range(0, len(wholeCredentials)):
        emailList.append(getField( wholeCredentials[idx] , 1 ))
        passwordList.append(getField( wholeCredentials[idx] , 2 ))
    
    print(len(wholeCredentials))
    print(len(emailList))
    print(len(passwordList))
    
    for idx in range( 0 , len(emailList)):
        if email == emailList[idx] and pw == passwordList[idx]:
            authentic = getField( wholeCredentials[idx] , 0 )
            print(authentic)
            return True 
    return False

@app.route("/showall" , methods=["POST","GET"])
def showll():
    
    objects_list = []
    whole= []
    myFile=open("dataCSV.txt" , "r")
    whole = myFile.read().splitlines()
    myFile.close()
    num = 0
    for element in whole:
        
        obj = making_marks(element)
        objects_list.append(obj)
        
    return render_template("showall.html" , list= objects_list)



@app.route("/addquestion" , methods=["POST","GET"])
def add_question():
    inp = dict(request.form)
    print(request.form)
    #write to json
    with open('static/Quizes/chekoduadarsh_1.json', "r") as file:
        fdata = json.load(file)
    if(inp["quizID"] != "None"):

        for idx, obj in enumerate(fdata):
            if obj['quizID'] == inp["quizID"]:
                fdata.pop(idx)



        data = {"quizName": inp["labelQuizName"],
            "grade": inp["labelGrade"],
            "quizID": "0"if len(fdata)== 0 else str(int(fdata[len(fdata)-1]["quizID"])+1),
            "subGrade": inp["labelSubGrde"],
            "topic": inp["labelQuizTopic"],
            "quizDisc": inp["quizDisc"],
            "quizHour": "0",
            "quizMinutes": inp["labelMinute"],
            "quizSubject": inp["labelSubject"],
            "quizMedium": inp["labelMedium"],
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
            question["score"] = inp['q'+qid+'Score']
            question["selected"] = []
            options = []
            correct = []
            for x in inp:
                if "q"+qid in x:
                    if 'q'+qid+'op' in x:
                        options.append(inp[x])
                    
                    if 'q'+qid+'answer' in x:
                        correct.append(inp['q'+qid+'op'+x[-1]])

            question["options"] = options
            question["correctAnswer"] = correct

            questions.append(question)

            print(questions)

        data["questions"] = questions  
        fdata.append(data)
        # 3. Write json file
        with open('static/Quizes/chekoduadarsh_1.json', "w") as file:
            json.dump(fdata, file) 
        return render_template("profile.html")

    data = {"quizName": inp["labelQuizName"],
            "grade": inp["labelGrade"],
            "quizID": "0"if len(fdata)== 0 else str(int(fdata[len(fdata)-1]["quizID"])+1),
            "subGrade": inp["labelSubGrde"],
            "topic": inp["labelQuizTopic"],
            "quizDisc": inp["quizDisc"],
            "quizHour": "0",
            "quizMinutes": inp["labelMinute"],
            "quizSubject": inp["labelSubject"],
            "quizMedium": inp["labelMedium"],
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
        question["score"] = inp['q'+qid+'Score']
        question["selected"] = []
        options = []
        correct = []
        for x in inp:
            if "q"+qid in x:
                if 'q'+qid+'op' in x:
                    options.append(inp[x])
                
                if 'q'+qid+'answer' in x:
                    correct.append(inp['q'+qid+'op'+x[-1]])

        question["options"] = options
        question["correctAnswer"] = correct

        questions.append(question)

        print(questions)

    data["questions"] = questions

    fdata.append(data)
    # 3. Write json file
    with open('static/Quizes/chekoduadarsh_1.json', "w") as file:
        json.dump(fdata, file)
        
    return render_template("profile.html")
    

@app.route("/submit" , methods=["POST","GET"])
def submit_quiz():
    print(request.form)
    global email
    wholeCredentials = []
    
    attempts = []
    score = 0
    whole_quiz = []
    
    myFile=open("questions.txt" , "r")
    questions = myFile.read().splitlines()
    myFile.close()
    number=0
    for element in questions:
        obj= making_objects(element , number)
        whole_quiz.append(obj)
    
    for idx in range(0,len(whole_quiz)):
        mcq="mcq"+str(idx+1)
        attempts.append(request.form.get(mcq))
    
    for udx in attempts:
        print(udx)
    
    for idx in range(0,len(whole_quiz)):
        if whole_quiz[idx].correct == attempts[idx]:
            score+=1
    
    myFile=open("dataCSV.txt" , "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()
    
    for idx in range(0,len(wholeCredentials)):
        if email==getField(wholeCredentials[idx],1):
            wholeCredentials[idx]= str(getField(wholeCredentials[idx],0))+ ","+str(getField(wholeCredentials[idx],1))+ "," +str(getField(wholeCredentials[idx],2))+ "," +str(score)+ "," +str(len(attempts))+ "," +str(len(whole_quiz))
    
    myFile=open("dataCSV.txt" , "w")
    for record in wholeCredentials:
        print(record , file= myFile , sep="\n")
    
    myFile.close()

    print("Your score is:", score)
    return render_template("profile.html")



@app.route("/" , methods=["POST","GET"])
def validation():
    return render_template("login.html")


@app.route("/show" , methods=["POST","GET"])
def results():
    global email
    wholeCredentials = []
    attempts = 0
    myFile=open("dataCSV.txt" , "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()
    
    score = 0
    print(email)
    for result in wholeCredentials:
        check = getField(result, 1)
        if email == check:
            score = str(getField(result, 3))
            attempts = str(getField(result, 4))
    return render_template("result.html" , var1=score, var2=attempts)

@app.route("/register" , methods=["POST","GET"])
def register():
    return render_template("register.html")

@app.route("/makeQuiz" , methods=["POST","GET"])
def makeQuiz():
    return render_template("makeQuiz.html")

@app.route("/score" , methods=["POST","GET"])
def score():
    score = request.args.get('Score')
    userID = request.args.get('user')
    quizID = request.args.get('quizID')
    myFile=open("userscore.csv" , "r")
    data = myFile.read().splitlines()
    myFile.close()
    data.append(userID+","+quizID+","+score)
    myFile=open("userscore.csv" , "w")
    for d in data:
        print(d , file= myFile , sep="\n")
    myFile.close()
    return render_template("Score.html", Score =score)

@app.route("/quizOn" , methods=["POST","GET"])
def quizOn():
    quizID = request.args.get('quizID')
    with open('static/Quizes/chekoduadarsh_1.json', 'r') as f:
        data = json.load(f)
    for d in (data):
        if d["quizID"] == quizID:
          return render_template("game.html", quizdata =d)
    return render_template("profile.html")

@app.route("/contact" , methods=["POST","GET"])
def get_social():
    return render_template("contact.html")

@app.route("/add" , methods=["POST","GET"])
def add():
    labelQuizName = request.args.get('labelQuizName')
    labelQuizTopic = request.args.get('labelQuizTopic')
    labelGrade = request.args.get('labelGrade')
    labelSubGrde = request.args.get('labelSubGrde')
    labelQuizShare = request.args.get('labelQuizShare')
    labelMinute = request.args.get('labelMinute')
    quizDisc = request.args.get('quizDisc')
    labelSubject = request.args.get('labelSubject')
    labelMedium = request.args.get('labelMedium')
    quizID = request.args.get('quizID')
    return render_template("addques.html",labelQuizName=labelQuizName,labelQuizTopic=labelQuizTopic,labelGrade=labelGrade,labelSubGrde=labelSubGrde,labelQuizShare=labelQuizShare, labelMinute=labelMinute,quizDisc=quizDisc, labelMedium=labelMedium,quizID=quizID)

@app.route("/profile" , methods=["POST","GET"])
def profile():

    global authentic
    return render_template("profile.html", var=authentic)


@app.route("/logout" , methods=["POST","GET"])
def logout():
    global email
    global password
    email = ""
    password= ""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug= True , host="localhost")