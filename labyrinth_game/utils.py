import math

import labyrinth_game.constants as const


def describe_current_room(game_state):
    room = game_state['current_room']
    info = const.ROOMS[room]
    printInfo(room, info)


def printInfo(roomname, info):
    print(f'============ {roomname.upper()} ============')
    print("Описание: ", info['description'])
    if len(info['items']) != 0:
        print("Заметные предметы: ", info['items'])

    print_exits(info['exits'], const.BASE_IDENT)
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
    if const.ROOMS[room].get("puzzle") is None:
        print("Загадок здесь нет.")
        return
    
    puzzle = const.ROOMS[room]["puzzle"]
    print(puzzle[0])
    
    answer = input("Ваш ответ: ")
    while answer != "stop" and not game_state['game_over']:
        if answer != puzzle[1] and puzzle[1] != const.WORDS.get(answer):
            print("Неверно. Попробуйте снова. Чтобы закончить - stop")
            if room == "trap_room" or room == "lair":
                trigger_trap(game_state)
                if game_state['game_over']:
                    return
            answer = input("Ваш ответ: ")
            continue

        print("Успех!")
        const.ROOMS[room]["puzzle"] = None
        print("Вы получаете награду")
        getAward(game_state)
        return True
    
    return False

def getAward(game_state):
    award = const.ROOMS[game_state['current_room']]['award']
    const.ROOMS[game_state['current_room']]['award'] = None
    game_state["player_inventory"].append(award)
    print("Вы получаете:", award)

def attempt_open_treasure(game_state):
    if const.KEY in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
    else:
        cmd = input("Сундук заперт. ... Ввести код? (да/нет)")
        if cmd != "да":
            print("Вы отступаете от сундука.")
            return
        
        if not solve_puzzle(game_state):
            print("Вы можете вернуться к сундуку позже.")
            return

    const.ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
    print("В сундуке сокровище! Вы победили!")
    game_state['game_over'] = True

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.345) * 6789.1011
    x = x - math.floor(x)
    return math.floor(x * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    if len(game_state['player_inventory']) == 0 or game_state['current_room'] == 'lair':
        damage = pseudo_random(game_state['steps_taken'], const.DAMAGE_PROBABILITY)
        p = const.ROOM_DAMAGE 
        if game_state['current_room'] == 'lair':
            p = const.LAIR_DAMAGE
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
    p_event = pseudo_random(game_state['steps_taken'], const.EVENT_PROBABILITY)
    if p_event < const.EVENT_SUCCESS:
        event = pseudo_random(game_state['steps_taken'], const.NUMER_EVENTS)
        match event:
            case 0:
                print("Вы находите монетку")
                game_state['player_inventory'].append("coin")
            case 1:
                print("Вы слышите шорох")
                if "sword" in game_state['player_inventory']:
                    print("Вы отпугнули существо")
            case 2:
                if (game_state['current_room'] == "trap_room" and 
                        "torch" not in game_state['player_inventory']):
                    print("Вы в опасности")
                    trigger_trap(game_state)

def show_help(COMMANDS):
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")