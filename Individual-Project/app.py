from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import random 

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
            return redirect(url_for('home'))
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
    reflection_questions = {
    "1": "What were the highlights of my day?",
    "2": "What challenges did I face today, and how did I handle them?",
    "3": "What emotions did I experience today, and what triggered them?",
    "4": "Did I make progress toward my goals? If yes, how? If not, why?",
    "5": "What made me feel grateful today?",
    "6": "How did I show kindness or support to others?",
    "7": "What did I learn today, and how can I apply it in the future?",
    "8": "Did I take care of my physical and mental well-being today? If not, what can I do differently tomorrow?",
    "9": "What activities brought me joy and fulfillment?",
    "10": "Was there a moment of self-discovery or realization today?",
    "11": "Did I have any moments of self-doubt, and how can I overcome them?",
    "12": "Did I make meaningful connections with others today?",
    "13": "What choices or decisions did I make today, and are they aligned with my values?",
    "14": "What could I have done differently to improve my day?",
    "15": "What are my priorities for tomorrow, and how can I prepare for a successful day?"
    }
    num = str(random.randint(1, 15))
    login_session['question'] = reflection_questions[num]
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
            db.child(login_session['user']['localId']).child("answers").push(qa)
            return redirect(url_for("answers"))
       except:
           error = "Authentication failed"
    RandomQuestion()
    print(login_session['user']['localId'])
    user = db.child("users").child(login_session['user']['localId']).get().val()
    return render_template("home.html", question = login_session['question'], full_name = user["full_name"])

#ANSWERS ROUTE
@app.route('/answers', methods=['GET', 'POST'])
def answers():
    UID = login_session['user']['localId']
    answersDic = db.child(UID).child("answers").get().val()
    print(answersDic)
    return render_template("answers.html", answers = answersDic, uid = UID)

@app.route('/logOut')
def logOut():
    login_session['user'] = None
    auth.current_user = None
    return render_template("signIn.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)