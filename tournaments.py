import random
import math

def calculate_swiss_rounds(num_players):
    # Рассчитываем количество туров
    rounds = math.ceil(math.log2(num_players))+math.ceil(math.log2(3))
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

    # Если остался один игрок, он получает 1 очко
    if players:
        players[0]['points'] += 1

    return pairs

def swiss_system_draw(players):
    # Сортируем игроков по количеству очков
    players.sort(key=lambda x: x['points'], reverse=True)

    # Разделяем игроков на пары
    pairs = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairs.append((player1, player2))

    # Если остался один игрок, он получает 1 очко
    if players:
        players[0]['points'] += 1

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

    for i in range(n):
        round_pairs = []
        for j in range(n // 2):
            round_pairs.append((players[j], players[n - 1 - j]))
        pairs.append(round_pairs)
        # Ротация игроков для следующего раунда
        players = [players[0]] + [players[n - 1]] + players[1:n - 1]

    return pairs

def update_points(pairs, players):
    for pair in pairs:
        player1, player2 = pair
        result = input(f"Введите результат матча между {player1['name']} и {player2['name']} (1 - победа первого, 2 - победа второго, 0 - ничья): ")
        if result == '1':
            player1['points'] += 1
        elif result == '2':
            player2['points'] += 1
        elif result == '0':
            player1['points'] += 0.5
            player2['points'] += 0.5
        else:
            print("Неверный ввод. Пожалуйста, введите 1, 2 или 0.")
            return False
    return True

def print_results(players):
    # Сортируем игроков по количеству очков
    players.sort(key=lambda x: x['points'], reverse=True)

    # Выводим итоговые результаты
    print("\nИтоговые результаты:")
    print("{:<10} {:<10}".format('Имя', 'Очки'))
    print('-' * 20)
    for player in players:
        print("{:<10} {:<10}".format(player['name'], player['points']))

# Ввод произвольного числа игроков с консоли
num_players = int(input("Введите количество игроков: "))
players = []

# Ввод имён игроков с консоли
for i in range(num_players):
    name = input(f"Введите имя игрока {i+1}: ")
    players.append({'name': name, 'points': 0, 'had_bye': False})

# Расчёт числа туров
rounds = calculate_swiss_rounds(num_players)
print(f"Количество туров для {num_players} участников: {rounds}")

# Жеребьёвка первого раунда швейцарской системы
first_round_pairs = swiss_system_first_round_draw(players.copy())
print("Swiss System First Round Pairs:", first_round_pairs)

# Ввод результатов первого раунда
if not update_points(first_round_pairs, players):
    print("Ошибка при вводе результатов. Программа завершена.")
    exit()

# Жеребьёвка последующих раундов
for round_num in range(1, rounds):
    # Найти игрока с наименьшим количеством очков, который еще не имел бай
    bye_player = min((player for player in players if not player['had_bye']), key=lambda x: x['points'], default=None)

    if bye_player:
        bye_player['points'] += 1
        bye_player['had_bye'] = True
        players = [player for player in players if player != bye_player]

    pairs = swiss_system_draw(players.copy())
    print(f"Swiss System Round {round_num + 1} Pairs:", pairs)

    # Ввод результатов текущего раунда
    if not update_points(pairs, players):
        print("Ошибка при вводе результатов. Программа завершена.")
        exit()

# Вывод итоговых результатов
print_results(players)

# Нокаут-система
knockout_pairs = knockout_system_draw(players.copy())
print("Knockout System Pairs:", knockout_pairs)

# Круговая система
round_robin_pairs = round_robin_draw(players.copy())
print("Round Robin System Pairs:", round_robin_pairs)