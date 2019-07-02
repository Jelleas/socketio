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
    # Get the player id
    player_id = request.sid

    # Join a new game
    game = lobby.join_game(request.sid)

    # Let each player know which game she is in
    for player in game.players:
        socketio.emit("joined_game",
                     {
                          "board": game["board"],
                          "is_waiting": game["player1"] == None or game["player2"] == None
                     },
                     room=player)


@socketio.on("disconnect")
def disconnect():
    # Get the player id
    player_id = request.sid

    # Get the current game
    game = lobby.get_game(player_id)

    # If no game is being played, nothing to do
    if game == None:
        return

    # Otherwise, find the other player
    if game.player1 != player_id:
        other_player_id = game.player1
    else:
        other_player_id = game.player2

    # Let her know her opponent has disconnected
    socketio.emit("disconnected", room=other_player_id)

    # Remove the game from the server
    lobby.remove_game(player_id)


@socketio.on("place_tile")
def place(data):
    player_id = request.sid

    game = lobby.get_game(player_id)
    board = game["board"]

    x = data["x"]
    y = data["y"]

    # TODO

    for player in [game["player1"], game["player2"]]:
        socketio.emit("placed_tile",
                      {
                        "x": x,
                        "y": y
                      },
                      room=player)
