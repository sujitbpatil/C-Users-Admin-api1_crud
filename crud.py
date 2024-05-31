from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:W0rld(up@127.0.0.1/db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)
    status= db.Column(db.String(80))
    created_by=db.Column(db.String(80))

    def __init__(self, title, description, status,created_by):
        self.title = title
        self.description = description
        self.status = status
        self.created_by=created_by


class TODOSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'description', 'status','created_by')


todo_schema = TODOSchema()
todos_schema = TODOSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    title = request.json['title']
    description = request.json['description']
    status = request.json['status']
    created_by= request.json['created_by']
    
    new_user = TODO(title, description, status,created_by)

    db.session.add(new_user)
    db.session.commit()

    return todo_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = TODO.query.all()
    result = todos_schema.dump(all_users)
    return jsonify(result)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = TODO.query.get(id)
    return todo_schema.dump(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = TODO.query.get(id)
    title = request.json['title']
    description = request.json['description']
    status = request.json['status']
    created_by= request.json['created_by']

    user.description = description
    user.title = title
    user.status = status
    user.created_by=created_by

    db.session.commit()
    return todo_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = TODO.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return todo_schema.jsonify(user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)