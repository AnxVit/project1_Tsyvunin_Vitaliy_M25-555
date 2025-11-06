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