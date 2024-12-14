import random
import math
import pytest

def calculate_swiss_rounds(num_players):
    rounds = math.ceil(math.log2(num_players)) + math.ceil(math.log2(3))
    return int(rounds)

def swiss_system_first_round_draw(players):
    random.shuffle(players)
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))
    if players:
        players[0]['points'] += 1
    return pairs

def swiss_system_draw(players):
    players.sort(key=lambda x: x['points'], reverse=True)
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))
    if players:
        players[0]['points'] += 1
    return pairs

def knockout_system_draw(players):
    random.shuffle(players)
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))
    return pairs

def round_robin_draw(players):
    pairs = []
    n = len(players)
    if n % 2 != 0:
        players.append({'name': 'Bye'})
    for i in range(n):
        round_pairs = []
        for j in range(n // 2):
            round_pairs.append((players[j], players[n - 1 - j]))
        pairs.append(round_pairs)
        players = [players[0]] + [players[n - 1]] + players[1:n - 1]
    return pairs

def update_points(pairs, players):
    results = [
        (('Player1', 'Player2'), 1),
        (('Player3', 'Player4'), 2),
        (('Player5', 'Player6'), 0),
        (('Player7', 'Player8'), 1)
    ]
    for (pair, result) in results:
        for p1, p2 in pairs:
            if (p1['name'], p2['name']) == pair:
                if result == 1:
                    p1['points'] += 1
                elif result == 2:
                    p2['points'] += 1
                elif result == 0:
                    p1['points'] += 0.5
                    p2['points'] += 0.5
                break
    return True

def print_results(players):
    players.sort(key=lambda x: x['points'], reverse=True)
    print("\nИтоговые результаты:")
    print("{:<10} {:<10}".format('Имя', 'Очки'))
    print('-' * 20)
    for player in players:
        print("{:<10} {:<10}".format(player['name'], player['points']))

def test_tournament():
    num_players = 8
    players = [{'name': f"Player{i+1}", 'points': 0, 'had_bye': False} for i in range(num_players)]

    rounds = calculate_swiss_rounds(num_players)
    print(f"Количество туров для {num_players} участников: {rounds}")

    first_round_pairs = swiss_system_first_round_draw(players.copy())
    print("Swiss System First Round Pairs:", first_round_pairs)

    for round_num in range(1, rounds):
        bye_player = min((player for player in players if not player['had_bye']), key=lambda x: x['points'], default=None)
        if bye_player:
            bye_player['points'] += 1
            bye_player['had_bye'] = True
            players = [player for player in players if player != bye_player]

        pairs = swiss_system_draw(players.copy())
        print(f"Swiss System Round {round_num + 1} Pairs:", pairs)

    print_results(players)

    knockout_pairs = knockout_system_draw(players.copy())
    print("Knockout System Pairs:", knockout_pairs)

    round_robin_pairs = round_robin_draw(players.copy())
    print("Round Robin System Pairs:", round_robin_pairs)

if __name__ == "__main__":
    pytest.main([__file__])

