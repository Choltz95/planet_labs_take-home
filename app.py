from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# -- will move models to seperate file --
# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    userid = db.Column(db.String(20))
    groups = db.Column(db.String(50)) # assume groups are single words without spaces

    def __init__(self, first_name, last_name, userid, groups):
        self.first_name = first_name
    	self.last_name = last_name
    	self.userid = userid
    	self.groups = groups

class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    group_name - db.Column(db.String(20))

    def __init__(self, group_name):
        self.group_name = group_name

# -------- USERS

@app.route('/users/', methods = ['GET'])
def index():
    return 0

@app.route('/users/', methods = ['POST'])
def create_user():
    return 0

@app.route('/users/<userid>', methods = ['DELETE'])
def delete_user(id):
    return 0
    
@app.route('/users/<userid>', methods = ['PUT'])
def update_user(id):
    return 0

# -------- GROUPS

if __name__ == '__main__':
    app.debug = True
    app.run()
