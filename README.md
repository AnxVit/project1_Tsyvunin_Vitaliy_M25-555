# project1_Tsyvunin_Vitaliy_M25-555

## Labyrinth Game
Игра создана на основе функционального программирования языка Python.

### Описание игры
Карта игры:
```mermaid
graph TD
    entrance["Entrance"] -->|north| hall
    entrance -->|east| trap_room

    hall -->|south| entrance
    hall -->|west| library
    hall -->|north| treasure_room

    trap_room -->|west| entrance
    trap_room -->|north| cave

    library -->|east| hall
    library -->|north| armory

    armory -->|south| library

    treasure_room -->|south| hall

    cave -->|south| trap_room
    cave -->|east| lair

    lair -->|west| cave
```

Цель: вам необходимо открыть сундук и забрать главные сокровища

Вас ждут загадки, ловушки и предметы, которую могут помочь вам на пути к цели.

### Команды для работы с проектом
```bash
# Установить зависимости
make install

# Запустить проект
make project

# Собрать пакет
make build

# Проверить публикацию (dry-run)
make publish

# Установить собранный пакет локально
make package-install

# Проверить стиль кода
make lint
```

## Пример работы игры
[![asciicast](https://asciinema.org/a/9F6JYHb8sQVnFY8WeHfae40Wf)](https://asciinema.org/a/9F6JYHb8sQVnFY8WeHfae40Wf)