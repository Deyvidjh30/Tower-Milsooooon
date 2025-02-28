import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA

class World():
    def __init__(self, data, map_image):
        # Initialize the World class with basic attributes
        self.level = 1  # Current level of the game
        self.game_speed = 1  # Game speed
        self.health = c.HEALTH  # Player's health (defined in constants.py)
        self.money = c.MONEY  # Player's money (defined in constants.py)
        self.tile_map = []  # Tile map (blocks) of the level
        self.waypoints = []  # Waypoints that enemies will follow
        self.level_data = data  # Level data (loaded from a JSON file, for example)
        self.image = map_image  # Image of the level map
        self.enemy_list = []  # List of enemies to be spawned
        self.spawned_enemies = 0  # Counter of enemies that have already been spawned
        self.killed_enemies = 0  # Counter of enemies that have been killed
        self.missed_enemies = 0  # Counter of enemies that passed without being killed

    def process_data(self):
        # Process level data to extract relevant information
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                # If the layer is the tilemap, store the tile data
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                # If the layer is waypoints, process the waypoints
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        # Iterate through the waypoints to extract x and y coordinates
        for point in data:
            temp_x = point.get("x")  # Get the x coordinate of the point
            temp_y = point.get("y")  # Get the y coordinate of the point
            self.waypoints.append((temp_x, temp_y))  # Add the point to the list of waypoints

    def process_enemies(self):
        try:
            enemies = ENEMY_SPAWN_DATA[self.level - 1]
        except IndexError:
            print("You have reached the maximum level! Congratulations!")
            self.reset_level()
            self.level = 1
            return

        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        # Check if the level has been completed
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True  # Return True if all enemies have been killed or passed

    def reset_level(self):
        # Reset variables related to enemies to start a new level
        self.enemy_list = []  # Clear the list of enemies
        self.spawned_enemies = 0  # Reset the counter of spawned enemies
        self.killed_enemies = 0  # Reset the counter of killed enemies
        self.missed_enemies = 0  # Reset the counter of enemies that passed

    def draw(self, surface):
        # Draw the level map on the screen
        surface.blit(self.image, (0, 0))  # Draw the map image at position (0, 0)
