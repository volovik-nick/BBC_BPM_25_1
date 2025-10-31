import random
import sys

#---------------Cловари классов, монстров, комнат-------------------------
rooms = ['пусто', 'сундук', 'монстр', 'ключ', 'секретная комната', 'портал', 'комната босса']
room_weights = [0.45, 0.25, 0.20, 0.0, 0.10, 0.0, 0.0]  # Вероятности (0 для уникальных)
# Описание лута из сундука
chest_loot = {
    'артефакты': [
        {'item': 'плащ невидимости (25% шанс уклонения от атаки)', 'rarity': 'редкий', 'weight': 0.4},
        {'item': 'кольцо регенерации (восстанавливает 2 hp за ход)', 'rarity': 'обычный', 'weight': 0.6},
        {'item': 'амулет воскрешения', 'rarity': 'эпический', 'weight': 0.2},
        {'item': 'ключ', 'rarity': 'эпический', 'weight': 0.1}
    ],
    'зелья': [
        {'item': 'зелье защиты (+5 брони на 3 хода)', 'rarity': 'обычный', 'weight': 0.7},
        {'item': 'зелье урона (+50% урона на 2 хода)', 'rarity': 'обычный', 'weight': 0.7},
        {'item': 'зелье исцеления (восстанавливает 25 hp)', 'rarity': 'обычный', 'weight': 0.7},
        {'item': 'зелье скорости (двойная атака в следующий ход)', 'rarity': 'редкий', 'weight': 0.3},
        {'item': 'зелье яда (следующая атака наносит 8 урона за 3 хода)', 'rarity': 'редкий', 'weight': 0.3},
        {'item': 'флакон со святой водой (мгновенно убивает нежить)', 'rarity': 'необычный', 'weight': 0.4},
        {'item': 'зелье ошеломления (враг пропускает 2 хода)', 'rarity': 'эпический', 'weight': 0.2},
        {'item': 'зелье превращения в осла (превращяет в безобидно осла любого монстра, кроме босса)', 'rarity': 'легендарное', 'weight': 0.03}
    ],
    'снаряжение': {
        'рыцарь': [
            'железный топор (18 физического урона)',
            'стальной щит (6 защиты)',
            'кольчуга (8 защиты)'
        ],
        'маг': [
            'магический посох (14 магического урона)',
            'мистическая мантия (6 защиты, +2 к урону заклинаний)',
            'кристалл фокусировки (+10 hp, ускоряет метеоритный дождь)'
        ],
        'лучник': [
            'композитный лук (14 урона)',
            'усиленный шлем (7 защиты)',
            'стрелы x20',
            'бронебойные стрелы x15'
        ]
    }
}
secretroom = ['фонтан исцеления', 'зыбучие пески', 'шипы', 'меч в камне', 'подозрительная лужа', 'казино']
monsters_stats = {
    'вампир': {'hp': 30, 'damage': 16, 'особенность': 'восстанавливает 3 hp при атаке'},
    'карманник': {'hp': 15, 'damage': 14, 'особенность': '10% шанс украсть предмет из инвентаря'},
    'легион скелетов x5': {'hp': 10, 'damage': 12, 'особенность': 'каждый скелет атакует отдельно (общее hp: 60)'},
    'гоблин шаман': {'hp': 25, 'damage': 15, 'особенность': '10% шанс наложить ослабление (урон игрока -2 на 2 хода)'},
    'призрак': {'hp': 20, 'damage': 14, 'особенность': 'ошеломляет игрока на 2 хода'},
    'упырь': {'hp': 30, 'damage': 17, 'особенность': 'наносит дополнительный урон (2) при hp игрока ниже 20'},
    'темный принц': {'hp': 30, 'damage': 19, 'особенность': 'имеет 5 брони'},
    'некромант': {'hp': 25, 'damage': 15, 'особенность': 'раз в 3 хода призывает скелета (hp: 10, damage: 12)'}
}
boss_stats = {
    'орк ~Русланчик~': {
        'hp': 70,
        'damage': 18,
        'armor': 8,
        'особенность': [
            'каждые 2 хода наносит сокрушительный удар (+6 урона, игнорирует 50% брони)',
            'иммунитет к ослаблению и ошеломлению'
        ],
        'особый дроп': {
            'рыцарь': 'рунический двуручный меч (21 физического урона, +5 брони)',
            'маг': 'кристалл мощи (увеличивает урон заклинаний на 50%, метеоритный дождь доступен раз в 2 хода)',
            'лучник': 'арбалет гоблинокрушителя (16 урона, бронебойные стрелы наносят +5 урона против бронированных врагов)'
        }
    },
    'дракон': {
        'hp': 75,
        'damage': 24,
        'armor': 12,
        'особенность': ['огненное дыхание: раз в 3 хода наносит поджигает игрока на 2 хода(огонь наносит 3 урона)'],
        'особый дроп': {
            'рыцарь': 'драконий меч (22 урона, поджигает врага(3 урона каждый ход))',
            'маг': 'обгаревшый мануал (18 магического урона, метеоритный дождь наносит 30 урона и поджигает врагов)',
            'лучник': 'драконий лук (20 урона)'
        }
    }
}
clases = {
    'рыцарь': {
        'стартовые характеристики': {'hp': 60, 'armor': 10, 'damage': 9},
        'стартовый инвентарь': {
            'экипировка': ['старый топор (12 физического урона)','деревяный щит (2 защиты)','кожанный нагрудник (4 защиты)'],
            'зелья': []},
        'особенность класса': ['повышенное здоровье', "пасивные 4 единицы защиты", 'неуезвимость к ошеломлению']
    },
    'маг': {
        'стартовые характеристики': {'hp': 55, 'armor': 3, 'damage': 8},
        'стартовый инвентарь': {
            'экипировка': ['деревянный посох (8 магического урона)', 'потрепанная мантия(3 защиты)'],
            'зелья': ['зелье ослабления']},
        'особенность класса': ['раз в 3 комнты есть возможность призвать метеоритный дождь(16 физического урона против всех противников)']
    },
    'лучник': {
        'стартовые характеристики': {'hp': 48, 'armor': 5, 'damage': 8},
        'стартовый инвентарь': {
            'экипировка': ['деревянный лук', 'кожанный шлем(5 защиты)', f'обычные стелы {20}', f'бронебойные стрелы{10}'],
            'зелья': ['зелье исчезновения']},
        'особенность класса': [f'после убийства монстра есть вероятность выпадения стрел {10} (50%)']
    }
}
#------------Функция перемещения----------------------------
def moving(a):
    global movements
    global player_view
    global game_field
    if a == '1':
        movements.append((movements[-1][0] - 1, movements[-1][1]))
    elif a == '2':
        movements.append((movements[-1][0] + 1, movements[-1][1]))
    elif a == '3':
        movements.append((movements[-1][0], movements[-1][1] + 1))
    elif a == '4':
        movements.append((movements[-1][0], movements[-1][1] - 1))
    player_view[movements[-1][0]][movements[-1][1]] = game_field[movements[-1][0]][movements[-1][1]]

