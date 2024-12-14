import random
import math
from prettytable import PrettyTable

def calculate_swiss_rounds(num_players):
    # Рассчитываем количество туров
    if (num_players>6) :
        rounds = math.ceil(math.log2(num_players)) + math.ceil(math.log2(3))
    if (num_players==3) :
        rounds = 2
    if (num_players==4) :
        rounds = 3
    if (num_players==5) :
        rounds = 4
    if (num_players==6) :
        rounds = 4

    return rounds

def swiss_system_first_round_draw(players):
    # Перемешиваем игроков случайным образом
    random.shuffle(players)

    # Разделяем игроков на пары
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))
        player1['opponents'].append(player2['name'])
        player2['opponents'].append(player1['name'])

    # Если остался один игрок, он получает 1 очко
    if players:
        players[0]['points'] += 1
        players[0][f'round_{1}'] = 'bye'
        players[0]['had_bye'] = True
    return pairs

def swiss_system_draw(players, round_num):
    # Сортируем игроков по количеству очков, Бухгольцу и Бергеру
    players.sort(key=lambda x: (x['points'], x['buchholz'], x['berger']), reverse=True)

    # Разделяем игроков на пары
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

    # Если остался один игрок, он получает 1 очко
    if players:
        players[0]['points'] += 1
        players[0][f'round_{round_num}'] = 'bye'
    return pairs

def knockout_system_draw(players):
    # Перемешиваем игроков случайным образом
    random.shuffle(players)

    # Разделяем игроков на пары
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))

    return pairs

