from flask import Flask, abort, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# -- will move models to seperate file --
# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    groups = db.Column(db.String(50)) # assume groups are single words without spaces

    def __init__(self, userid, first_name, last_name, groups):
        self.userid = userid
        self.first_name = first_name
    	self.last_name = last_name
    	self.groups = groups

    # hack to return self atttributes as elements in dict
    def as_dict(self):
        return{c.name: getattr(self,c.name)for c in self.__table__.columns}

class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    group_name = db.Column(db.String(20))

    def __init__(self, group_name):
        self.group_name = group_name

db.create_all()
# -------- USERS 

@app.route('/users/', methods = ['GET'])
def index():
    user = User.query.all()
    users = []
    if(user is not None):
        for d in range(len(user)):
            users.append(user[d].as_dict())
        return jsonify({'users': users})
    else:
        return jsonify({'users':'none'})

@app.route('/users/', methods = ['POST'])
def create_user():
    # userid should be mandatory for user creation
    if not request.json or not 'userid' in request.json:
        abort(400)
    user = User(request.json['userid'],request.json.get('first_name',''),request.json.get('last_name',''), request.json.get('groups',''))
    db.session.add(user)
    db.session.commit()
    return jsonify({'user':user.as_dict()})

@app.route('/users/<userid>', methods = ['DELETE'])
def delete_user(userid):
    db.session.delete(User.query.filter_by(userid = userid).first()) # userid should be unique
    db.session.commit()
    return jsonify({'result': True})

@app.route('/users/<userid>', methods = ['PUT'])
def update_user(userid):
    return 0

# -------- GROUPS (ignore for now)

if __name__ == '__main__':
    app.debug = True
    app.run()
