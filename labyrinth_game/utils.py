import math

from labyrinth_game.constants import ROOMS

key = 'treasure_key'
words = {
    'один': '1', 'два': '2', 'три': '3', 'четыре': '4', 'пять': '5',
    'шесть': '6', 'семь': '7', 'восемь': '8', 'девять': '9', 'десять': '10'
}

def describe_current_room(game_state):
    room = game_state['current_room']
    info = ROOMS[room]
    printInfo(room, info)


def printInfo(roomname, info):
    print(f'============ {roomname.upper()} ============')
    print("Описание: ", info['description'])
    if len(info['items']) != 0:
        print("Заметные предметы: ", info['items'])

    print_exits(info['exits'], 4)
    if info.get("puzzle") is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def print_exits(data, indent=0):
    print("Выходы: ")
    for key, value in data.items():
        if isinstance(value, dict):
            print(' ' * indent + f"{key}:")
            print_exits(value, indent + 4)
        else:
            print(' ' * indent + f"{key}: {value}")

def solve_puzzle(game_state):
    room = game_state['current_room']
    if ROOMS[room].get("puzzle") is None:
        print("Загадок здесь нет.")
        return
    
    puzzle = ROOMS[room]["puzzle"]
    print(puzzle[0])
    
    answer = input("Ваш ответ: ")
    while answer != "stop" and not game_state['game_over']:
        if answer != puzzle[1] and puzzle[1] != words.get(answer):
            print("Неверно. Попробуйте снова. Чтобы закончить - stop")
            if room == "trap_room":
                trigger_trap(game_state)
                if game_state['game_over']:
                    return
            answer = input("Ваш ответ: ")
            continue

        print("Успех!")
        ROOMS[room]["puzzle"] = None
        print("Вы получаете награду")
        getAward(game_state)
        return True
    
    return False

def getAward(game_state):
    award = ROOMS[game_state['current_room']]['award']
    ROOMS[game_state['current_room']]['award'] = None
    game_state["player_inventory"].append(award)
    print("Вы получаете:", award)

def attempt_open_treasure(game_state):
    if key in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
    else:
        cmd = input("Сундук заперт. ... Ввести код? (да/нет)")
        if cmd != "да":
            print("Вы отступаете от сундука.")
            return
        
        if not solve_puzzle(game_state):
            print("Вы можете вернуться к сундуку позже.")
            return

    ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
    print("В сундуке сокровище! Вы победили!")
    game_state['game_over'] = True

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.345) * 6789.1011
    x = x - math.floor(x)
    return math.floor(x * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    if len(game_state['player_inventory']) == 0:
        damage = pseudo_random(game_state['steps_taken'], 9)
        p = 3
        if damage < p:
            print("Вы получили смертельный урон")
            game_state['game_over'] = True
        else:
            print("Игрок уцелел")
    else:
        number_item = pseudo_random(
            game_state['steps_taken'], len(game_state['player_inventory'])
        )
        item = deleteItemOfInvenory(game_state, number_item)
        print("Вы потеряли предмет: ", item)

def deleteItemOfInvenory(game_state, n_item):
    return game_state['player_inventory'].pop(n_item)

def random_event(game_state):
    p_event = pseudo_random(game_state['steps_taken'], 10)
    if p_event < 4:
        event = pseudo_random(game_state['steps_taken'], 3)
        match event:
            case 0:
                print("Вы находите монетку")
                game_state['player_inventory'].append("coin")
            case 1:
                print("Вы слышите шорох")
                if "sword" in game_state['player_inventory']:
                    print("Вы отпугнули существо")
            case 2:
                if game_state['current_room'] == "trap_room" and "torch" not in game_state['player_inventory']:
                    print("Вы в опасности")
                    trigger_trap(game_state)

def show_help(COMMANDS):
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")