import random
import math
from prettytable import PrettyTable

def calculate_swiss_rounds(number_players):
    """Рассчитывает количество туров для швейцарской системы."""
    if not isinstance(number_players, int):
        raise ValueError("Неправильный формат ввода")
    if number_players < 2:
        raise ValueError("В турнире не может быть менее 2 участников")

    if number_players > 6:
        rounds = math.ceil(math.log2(number_players)) + math.ceil(math.log2(3))
    elif number_players == 2:
        rounds = 1
    elif number_players == 3:
        rounds = 3
    elif number_players == 4:
        rounds = 3
    elif number_players == 5:
        rounds = 4
    elif number_players == 6:
        rounds = 4

    return rounds

def swiss_system_first_round_draw(players):
    """Проводит жеребьевку первого раунда для швейцарской системы."""
    random.shuffle(players)

    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))
        player1['opponents'].append(player2['name'])
        player2['opponents'].append(player1['name'])

    if players:
        players[0]['points'] += 1
        players[0][f'round_{1}'] = 'bye'
        players[0]['had_bye'] = True

    return pairs

def swiss_system_draw(players, round_num):
    """Проводит жеребьевку для швейцарской системы."""
    players.sort(
        key=lambda x: (x['points'], x['buchholz'], x['berger']),
        reverse=True
    )

    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        for i, player2 in enumerate(players):
            if player2['name'] not in player1['opponents']:
                pairs.append((player1, player2))
                player1['opponents'].append(player2['name'])
                player2['opponents'].append(player1['name'])
                players.pop(i)
                break

    if players:
        players[0]['points'] += 1
        players[0][f'round_{round_num}'] = 'bye'

    return pairs

def knockout_system_draw(players):
    """Проводит жеребьевку для системы на вылет."""
    random.shuffle(players)

    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))

    return pairs

def round_robin_draw(players):
    """Проводит жеребьевку для круговой системы."""
    pairs = []
    n = len(players)

    if n % 2 != 0:
        players.append({'name': 'Bye'})

    for i in range(n - 1):
        round_pairs = []
        for j in range(n // 2):
            round_pairs.append((players[j], players[n - 1 - j]))
        pairs.append(round_pairs)
        players = [players[0]] + [players[n - 1]] + players[1:n - 1]

    return pairs

def update_points(pairs, players, round_num):
    """Обновляет очки игроков после раунда."""
    for pair in pairs:
        player1, player2 = pair
        result = input(
            f"Введите результат матча между {player1['name']} \
            и {player2['name']} (1 - победа первого,\
            2 - победа второго, 0 - ничья): "
            )
        if result == '1':
            player1['points'] += 1
            player1['wins'] += 1
            player2['losses'] += 1
            player1[f'round_{round_num}'] = '1'
            player2[f'round_{round_num}'] = '0'
        elif result == '2':
            player2['points'] += 1
            player2['wins'] += 1
            player1['losses'] += 1
            player1[f'round_{round_num}'] = '0'
            player2[f'round_{round_num}'] = '1'
        elif result == '0':
            player1['points'] += 0.5
            player2['points'] += 0.5
            player1[f'round_{round_num}'] = '½'
            player2[f'round_{round_num}'] = '½'
        else:
            print("Неверный ввод. Пожалуйста, введите 1, 2 или 0.")
            return False
    return True

def calculate_buchholz_and_berger(players):
    """Рассчитывает дополнительные метрики Бухгольца и Бергера."""
    for player in players:
        player['buchholz'] = sum(
            opponent['points'] for opponent in players if opponent[
            'name'] in player['opponents'])
        player['berger'] = sum(
            opponent['points'] for opponent in players if opponent[
            'name'] in player['opponents'] and opponent['points'] > 0)

def print_results(players, tournament_type, rounds):
    """Печатает результаты турнира."""
    table = PrettyTable()
    table.field_names = ["№", "Участники"] + [
    f"{r}" for r in range(1, rounds + 1)] + [
    "+", "-", "=", "Очки", "Доп1", "Доп2", "Место"]

    if tournament_type == "swiss":
        players.sort(key=lambda x: 
            (x['points'], x['buchholz'], x['berger']), reverse=True)
    elif tournament_type == "round_robin":
        players.sort(key=lambda x: 
            (x['points'], x['wins'], x['berger']), reverse=True)
    else:
        players.sort(key=lambda x: 
            (x['points'],), reverse=True)

    for idx, player in enumerate(players, start=1):
        row = [idx, player['name']]
        for r in range(1, rounds + 1):
            row.append(player[f'round_{r}'])
        row.append(player['wins'])
        row.append(player['losses'])
        row.append(player['points'] - player['wins'])
        row.append(player['points'])
        if tournament_type == "swiss":
            row.append(player['buchholz'])
            row.append(player['berger'])
        elif tournament_type == "round_robin":
            row.append(player['wins'])
            row.append(player['berger'])
        row.append(idx)
        table.add_row(row)

    print(table)

def print_round_pairs(pairs, round_num):
    """Печатает пары для раунда."""
    table = PrettyTable()
    table.field_names = ["Пара", "Игрок 1", "Очки 1", "Игрок 2", "Очки 2"]

    for idx, pair in enumerate(pairs, start=1):
        player1, player2 = pair
        table.add_row([
            idx, player1['name'],
            player1['points'],
            player2['name'], player2['points']])

    print(f"Жеребьёвка раунда {round_num}:")
    print(table)

def reset_additional_metrics(players, rounds):
    """Сбрасывает дополнительные метрики игроков."""
    for player in players:
        player['buchholz'] = 0
        player['berger'] = 0
        player['wins'] = 0
        player['losses'] = 0
        player['opponents'] = []
        for r in range(1, rounds + 1):
            player[f'round_{r}'] = ""