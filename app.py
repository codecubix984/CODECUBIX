from datetime import date, datetime
import sqlite3
from logging import error
from re import template
from flask import Flask,render_template,request,session
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.config["SECRET_KEY"]="1324"
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/mycreation', methods=['GET', 'POST'])
def mycreation():
    return render_template('mycreation.html')


@app.route('/bmicalc', methods=['GET', 'POST'])
def bmicalc():
    if request.method=='GET':
        return render_template('bmi.html')
    name=request.form.get('name')    
    height=request.form.get('height', type=int)
    weight=request.form.get('weight', type=int)
    result=''
    bmi=weight/((height/100)**2)
    bmi=round(bmi,2)
    if bmi<18.5:
        result='underweight'
    elif bmi>=18.5 and bmi<=24.9:
        result='ideal person'
    elif bmi>24.9 and bmi<=29.9:
        result='overweight'
    elif bmi>29.9:
        result='obese'

    conn = sqlite3.connect('codecubix.db')
    cur = conn.cursor()
    cur.execute('SELECT name from bmi')
    records_name=cur.fetchall()
    names=[]
    for i in records_name:
        names.append(i[0])
    if name in names:
        return render_template('bmi.html', message2='Name already exists')
    cur.execute('''
    INSERT INTO bmi (name, weight, height, bmi, body_type)
    VALUES(?, ?, ?, ?, ?)''', (name, weight, height, bmi, result))
    records = cur.execute('SELECT * FROM bmi').fetchall()
    print(records)
    conn.commit()
    conn.close()
    message='your bmi is '+str(bmi)+' and you are '+result
    return render_template('bmirec.html', message=message, records=records)

@app.route('/addition', methods=['POST', 'GET'])
def addition():
    if request.method=='GET':
        return render_template('calc.html')

    num1=request.form.get('number1')
    num1=int(num1)
    num2=request.form.get('number2')
    num2=int(num2)
    result=0
    error=''
    if request.form.get('calc')=='add':
        result=num1+num2
    elif request.form.get('calc')=='sub':
        result=num1-num2
    elif request.form.get('calc')=='multi':
        result=num1*num2 
 
    elif request.form.get('calc')=='divi':

        if num2!=0:
            result=num1/num2
        else:
            error='this operation cannot be performed since num2 is 0'
    
    return render_template('calc.html',add=result,error=error)



@app.route('/q1')  
def q1():
    return render_template('space.html') 

@app.route('/validateq1',methods=['post']) 
def validateq1():
    user_option=request.form.get('quiz')
    message=''
    score=0
    if user_option=='option1':
        message='your ans is correct'
        score=score+10
    else:
        message='wrong ans correct option is number 1'
    session["score"]=score    
    return render_template ('space.html',message=message)  

@app.route('/q2')
def q2():
    return render_template('quiz.html')

@app.route('/validateq2',methods=['post'])
def validateq2():
    user_option=request.form.get('quiz2')
    message=''
    score=session.get('score')
    if user_option=='q2option3':
        message='good job'
        score=score+10  
    else:
        message='wrong ans'
    session["score"]=score    
    return render_template ('space.html',message2=message)

@app.route('/studentinfo', methods=['GET', 'POST'])
def studentifo():
    if request.method=='GET':
        return render_template('students.html')
    name=request.form.get('name')
    marks=request.form.get('marks', type=int)    
    conn= sqlite3.connect('codecubix.db')
    cur=conn.cursor()
    #cur.execute('CREATE TABLE students(name TEXT, marks REAL)')
    cur.execute('''
    INSERT INTO students (name, marks)
    VALUES (?, ?)''', (name, marks))
    records = cur.execute('SELECT * FROM students').fetchall()
    print(records)
    conn.commit()
    conn.close()
    return render_template('students.html', records=records)

@app.route('/commentstart', methods=['GET', 'POST'])
def commentstart():
    if request.method=='GET':
        return render_template('commentstart.html')
    name=request.form.get('username')
    session['username']=name
    return render_template('comments.html')

@app.route('/comments', methods=['GET', 'POST'])
def comment():
    if request.method=='GET':
        return render_template('comments.html')
    userinp= request.form.get('userinp')
    name= request.form.get('name')
    conn = sqlite3.connect('codecubix.db')
    cur = conn.cursor()
    #cur.execute('CREATE TABLE comment(userinp TEXT, name TEXT)')
    cur.execute('''
    INSERT INTO comment (userinp, name)
    VALUES(?, ?)''', (userinp, name))
    records = cur.execute('SELECT * FROM comment').fetchall()
    print(records)
    conn.commit()
    conn.close()
    return render_template('comments.html', records=records)    


            





if __name__=="__main__":
    app.run(debug=True)