#------------Функция определяющая дроп из сундука----------------------------
def open_chest(player_class):
    combination = random.choices(['1', '2'], weights=[0.65, 0.35], k=1)[0]
    # Получаем снаряжение (всегда одно, для класса игрока)
    result = [random.choice(chest_loot['снаряжение'][player_class])]
    # Получаем зелья и артефакты с учетом выпавшей комбинации
    if combination == '1':
        result.append(random.choices([p['item'] for p in chest_loot['зелья']], weights=[p['weight'] for p in chest_loot['зелья']], k=1))
    else:
        result.append(random.choices([a['item'] for a in chest_loot['артефакты']], weights=[a['weight'] for a in chest_loot['артефакты']], k=1))
    return result

#------------Функция генерируящая 2 матрицы(1 с открытыми полями, лругая с неизвестными)----------------------------
def create_game_matrices(rows, cols):
    # Проверяем, что матрица достаточно велика для входа и 3 уникальных комнат
    if rows * cols < 4:
        raise ValueError("Матрица слишком мала для размещения всех уникальных комнат")
    # Создаём основную матрицу (game_field) с помощью генератора
    game_field = [[None for _ in range(cols)] for _ in range(rows)]
    # Устанавливаем вход в [0][0]
    game_field[0][0] = 'вход'
    # Список уникальных комнат и их позиции
    unique_rooms = ['ключ', 'портал', 'комната босса']
    used_positions = [(0, 0)]  # Вход уже занят
    # Размещаем уникальные комнаты в случайных позициях
    for room in unique_rooms:
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            if (row, col) not in used_positions:  # Проверяем, что позиция свободна
                game_field[row][col] = room
                used_positions.append((row, col))
                break
    # Оставшиеся комнаты (без уникальных)
    available_rooms = ['пусто', 'сундук', 'монстр', 'секретная комната']
    available_weights = [0.35, 0.25, 0.30, 0.10]  # Вероятности для оставшихся комнат
    # Заполняем оставшиеся клетки основной матрицы
    game_field = [
        [
            game_field[i][j] if game_field[i][j] is not None else random.choices(available_rooms, weights=available_weights, k=1)[0] for j in range(cols)
        ]
        for i in range(rows)
    ]
    # Создаём матрицу для игрока (player_view) с знаками вопроса, кроме входа
    player_view = [['?' for _ in range(cols)] for _ in range(rows)]
    player_view[0][0] = 'вход'
    return game_field, player_view

