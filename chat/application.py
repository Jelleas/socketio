import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

votes = {"yes": 0, "no": 0, "maybe": 0}
messages = []


@app.route("/")
def index():
    return render_template("index.html", votes=votes, messages=messages)


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)
    

# TODO
# Using @socketio.on, listen for an event to receive a message from the user
# Append the message to the messages list and emit an event to display the message list
