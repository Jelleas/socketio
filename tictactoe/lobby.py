"""
A game is a dictionary with the following structure:
{
    board: [['X', '', ''], ['', 'O', ''], ['X', '', '']]
    players: [player_foo, player_bar]
    turn: player_foo
}
"""
GAMES = []


def get_game(player_id):
    """Find the game in which player_id is playing."""
    for game in GAMES:
        if player_id in game["players"]:
            return game

    return None


def join_game(player_id):
    """
    If there is a game without a second player, have player_id join it.
    Otherwise, create a new game for player_id.
    """
    # If player_id is already in a game, return that game
    game = get_game(player_id)
    if game != None:
        return game

    # Find a game with only one player, and join it
    for game in GAMES:
        if len(game["players"]) < 2:
            game["players"].append(player_id)
            return game

    # Otherwise start a new game
    game = {}

    # Create an empty board
    game["board"] = [["", "", ""] for i in range(3)]

    # Add current player as player1
    game["players"] = [player_id]

    # Player1 gets to start
    game["turn"] = player_id

    # Add the new game to GAMES
    GAMES.append(game)

    return game


def remove_game(player_id):
    """Remove the game player_id is playing in."""
    for i in range(len(GAMES)):
        if player_id in GAMES[i]["players"]:
            del GAMES[i]
            return