#------------Функция боя с монстром----------------------------
def battle(clas, monster_name):
    """
    Бой с поддержкой способностей классов.
    """
    # --- ИГРОК ---
    player = {
        'hp': clas['стартовые характеристики']['hp'],
        'max_hp': clas['стартовые характеристики']['hp'],
        'damage': clas['стартовые характеристики']['damage'],
        'armor': clas['стартовые характеристики']['armor'],
        'inventory': {
            'экипировка': clas['стартовый инвентарь']['экипировка'].copy(),
            'зелья': clas['стартовый инвентарь']['зелья'].copy()
        },
        'effects': {},
        'stunned': 0,
        'double_attack': False,
        'next_poison': 0,
        'class': list(clases.keys())[list(clases.values()).index(clas)],
        'ability_cooldown': 0,  # перезарядка способности
        'ability_ready': True   # готовность
    }

    # --- МОНСТР ---
    monster_stats = monsters_stats[monster_name].copy()
    monster = {
        'name': monster_name,
        'hp': monster_stats['hp'],
        'max_hp': monster_stats['hp'],
        'damage': monster_stats['damage'],
        'armor': monster_stats.get('armor', 0),
        'feature': monster_stats['особенность'],
        'turn_counter': 0,
        'summons': [],
        'stunned': 0,
        'effects': {}
    }

    # Пассивки класса
    if player['class'] == 'рыцарь':
        player['immune_to_stun'] = True
    else:
        player['immune_to_stun'] = False

    turn = 0
    print(f"\nБОЙ: {player['class'].capitalize()} vs {monster['name'].capitalize()}\n")

    while player['hp'] > 0 and (monster['hp'] > 0 or monster['summons']):
        turn += 1
        print(f"{'─' * 15} ХОД {turn} {'─' * 15}")

        # --- ЭФФЕКТЫ НА ИГРОКЕ ---
        if 'огонь' in player['effects']:
            player['hp'] -= 3
            print("Огонь наносит 3 урона!")
            player['effects']['огонь'] -= 1
            if player['effects']['огонь'] <= 0:
                del player['effects']['огонь']

        if 'регенерация' in player['effects']:
            heal = min(2, player['max_hp'] - player['hp'])
            player['hp'] += heal
            print(f"Регенерация: +{heal} HP")
            player['effects']['регенерация'] -= 1
            if player['effects']['регенерация'] <= 0:
                del player['effects']['регенерация']

        # Уменьшаем эффекты
        for eff in list(player['effects'].keys()):
            if eff not in ['огонь', 'регенерация']:
                player['effects'][eff] -= 1
                if player['effects'][eff] <= 0:
                    print(f"Эффект '{eff}' закончился.")
                    del player['effects'][eff]

        # Уменьшаем перезарядку способности
        if player['ability_cooldown'] > 0:
            player['ability_cooldown'] -= 1
            if player['ability_cooldown'] == 0:
                player['ability_ready'] = True
                print("Способность готова!")

        # --- ХОД ИГРОКА ---
        if player['stunned'] > 0:
            print("Вы ошеломлены и пропускаете ход!")
            player['stunned'] -= 1
        else:
            print(f"Вы: {player['hp']}/{player['max_hp']} HP | Броня: {player['armor']} | Урон: {player['damage']}")
            print(f"{monster['name']}: {monster['hp']}/{monster['max_hp']} HP | Броня: {monster['armor']}")

            # --- ДЕЙСТВИЯ ---
            print("\nДействия:")
            print("1. Атаковать")
            if player['inventory']['зелья']:
                print("2. Использовать зелье")
            else:
                print("2. Использовать зелье (пусто)")

            # Способность мага
            if player['class'] == 'маг' and player['ability_ready']:
                print("3. Метеоритный дождь (16 урона всем врагам)")
            elif player['class'] == 'маг':
                print(f"3. Метеоритный дождь (перезарядка: {player['ability_cooldown']} ходов)")

            while True:
                choice = input("\nВыбор (1/2/3): ").strip()
                if choice == '1':
                    # --- АТАКА ---
                    attacks = 2 if player.get('double_attack', False) else 1
                    player['double_attack'] = False

                    for _ in range(attacks):
                        if monster['hp'] <= 0:
                            break
                        damage = player['damage']
                        if 'урон+50%' in player['effects']:
                            damage = int(damage * 1.5)
                        if 'ослабление' in player['effects']:
                            damage = max(1, damage - 2)

                        actual_dmg = max(0, damage - monster['armor'])
                        monster['hp'] -= actual_dmg
                        print(f"Атака: {actual_dmg} урона!")

                        if player.get('next_poison', 0) > 0:
                            monster['effects']['яд'] = player['next_poison']
                            print(f"{monster['name']} отравлен!")
                            player['next_poison'] = 0
                    break

                elif choice == '2' and player['inventory']['зелья']:
                    print("\nВыберите зелье:")
                    for i, p in enumerate(player['inventory']['зелья'], 1):
                        print(f"{i}. {p}")
                    try:
                        idx = int(input("Номер: ")) - 1
                        if 0 <= idx < len(player['inventory']['зелья']):
                            potion = player['inventory']['зелья'].pop(idx)
                            target = choose_potion_target(potion, player, monster)
                            apply_potion(potion, player, monster, target)
                            break
                    except:
                        print("Введите число!")

                elif choice == '3' and player['class'] == 'маг' and player['ability_ready']:
                    # --- МЕТЕОРИТНЫЙ ДОЖДЬ ---
                    print("МЕТЕОРИТНЫЙ ДОЖДЬ!")
                    meteor_dmg = 16
                    # Урон по основному монстру
                    dmg_to_monster = max(0, meteor_dmg - monster['armor'])
                    monster['hp'] -= dmg_to_monster
                    print(f"{monster['name']} получает {dmg_to_monster} урона!")

                    # Урон по скелетам
                    for sk in monster['summons']:
                        sk_dmg = max(0, meteor_dmg - 0)  # скелеты без брони
                        sk['hp'] -= sk_dmg
                        print(f"Скелет получает {sk_dmg} урона!")

                    # Очистка мёртвых скелетов
                    monster['summons'] = [s for s in monster['summons'] if s['hp'] > 0]

                    player['ability_ready'] = False
                    player['ability_cooldown'] = 3
                    break

                else:
                    print("Неверный выбор!")

        # --- ЭФФЕКТЫ НА МОНСТРЕ ---
        if 'яд' in monster['effects']:
            monster['hp'] -= 8
            print(f"Яд: -8 HP {monster['name']}!")
            monster['effects']['яд'] -= 1
            if monster['effects']['яд'] <= 0:
                del monster['effects']['яд']

        # --- ХОД МОНСТРА ---
        if monster['hp'] > 0 and monster['stunned'] <= 0:
            monster['turn_counter'] += 1

            # Особенности монстров (как раньше)
            if 'восстанавливает 3 hp' in monster['feature'] and 'actual_dmg' in locals() and actual_dmg > 0:
                heal = min(3, monster['max_hp'] - monster['hp'])
                monster['hp'] += heal
                print(f"{monster['name']} восстанавливает {heal} HP!")

            if 'дополнительный урон' in monster['feature'] and player['hp'] < 20:
                monster['damage'] += 2

            if 'наложить ослабление' in monster['feature'] and random.random() < 0.1:
                player['effects']['ослабление'] = player['effects'].get('ослабление', 0) + 2
                print("Вы ослаблены!")

            if 'ошеломляет' in monster['feature'] and not player['immune_to_stun']:
                player['stunned'] = 2
                print("Вы ошеломлены!")

            if 'призывает скелета' in monster['feature'] and monster['turn_counter'] % 3 == 0:
                monster['summons'].append({'hp': 10, 'damage': 12})
                print("Призван скелет!")

            # Атака
            dmg = monster['damage']
            player_dmg = max(0, dmg - player['armor'])
            player['hp'] -= player_dmg
            print(f"{monster['name']} наносит {player_dmg} урона!")

        elif monster['stunned'] > 0:
            print(f"{monster['name']} ошеломлён!")
            monster['stunned'] -= 1

        # Скелеты
        for sk in monster['summons'][:]:
            if sk['hp'] > 0:
                sk_dmg = max(0, sk['damage'] - player['armor'])
                player['hp'] -= sk_dmg
                print(f"Скелет наносит {sk_dmg} урона!")

        print()

    # --- РЕЗУЛЬТАТ ---
    if player['hp'] <= 0:
        print("Вы погибли...")
        return False
    else:
        print(f"Победа над {monster['name']}!")
        if player['class'] == 'лучник' and random.random() < 0.5:
            print("Найдено 10 стрел!")
        return True
