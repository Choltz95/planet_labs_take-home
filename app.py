from flask import Flask, abort, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
import sys

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# -- will move models to seperate file --
# relationship table
group_table = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    groups = db.relationship('Group', secondary=group_table, backref='users' )

    def __init__(self, userid, first_name, last_name):
        self.userid = userid
        self.first_name = first_name
    	self.last_name = last_name

    # hack to return self atttributes as elements in dict
    def as_dict(self):
        return{c.name: getattr(self,c.name)for c in self.__table__.columns}

#group model
class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    group_name = db.Column(db.String(20))

    def __init__(self, group_name):
        self.group_name = group_name

    def as_dict(self):
        return{c.name: getattr(self,c.name)for c in self.__table__.columns}

db.create_all()


# -------- USERS 
@app.route('/users/<userid>', methods = ['GET'])
def get_user(userid):
    user = User.query.filter_by(userid=userid).first()
    if (user is None):
        abort(404)

    il_groups = user.groups # instrumented list of group objects
    groups = []
    for g in il_groups:
        groups.append(g.group_name)
    
    u_dict = jsonify(user.as_dict(), groups = groups)
    return u_dict

'''
POST /users
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
'''
@app.route('/users/', methods = ['POST'])
def create_user():
    # userid should be mandatory for user creation
    if not request.json or not 'userid' in request.json:
        abort(400)
    if User.query.filter_by(userid=request.json['userid']).first() is not None:
        abort(409) # user already exists
    user = User(request.json['userid'],request.json.get('first_name',''),request.json.get('last_name',''))

    db.session.add(user)

    group_names = request.json.get('groups','')
    # update association table
    for g in group_names:
        g = Group.query.filter_by(group_name = g).first()
        user.groups.append(g)

    db.session.commit()

    il_groups = user.groups # instrumented list of group objects
    groups = []
    for g in il_groups:
        groups.append(g.group_name)
    
    u_dict = jsonify(user.as_dict(), groups = groups)
    return u_dict

'''
PUT /users/<userid>
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
'''
@app.route('/users/<userid>', methods = ['PUT'])
def update_user(userid):
    user = User.query.filter_by(userid = userid).first()
    if (user is None):
        abort(404) # user does not exist
    user.userid = request.json.get('userid', user.userid)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)

    db.session.commit()
    il_groups = user.groups # instrumented list of group objects
    groups = []
    for g in il_groups:
        groups.append(g.group_name)
    
    u_dict = jsonify(user.as_dict(), groups = groups)
    return jsonify(user.as_dict(), groups=groups)

'''
DELETE /users/<userid>
    Deletes a user record. Returns 404 if the user doesn't exist.
'''
@app.route('/users/<userid>', methods = ['DELETE'])
def delete_user(userid):
    user = User.query.filter_by(userid = userid).first()
    if (user is None):
        abort(404) # user does not exist
    db.session.delete(user) # userid should be unique
    db.session.commit()
    return jsonify({'result': True})


# -------- GROUPS
'''
GET /groups/<group name>
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist.
'''
@app.route('/groups/<group_name>', methods = ['GET'])
def get_groups(group_name):
    group = Group.query.filter_by(group_name=group_name).first()
    if (group is None):
        abort(404)
    il_users = group.users # instrumented list of user objects
    users = []
    for u in il_users:
        users.append(u.userid)
    
    g_dict = jsonify(users=users)
    return g_dict

'''
POST /groups
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a `name` parameter
'''
@app.route('/groups/', methods = ['POST'])
def create_group():
    if not request.json or not 'name' in request.json:
        abort(400)
    if Group.query.filter_by(group_name=request.json['name']).first() is not None:
        abort(409) # group already exists
    group = Group(request.json['name'])
    db.session.add(group)
    db.session.commit()
    return jsonify(group.as_dict())

'''
PUT /groups/<group name>
    Updates the membership list for the group. The body of the request should 
    be a JSON list describing the group's members.
'''
@app.route('/groups/<group_name>', methods = ['PUT'])
def update_group(group_name):
    if Group.query.filter_by(group_name=group_name).first() is None:
        abort(404) # group does not exist
    uids = request.json['uids']

    # update association table
    group = Group.query.filter_by(group_name=group_name).first()
    for uid in uids:
        user = User.query.filter_by(userid = uid).first()
        group.users.append(user)

    db.session.commit()

    il_users = group.users # instrumented list of user objects
    users = []
    for u in il_users:
        users.append(u.userid)
    
    g_dict = jsonify(group.as_dict(), users=users)
    return g_dict

'''
DELETE /groups/<group name>
    Deletes a group.
'''
@app.route('/groups/<group_name>', methods = ['DELETE'])
def delete_group(group_name):
    group = Group.query.filter_by(group_name = group_name).first()
    if (group is None):
        abort(404) # group does not exist
    db.session.delete(group) # group_name should be unique
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        if(sys.argv[1] == "-d"):   app.debug = True # debug
    app.run()