def round_robin_draw(players):
    # Создаем пары для круговой системы
    pairs = []
    n = len(players)

    if n % 2 != 0:
        players.append({'name': 'Bye'})  # Добавляем "пустого" игрока, если нечетное количество игроков

    for i in range(n - 1):
        round_pairs = []
        for j in range(n // 2):
            round_pairs.append((players[j], players[n - 1 - j]))
        pairs.append(round_pairs)
        # Ротация игроков для следующего раунда
        players = [players[0]] + [players[n - 1]] + players[1:n - 1]

    return pairs

def update_points(pairs, players, round_num):
    for pair in pairs:
        player1, player2 = pair
        result = input(f"Введите результат матча между {player1['name']} и {player2['name']} (1 - победа первого, 2 - победа второго, 0 - ничья): ")
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
    for player in players:
        player['buchholz'] = sum(opponent['points'] for opponent in players if opponent['name'] in player['opponents'])
        player['berger'] = sum(opponent['points'] for opponent in players if opponent['name'] in player['opponents'] and opponent['points'] > 0)

def print_results(players, tournament_type, rounds):
    # Создаем таблицу
    table = PrettyTable()
    table.field_names = ["№", "Участники"] + [f"{r}" for r in range(1, rounds + 1)] + ["+", "-", "=", "Очки", "Доп1", "Доп2", "Место"]

    # Сортируем игроков по количеству очков, Бухгольцу и Бергеру
    if tournament_type == "swiss":
        players.sort(key=lambda x: (x['points'], x['buchholz'], x['berger']), reverse=True)
    elif tournament_type == "round_robin":
        players.sort(key=lambda x: (x['points'], x['wins'], x['berger']), reverse=True)
    else:
        players.sort(key=lambda x: (x['points'],), reverse=True)

    # Заполняем таблицу данными
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
    # Создаем таблицу
    table = PrettyTable()
    table.field_names = ["Пара", "Игрок 1", "Очки 1", "Игрок 2", "Очки 2"]

    # Заполняем таблицу данными
    for idx, pair in enumerate(pairs, start=1):
        player1, player2 = pair
        table.add_row([idx, player1['name'], player1['points'], player2['name'], player2['points']])

    print(f"Жеребьёвка раунда {round_num}:")
    print(table)

def reset_additional_metrics(players, rounds):
    for player in players:
        player['buchholz'] = 0
        player['berger'] = 0
        player['wins'] = 0
        player['losses'] = 0
        player['opponents'] = []
        for r in range(1, rounds + 1):
            player[f'round_{r}'] = ""

# Ввод произвольного числа игроков с консоли
num_players = int(input("Введите количество игроков: "))
players = []

# Ввод имён игроков с консоли
for i in range(num_players):
    name = input(f"Введите имя игрока {i+1}: ")
    player_data = {'name': name, 'points': 0, 'buchholz': 0, 'berger': 0, 'wins': 0, 'losses': 0, 'had_bye': False, 'opponents': []}
    for r in range(1, num_players):
        player_data[f'round_{r}'] = ""
    players.append(player_data)

# Выбор вида турнира
tournament_type = input("Выберите вид турнира (swiss/round_robin/knockout): ").strip().lower()

if tournament_type == "swiss":
    # Расчёт числа туров
    rounds = calculate_swiss_rounds(num_players)
    print(f"Количество туров для {num_players} участников: {rounds}")

    # Жеребьёвка первого раунда швейцарской системы
    first_round_pairs = swiss_system_first_round_draw(players.copy())
    print_round_pairs(first_round_pairs, 1)

    # Ввод результатов первого раунда
    if not update_points(first_round_pairs, players, 1):
        print("Ошибка при вводе результатов. Программа завершена.")
        exit()

    # Пересчет коэффициентов Бухгольца и Бергера после первого раунда
    calculate_buchholz_and_berger(players)

    # Жеребьёвка последующих раундов
    for round_num in range(2, rounds + 1):
        # Найти игрока с наименьшим количеством очков, который еще не имел бай
        bye_player = min((player for player in players if not player['had_bye']), key=lambda x: x['points'], default=None)

        if bye_player:
            bye_player['points'] += 1
            bye_player['had_bye'] = True

        pairs = swiss_system_draw(players.copy(),round_num)
        print_round_pairs(pairs, round_num)

        # Ввод результатов текущего раунда
        if not update_points(pairs, players, round_num):
            print("Ошибка при вводе результатов. Программа завершена.")
            exit()

        # Пересчет коэффициентов Бухгольца и Бергера после каждого раунда
        calculate_buchholz_and_berger(players)

    # Вывод итоговых результатов швейцарской системы
    print_results(players, "swiss", rounds)

elif tournament_type == "round_robin":
    # Круговая система
    round_robin_pairs = round_robin_draw(players.copy())
    print("Round Robin System Pairs:", round_robin_pairs)

    # Ввод результатов каждого тура круговой системы
    for round_num, round_pairs in enumerate(round_robin_pairs, start=1):
        print_round_pairs(round_pairs, round_num)
        if not update_points(round_pairs, players, round_num):
            print("Ошибка при вводе результатов. Программа завершена.")
            exit()

        # Пересчет коэффициентов Бергера после каждого тура
        calculate_buchholz_and_berger(players)

    # Вывод итоговых результатов круговой системы
    print_results(players, "round_robin", len(round_robin_pairs))

elif tournament_type == "knockout":
    # Нокаут-система
    knockout_pairs = knockout_system_draw(players.copy())
    print("Knockout System Pairs:", knockout_pairs)

    # Ввод результатов каждого тура нокаут-системы
    round_num = 1
    while len(knockout_pairs) > 0:
        print_round_pairs(knockout_pairs, round_num)
        for pair in knockout_pairs:
            player1, player2 = pair
            result = input(f"Введите результат матча между {player1['name']} и {player2['name']} (1 - победа первого, 2 - победа второго): ")
            if result == '1':
                player1['points'] += 1
                player2['losses'] += 1
                player1[f'round_{round_num}'] = '1'
                player2[f'round_{round_num}'] = '0'
            elif result == '2':
                player2['points'] += 1
                player1['losses'] += 1
                player1[f'round_{round_num}'] = '0'
                player2[f'round_{round_num}'] = '1'
            else:
                print("Неверный ввод. Пожалуйста, введите 1 или 2.")
                exit()

        # Фильтруем победителей для следующего раунда
        winners = [player for pair in knockout_pairs for player in pair if player['points'] > 0]
        knockout_pairs = knockout_system_draw(winners)
        round_num += 1

    # Вывод итоговых результатов нокаут-системы
    print_results(players, "knockout", round_num - 1)

else:
    print("Неверный выбор турнира. Программа завершена.")
    exit()