#------------------------------------------
def choose_potion_target(potion, player, monster):
    """Определяет, можно ли применить зелье на монстра"""
    offensive_potions = [
        'зелье яда', 'флакон со святой водой', 'зелье ошеломления',
        'зелье превращения в осла'
    ]
    if any(op in potion for op in offensive_potions):
        print(f"Применить '{potion}' на {monster['name']}? (да/нет)")
        while True:
            ans = input().lower()
            if ans in ['да', 'yes', 'д', 'y']:
                return 'monster'
            elif ans in ['нет', 'no', 'н', 'n']:
                return 'player'
            else:
                print("да/нет")
    return 'player'  # по умолчанию — на себя

#------------------------------------------
def apply_potion(potion, player, monster, target):
    if potion == 'зелье исцеления (восстанавливает 25 hp)' and target == 'player':
        heal = min(25, player['max_hp'] - player['hp'])
        player['hp'] += heal
        print(f"Исцеление: +{heal} HP")

    elif potion == 'зелье защиты (+5 брони на 3 хода)' and target == 'player':
        player['armor'] += 5
        player['effects']['защита+5'] = 3
        print("Броня +5 на 3 хода!")

    elif potion == 'зелье урона (+50% урона на 2 хода)' and target == 'player':
        player['effects']['урон+50%'] = 2
        print("Урон +50% на 2 хода!")

    elif potion == 'зелье скорости (двойная атака в следующий ход)' and target == 'player':
        player['double_attack'] = True
        print("Двойная атака в следующий ход!")

    elif potion == 'зелье яда (следующая атака наносит 8 урона за 3 хода)' and target == 'player':
        player['next_poison'] = 3
        print("Следующая атака отравит врага!")

    elif potion == 'флакон со святой водой (мгновенно убивает нежить)' and target == 'monster':
        if any(w in monster['name'].lower() for w in ['скелет', 'призрак', 'упырь', 'некромант', 'вампир']):
            monster['hp'] = 0
            print("Нежить уничтожена!")
        else:
            print("Не действует!")

    elif potion == 'зелье ошеломления (враг пропускает 2 хода)' and target == 'monster':
        monster['stunned'] = 2
        print(f"{monster['name']} ошеломлён на 2 хода!")

    elif potion == 'зелье превращения в осла (превращяет в безобидно осла любого монстра, кроме босса)' and target == 'monster':
        if 'босс' not in monster['name'].lower():
            monster['hp'] = 0
            print(f"{monster['name']} → осёл! Убегает!")
        else:
            print("Не действует на босса!")

