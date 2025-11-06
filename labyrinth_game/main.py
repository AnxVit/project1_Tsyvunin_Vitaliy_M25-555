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
        case "":
            print()
    
def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    u.describe_current_room(game_state)
    while not game_state['game_over']:
        inp = pa.get_input()
        process_command(game_state, inp)

    print("Game over!")

if __name__ == "__main__":
    main()