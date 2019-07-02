from flask import Flask, render_template, request
from flask_socketio import SocketIO
import lobby

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["DEBUG"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app, ping_interval=4, ping_timeout=10)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("join_game")
def join_game():
    """Have the player join a game."""

    # Get the player id
    player_id = request.sid

    # Join a new game
    game = lobby.join_game(request.sid)

    # Let each player know which game she is in
    for player in game["players"]:
        socketio.emit("joined_game",
                     {
                          "board": game["board"],
                          "is_waiting": len(game["players"]) < 2,
                     },
                     room=player)


@socketio.on("disconnect")
def disconnect():
    """In case a player disconnected, let the other player know and remove game"""

    # Get the player id
    player_id = request.sid

    # Get the current game
    game = lobby.get_game(player_id)

    # If no game is being played, nothing to do
    if game == None:
        return

    # Otherwise, find the other player
    if game["players"][0] != player_id:
        other_player_id = game["players"][0]
    else:
        other_player_id = game["players"][1]

    # Let her know her opponent has disconnected
    socketio.emit("disconnected", room=other_player_id)

    # Remove the game from the server
    lobby.remove_game(player_id)


@socketio.on("place_tile")
def place(data):
    """Place a tile on the board."""

    # Get the player id
    player_id = request.sid

    # Get the current game & board
    game = lobby.get_game(player_id)
    board = game["board"]

    x = data["x"]
    y = data["y"]

    # TODO
    # add a tile on the board
    # emit the board through the socket

    for player in game["players"]:
        socketio.emit("placed_tile",
                      {
                        "x": x,
                        "y": y
                      },
                      room=player)