#--------------Вспомогательные переменные--------------------------
movements = [(0,0)] #список хранящий историю перемещений по карте
playing_class = {}
a = 0
list_chests = []
list_monsters = []
list_secret = []
bose = ()
portal = ()
key = ()
#--------------Выбор размера поля и класса--------------------------
choise = input('Выберете размеры игрового поля: ') #игрок задает размеры поля
rows, cols = map(int, choise.split())
game_field, player_view = create_game_matrices(rows, cols)
sys.stdout.write('\033[A\033[2K')
sys.stdout.flush()
print(f'Выбор класса: \n ')
for d in clases:
    a += 1
    print(d.capitalize())
    print('-' * 40)
    for e in clases[d]:
        print(e, clases[d][e])
    print('-' * 40)
    print(' ')
choise = input('Ваш выбор: ')
sys.stdout.write('\033[A\033[2K')
sys.stdout.flush()
playing_class = clases[choise]
#--------------Нахождение координат всех комнат--------------------------
a = 0
for e in game_field:
    for d in e:
        if 'портал' == d:
            portal = (a, e.index(d))
        elif 'монстр' == d:
            list_monsters.append((a, e.index(d)))
        elif 'секретная комната' == d:
            list_secret.append((a, e.index(d)))
        elif 'сундук' == d:
            list_chests.append((a, e.index(d)))
        elif 'ключ' == d:
            key = (a, e.index(d))
        elif 'комната босса' == d:
            bose = (a, e.index(d))
    a += 1
