from labyrinth_game.constants import ROOMS


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