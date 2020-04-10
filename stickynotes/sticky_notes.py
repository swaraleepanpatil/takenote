import os
from flask import Flask, request,Response,render_template,redirect,url_for,session
import pymysql
from new_connection import execute_query


app = Flask(__name__)
app.secret_key = os.urandom(12)

conn=pymysql.connect(host='localhost',user='swaralee',passwd='swaralee@123',db='StickyNotes')
cur= conn.cursor()

@app.route('/')


@app.route('/signup',methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        full_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        sql_query="SELECT * FROM users;"
        signup= execute_query(sql_query)
        for i in signup:
                if email==i[2]:
                    return ('User already exists. please try login.')

        sql_query="INSERT INTO users(full_name,email,password) VALUES ('{}','{}','{}')".format(full_name,email,password)
        execute_query(sql_query,'insert')
          
        return redirect('login')
        
    else:
        return render_template('signup.html')


@app.route('/login', methods=['POST','GET'])
def login():
    data={}
    if session.get('user_id'):
            data['logged in']=True
            
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM users;"
        login=execute_query(sql)
        for i in login:
            if email==i[2] and password==i[4]:
                session['user_id']=i[0]
                print(session['user_id'])
                return redirect('notes')
    
        return("invalid credintials")

    else:
        return render_template('login.html',content=data)
     
@app.route('/logout', methods = ['GET'])
def logout():
    session['user_id']=None
    del session['user_id']   
    return redirect('login')     
    

@app.route('/notes', methods=['POST','GET'])
def notes():
    data={}
    if session.get('user_id'):
        data['logged_in']=True
        
    if request.method == 'POST':
        notes_content=request.form['notes_content']
        sql_query="SELECT * FROM stickynotes;"
        notes= execute_query(sql_query)
        
        sql_query="INSERT INTO stickynotes(notes_content,user_id) VALUES ('{}','{}');".format(notes_content,session['user_id'])
        execute_query(sql_query,'insert')
        return redirect('/notes')
        
    else:
        return render_template('notes.html',content=data)

        
if __name__ == '__main__':
    
    app.run(debug=True)
