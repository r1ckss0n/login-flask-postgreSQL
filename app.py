import os, psycopg2
from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form.get("user")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2 and user:
            user = request.form.get("user")
            db.execute("INSERT INTO users (username, password) VALUES (:username, MD5(:password))",
                {"username": user, "password": password1})
            db.commit()
            return render_template("index.html", user = user)
        else:            
            return render_template("register.html", alert="Insert matching passwords, please")
    
    
    else:   
        return render_template("register.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            user = request.form.get("user")
            password = request.form.get("password1")
            user = db.execute("SELECT username FROM users WHERE username = :username AND password = MD5(:password)",
                {"username": user, "password": password}).fetchone()
            return render_template("index.html", user = user.username)
        except:
            return render_template("index.html", user = "Unable to login")

    else:
        return render_template("login.html")
