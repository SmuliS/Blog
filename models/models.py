from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=False)
    pw = db.Column(db.String(30), unique=False)

    def __init_(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Post:
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(30), unique=False)
    text = bd.Column(bd.Text(260), unique=True)

    def __init__(self, topic, text):
        self.topic = topic
        self.text = text

    def __repr__(self):
        return '<Post %r>' % self.topic
