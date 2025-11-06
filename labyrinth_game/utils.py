from labyrinth_game.constants import ROOMS

key = 'treasure_key'

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
        if answer != puzzle[1]:
            print("Неверно. Попробуйте снова. Чтобы закончить - stop")
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

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 