tournaments = {}

def create_tournament(tournament_id):
    tournaments[tournament_id] = []

def add_game_to_tournament(tournament_id, game_id):
    if tournament_id in tournaments:
        tournaments[tournament_id].append(game_id)

