from datetime import date, datetime
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

    message='your bmi is '+str(bmi)+' and you are '+result
    return render_template('bmi.html', message=message)

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

if __name__=="__main__":
    app.run(debug=True)