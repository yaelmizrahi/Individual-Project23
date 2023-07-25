from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

#Code goes below here
firebaseConfig = {
  "apiKey": "AIzaSyCDjiGy5LyRwcRtbRc73pZuuAgz3qOgWa0",
  "authDomain": "personal-cs-project.firebaseapp.com",
  "databaseURL": "https://personal-cs-project-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "personal-cs-project",
  "storageBucket": "personal-cs-project.appspot.com",
  "messagingSenderId": "529384358712",
  "appId": "1:529384358712:web:133ca5e0932c1e41cff7cd"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#SIGN IN ROUTE
@app.route('/', methods=['GET', 'POST'])
def signIn():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signIn.html")

#SIGN UP ROUTE
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       full_name = request.form['full_name']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email" : email,
                    "password" : password,
                    "full_name" : full_name
            }
            db.child("users").child(UID).set(user)
            return redirect(url_for("home"))
       except:
           error = "Authentication failed"
    return render_template("signUp.html")

#FUNCTION RANDOM QUESTION
def RandomQuestion():
    login_session['question'] = "hey"
    return None

#HOME ROUTE
@app.route('/home', methods=['GET', 'POST'])
def home():
    error = ""
    if request.method == 'POST':
       answer = request.form['answer']
       try:
            qa = {  "question" : login_session['question'],
                    "answer" : answer
            }
            db.child("answers").push(qa)
            return redirect(url_for("answers"))
       except:
           error = "Authentication failed"
    RandomQuestion()
    return render_template("home.html", question = login_session['question'])

#ANSWERS ROUTE
@app.route('/answers', methods=['GET', 'POST'])
def answers():
    UID = login_session['user']['localId']
    answersDic = db.child("answers").get().val()
    return render_template("answers.html", answers = answersDic, uid = UID)



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)