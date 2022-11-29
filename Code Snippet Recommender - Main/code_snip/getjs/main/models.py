#Main backend of the project. All the dealings with the database are defined here
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import user_collection, snippet_collection, db #import the other collection variables here
import uuid
import datetime
from operator import itemgetter
import bson.json_util as json_util
from bson.objectid import ObjectId


### Global Variables ###
searchkey = ""
request_keyword = ""

class User:

    def start_session(self, user):
        print(user)
        del user['password']
        del user['_id']
        session['logged_in'] = True
        session['user'] = user
        print("okay till here")
        return jsonify(user), 200

    def signup(self):

        # print(request.form)

        #Fetch form details
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        contact = request.form.get('contact')
        password = request.form.get('password')
        cpass = request.form.get('confirmpass')
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "username": username,
            "email": email,
            "contact": contact,
            "password": password
        }
        print(user)

        #confirm password
        if password != cpass:
            return jsonify({"error": "Password Mismatch"}), 400

        # Check for existing email address
        if user_collection.find_one({"username": user['username']}):
            return jsonify({"error": "Username in use"}), 400
        
        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if user_collection.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup Unsuccessful"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        print("reached here")
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_collection.find_one({"username": username})
        print(user)

        if user and pbkdf2_sha256.verify(password, user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid credentials"}), 401

    def upload(self):

        name = request.form.get('snipname')
        keywords = request.form.get('keywords')
        arr =keywords.split(',')  
        description = request.form.get('description')
        code = request.form.get('code')
        submitted_by = session['user']['username']#take logged in users name request.form.get('submitted_by')
        upload_date =datetime.datetime.today()  #take todays date   request.form.get('upload_date')
        # Create the user object
        codesnip = {
            "Name": name,
            "Keywords": arr,
            "Description": description,
            "Code": code,
            "Rating": "0",
            "Submitted_by": submitted_by,
            "Upload_date": upload_date,
            "NumOfVotes": "0"
        }
        print(codesnip)

        if snippet_collection.insert_one(codesnip):
            return jsonify({"error": "Upload successful"}), 200

        return jsonify({"error": "Upload Unsuccessful"}), 400

    def getUserSnippets(self):
        
            print("User.Inside getUserSnippets()")
            # cursor = snippet_collection.find( { "Keywords": keyword} )
            cursor = snippet_collection.find( { "Submitted_by": ""+ session['user']['username'] +"" } )
            # cursor = snippet_collection.find({'Keywords':{'$regex':'keyword'}})
            # cursor = snippet_collection.find( { "Keywords": {regex : "son"}} )
            deets = {}
            results = []
            for doc in cursor:
                # print(doc)
                # print(doc,end="\n\n")
                deets['name'] = doc['Name']
                deets['description'] = doc['Description']
                deets['code'] = doc['Code']
                deets['rating'] = int(doc['Rating'])
                deets['sub'] = doc['Submitted_by']
                deets['update'] = doc['Upload_date']
                results.append(deets.copy())
                deets.clear()
            # retlist = []
            # retlist.append(keyword)
            # retlist.append(results)
            # for i in results:
            #     print(i,end="\n\n")
            # if snippetDetails:
            #     print snippetDetails
            # return jsonify({'success': "Details fetched succesfully"}), 200
            # return jsonify(results), 200
            return results
    
    def getUserSnippetCount(self):

        print("User.Inside getUserSnippetCount()")
        # cursor = snippet_collection.find( { "Submitted_by": ""+ session['user']['username'] +"" } ).count()
            
        return len(list(snippet_collection.find( { "Submitted_by": ""+ session['user']['username'] +"" } )));

    def searchSnippet(self, key):

        print("User.Inside seachSnippet()")
        global request_keyword
        if(key != ""):
            request_keyword = key
        # keyword = request.form.get('search')
        request_keyword = request_keyword.lower()
        # cursor = snippet_collection.find( { "Keywords": keyword} )
        cursor = snippet_collection.find( { "Keywords": {'$regex':request_keyword}} )
        # cursor = snippet_collection.find({'Keywords':{'$regex':'keyword'}})
        # cursor = snippet_collection.find( { "Keywords": {regex : "son"}} )
        deets = {}
        results = []
        for doc in cursor:
            print(doc)
            # print(doc,end="\n\n")
            deets['id'] = json_util.dumps(doc['_id'])
            deets['name'] = doc['Name']
            deets['description'] = doc['Description']
            deets['code'] = doc['Code']
            deets['rating'] = int(doc['Rating'])
            deets['sub'] = doc['Submitted_by']
            deets['update'] = doc['Upload_date']
            vt = int(doc['NumOfVotes'])
            if vt != 0:
                deets['rating'] = round(float((deets['rating']/vt)*10),2)
            results.append(deets.copy())
            deets.clear()
        retlist = []
        newlist = []
        newlist = sorted(results, key=itemgetter('rating'), reverse=True) #sorting based on rating

        retlist.append(request_keyword)
        retlist.append(newlist)
        return retlist
    
    def searchall(self):

        print("User.Inside seachSnippet()")
        global searchkey
        keyword = searchkey
        # cursor = snippet_collection.find( { "Keywords": keyword} )
        cursor = snippet_collection.find( { "Keywords": {'$regex':keyword}} )
        # cursor = snippet_collection.find({'Keywords':{'$regex':'keyword'}})
        # cursor = snippet_collection.find( { "Keywords": {regex : "son"}} )
        deets = {}
        results = []
        for doc in cursor:
            # print(doc)
            # print(doc,end="\n\n")
            deets['name'] = doc['Name']
            deets['description'] = doc['Description']
            deets['code'] = doc['Code']
            deets['rating'] = int(doc['Rating'])
            deets['sub'] = doc['Submitted_by']
            deets['update'] = doc['Upload_date']
            results.append(deets.copy())
            deets.clear()
        retlist = []
        newlist = sorted(results, key=itemgetter('rating'), reverse=True) #sorting based on rating
        retlist.append(keyword)
        retlist.append(newlist)
        # retlist.append(results)
        return retlist
    
    def freq_search(self):
        print("entered models")
        cursor = snippet_collection.find().limit(50)
        deets = {}
        results = []
        for doc in cursor:
            deets['name'] = doc['Name']
            deets['description'] = doc['Description']
            deets['code'] = doc['Code']
            deets['rating'] = int(doc['Rating'])
            deets['sub'] = doc['Submitted_by']
            deets['update'] = doc['Upload_date']
            results.append(deets.copy())
            deets.clear()
        newlist = sorted(results, key=itemgetter('rating'), reverse=True) #sorting based on rating
        return newlist
    
    def ratingplus(self,it):
        sval = str(it)
        # obj = ObjectId(sval)
        cursor = snippet_collection.find_one(ObjectId(sval))
        print(cursor['Rating'])
        rating = float(cursor['Rating'])
        votes = int(cursor['NumOfVotes'])
        # for doc in cursor:
            # rating = float(doc['Rating'])
            # votes = int(doc['NumOfVotes'])
        print("yoyo")
        print(len(list(snippet_collection.find_one(ObjectId(sval)))))
        votes = votes+1
        rating = rating+1
        snippet_collection.update_one({"_id": ObjectId(sval)}, {'$set':{'Rating':rating}})
        snippet_collection.update_one({"_id": ObjectId(sval)}, {'$set':{'NumOfVotes':votes}})
        return
    
    def ratingminus(self,it):
        sval = str(it)
        # obj = ObjectId(sval)
        cursor = snippet_collection.find_one(ObjectId(sval))
        print(cursor['Rating'])
        rating = float(cursor['Rating'])
        votes = int(cursor['NumOfVotes'])
        # for doc in cursor:
            # rating = float(doc['Rating'])
            # votes = int(doc['NumOfVotes'])
        print("yoyo")
        print(len(list(snippet_collection.find_one(ObjectId(sval)))))
        votes = votes+1
        snippet_collection.update_one({"_id": ObjectId(sval)}, {'$set':{'Rating':rating}})
        snippet_collection.update_one({"_id": ObjectId(sval)}, {'$set':{'NumOfVotes':votes}})
        return
        
