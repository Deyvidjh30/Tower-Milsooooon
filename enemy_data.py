ENEMY_SPAWN_DATA = [
    {"weak": 3, "medium": 0, "strong": 0, "elite": 0},   # Level 1
    {"weak": 5, "medium": 1, "strong": 0, "elite": 0},   # Level 2
    {"weak": 7, "medium": 5, "strong": 0, "elite": 0},   # Level 3
    {"weak": 10, "medium": 5, "strong": 0, "elite": 0},   # Level 4
    {"weak": 5, "medium": 10, "strong": 0, "elite": 0},  # Level 5
    {"weak": 5, "medium": 5, "strong": 2, "elite": 0},   # Level 6
    {"weak": 5, "medium": 2, "strong": 5, "elite": 0},   # Level 7
    {"weak": 10, "medium": 5, "strong": 6, "elite": 0},  # Level 8
    {"weak": 15, "medium": 10, "strong": 5, "elite": 0},  # Level 9
    {"weak": 20, "medium": 10, "strong": 15, "elite": 1}, # Level 10
    {"weak": 20, "medium": 10, "strong": 15, "elite": 1}  # Level 11 (if you have it)
]

ENEMY_DATA = {
    "weak": {"health": 80, "speed": 0.75},
    "medium": {"health": 60, "speed": 0.9},
    "strong": {"health": 40, "speed": 1.5},
    "elite": {"health": 10000, "speed": 0.5}
}