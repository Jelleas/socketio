"""
A game is a dictionary with the following structure:
{
    board: [['X', '', ''], ['', 'O', ''], ['X', '', '']]
    player1: player_foo
    player2: player_bar
    turn: player_foo
}
"""
GAMES = []


def get_game(player_id):
    """Find the game in which player_id is playing."""
    for game in GAMES:
        if game["player1"] == player_id or game["player2"] == player_id:
            return game

    return None


def join_game(player_id):
    """
    If there is a game without a second player, have player_id join it.
    Otherwise, create a new game for player_id.
    """

    # Find a game with only one player, and join it
    for game in GAMES:
        if game["player2"] == None:
            game["player2"] = player_id
            return game

    # Otherwise start a new game
    game = {}

    # Create an empty board
    game["board"] = [["", "", ""] for i in range(3)]

    # Add current player as player1
    game["player1"] = player_id

    # Keep the second spot open
    game["player2"] = None

    # Player1 gets to start
    game["turn"] = player_id

    # Add the new game to GAMES
    GAMES.append(game)

    return game


def remove_game(player_id):
    """Remove the game player_id is playing in."""
    for i in range(len(GAMES)):
        if game["player1"] == player_id or game["player2"] == player_id:
            del GAMES[i]
            return
