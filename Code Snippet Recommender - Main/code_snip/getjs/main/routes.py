# Routes just calls User class methods from models.py upon receiving form values
from flask import Flask, render_template, redirect, url_for, request, session
import flask
from app import app
from main.models import User

templist = []
mylist = []


@app.route('/register', methods=['POST'])
def signup():
    return User().signup()


@app.route('/signout')
def signout():
    return User().signout()


@app.route('/login', methods=['POST'])
def login():
    print("reached login route")
    return User().login()


@app.route('/uploadsnip', methods=['POST'])
def upload():
    return User().upload()


@app.route('/', methods=["POST"])
def search():
    print("route:index form submit")
    global mylist
    global templist
    templist = User().searchSnippet(request.form.get('search'))
    mylist = templist[1]
    # for i in mylist:
    #         print(i,end="\n\n")
    # searchsnip(mylist)
    return User().searchSnippet(request.form.get('search'))
    # return render_template('/searchsnippet.html', results = mylist)


@app.route('/userhome', methods=["POST"])
def logsearch():
    print("route:logsearch form submit")
    global mylist
    global templist
    templist = User().searchSnippet(request.form.get('search'))
    mylist = templist[1]
    # for i in mylist:
    #         print(i,end="\n\n")
    # searchsnip(mylist)
    return User().searchSnippet(request.form.get('search'))


@app.route('/searchsnippet')
def searchsnip():
    print("searchsnip me ghusa")
    print(templist[0])
    return render_template('/searchsnippet.html', results=mylist, len=len(mylist), searchby=templist[0])


@app.route('/logsearchsnippet')
def logsearchsnip():
    print(templist[0])
    return render_template('/logsearchsnippet.html', results=mylist, len=len(mylist), searchby=templist[0])


@app.route('/viewsnipFunc')
def viewsnip():
    UserSnippetList = []
    UserSnippetList = User().getUserSnippets()

    return render_template('/viewsnip.html', results=UserSnippetList, len=len(UserSnippetList))


@app.route('/profile/')
# @login_required
def profile():
    count = User().getUserSnippetCount()
    return render_template('profile.html', snippetCount=count)


@app.route('/searchall')
def searchall():
    print(templist[0])
    return render_template('/searchall.html', results=mylist, len=len(mylist), searchby=templist[0])


@app.route('/logsearchall')
def logsearchall():
    print(templist[0])
    return render_template('/logsearchall.html', results=mylist, len=len(mylist), searchby=templist[0])


@app.route('/freqsearch')
def freqsearch():
    print("Entered")
    freqlist = []
    freqlist = User().freq_search()
    modified_list = freqlist[:10]
    return render_template('/freqsearch.html', modified_list=modified_list)


@app.route('/vote')
def vote():
    layout = flask.request.args.get('layout')
    print("Got the value")
    print(layout)
    num = str(layout).split("/")
    mydict = num[0][10:-2]
    print("see num")
    print(num)
    if (num[1] == '+1'):
        # upvote
        User().ratingplus(mydict)
    else:
        # downvote
        User().ratingminus(mydict)
    global mylist
    global templist
    templist = User().searchSnippet("")
    mylist = templist[1]
    return flask.jsonify({'html': flask.render_template('index.html', target=layout)})


@app.route('/about')
def about():
    return render_template('/about.html')
