#!/usr/bin/env python3

import labyrinth_game.player_actions as pa
import labyrinth_game.utils as u

from labyrinth_game.constants import ROOMS

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def process_command(game_state, command):
    cmd = command.split()
    match cmd[0]:
        case "go":
            if len(cmd) != 2:
                print("Неправильная команда")
                return
            
            pa.move_player(game_state, cmd[1])
            u.describe_current_room(game_state)
        case "look":
            u.describe_current_room(game_state)
        case "take":
            if len(cmd) != 2:
                print("Неправильная команда")
                return
            
            pa.take_item(game_state, cmd[1])
        case "use":
            if len(cmd) != 2:
                print("Неправильная команда")
                return
            # pa.use_item(game_state, cmd[1])
        case "inventory":
            pa.show_inventory(game_state)
        case "quit":
            game_state['game_over'] = True
            print("Game Over")
        case _:
            print("Неверная команда")
    
def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    u.describe_current_room(game_state)
    while not game_state['game_over']:
        inp = pa.get_input()
        process_command(game_state, inp)

    print("Game over!")

if __name__ == "__main__":
    main()