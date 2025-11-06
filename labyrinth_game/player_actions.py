import labyrinth_game.utils as u
from labyrinth_game.constants import ROOMS


def show_inventory(game_state):
    if len(game_state["player_inventory"]) == 0:
        print("Инвентарь пустой")
    else:
        print("Инвентарь: ", game_state["player_inventory"])

def get_input(prompt="> "):
    try:
        s = input(prompt)
        return s
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 
    
def move_player(game_state, direction):
    if ROOMS[game_state["current_room"]]['exits'].get(direction) is None:
        print("Нельзя пойти в этом направлении.")
        return
    
    if ROOMS[game_state["current_room"]]['exits'].get(direction) == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        else:
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
            )

    game_state["steps_taken"] += 1
    game_state["current_room"] = ROOMS[game_state["current_room"]]['exits'][direction]
    u.random_event(game_state)

def take_item(game_state, item_name):
    if item_name not in ROOMS[game_state["current_room"]]["items"]:
        print("Такого предмета здесь нет.")
        return
    
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    ROOMS[game_state["current_room"]]["items"].remove(item_name)
    game_state["player_inventory"].append(item_name)
    print("Вы подняли:", item_name)

def use_item(game_state, item_name):
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return
    
    match item_name:
        case "torch":
            print("Стало светлее")
        case "sword":
            print("Вы стали увереннее")
        case "bronze box":
            print("Вы открыли бронзовый сундук")
            if 'rusty_key' not in game_state["player_inventory"]:
                game_state["player_inventory"].append('rusty_key')
        case _:
            print("Вы не знаете как это использовать")
            return
    
    game_state["player_inventory"].remove(item_name)