#--------------Игровой процесс--------------------------
for row in player_view:
        print(' | '.join(f'{cell:<17}' for cell in row))
while True:
    if movements[-1] == portal and key in movements:
        print('Победа')
        break
    if movements[-1] == key:
        playing_class['стартовый инвентарь']['экипировка'].append('ключ')
    print(' \n1.вверх\n2.вниз\n3.вправо\n4.влево\n ')
    while True:
        choise = input('ваш выбор: ')
        if (movements[-1] == (0, 0) and choise in '14') or (movements[-1] in [(0, x) for x in range(1, rows - 1)] and choise == 1):
            print('невозможно, попробуйте ещё раз\n ')
        elif (movements[-1] == (0, rows - 1) and choise in '13') or (movements[-1] in [(x, rows - 1) for x in range(1, cols - 1)] and choise == 1):
            print('невозможно, попробуйте ещё раз\n ')
        elif (movements[-1] == (cols - 1, 0) and choise in '24') or (movements[-1] in [(x, 0) for x in range(1, cols - 1)] and choise == 1):
            print('невозможно, попробуйте ещё раз\n ')
        elif (movements[-1] == (cols - 1, rows - 1) and choise in '23') or (movements[-1] in [(cols - 1, x) for x in range(1, rows - 1)] and choise == 1):
            print('невозможно, попробуйте ещё раз\n ')
        else:
            moving(choise)
            break
    for row in player_view:
        print(' | '.join(f'{cell:<17}' for cell in row))
    if movements[-1] in list_monsters:
        monster_name = random.choice(list(monsters_stats.keys()))
        if not battle(playing_class, monster_name):
            print("Игра окончена.")
            break
        else:
            game_field[movements[-1][0]][movements[-1][1]] = 'пусто'
            player_view[movements[-1][0]][movements[-1][1]] = 'победа'
            for row in player_view:
                print(' | '.join(f'{cell:<17}' for cell in row))
        

    





