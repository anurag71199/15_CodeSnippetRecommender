from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

#Anurag's dummy db
# client = pymongo.MongoClient('mongodb+srv://anurag71199:aghoshmongodb.com01@cluster0.nqlhs2t.mongodb.net/?retryWrites=true&w=majority')
#db = client.get_database('ssdprojectdb')

#SSD project db
client = pymongo.MongoClient('mongodb+srv://all:Project1@ssdproject.gp7612k.mongodb.net/?retryWrites=true&w=majority')
db = client.get_database('ssdproject')
user_collection = db.UserCredentials  #need to make variables for other collections and pass it. Refer to models.py imports

snippet_collection = db.SnippetDetails #need to make variables for other collections and pass it. Refer to models.py imports


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


# Routes

from main import routes
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/searchsnippet')
# def searchsnip():
#     return render_template('searchsnippet.html')

@app.route('/login')
def loginfunc():
    return render_template('login.html')

@app.route('/register')
def registerfunc():
    return render_template('register.html')


@app.route('/userhome/')
@login_required
def dashboard():
    return render_template('userhome.html')

@app.route('/uploadsnip/')
@login_required
def uploadsnip():
    return render_template('uploadsnippet.html')


#Ignore this code

# from flask import Flask, render_template, session, redirect
# from functools import wraps

# from .main.routes import main
# from .extensions import mongo


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

#     app.config['MONGO_URI'] = 'mongodb+srv://anurag71199:aghoshmongodb.com01@cluster0.nqlhs2t.mongodb.net/ssdprojectdb?retryWrites=true&w=majority'

#     mongo.init_app(app)
    
#     app.register_blueprint(main)
#     return app