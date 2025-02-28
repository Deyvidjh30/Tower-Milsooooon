ROWS = 15
COLS = 15
TILE_SIZE = 48
SIDE_PANEL = 300
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FPS = 60
HEALTH = 2
MONEY = 300
TOTAL_LEVELS = 10

#enemy constants
SPAWN_COOLDOWN = 900

#turret constants
TURRET_LEVELS = 4
BUY_COST_TORRE1 = 300  # Custo da primeira torre
BUY_COST_TORRE2 = 400  # Custo da segunda torre
BUY_COST_TORRE3 = 500  # Custo da terceira torre
UPGRADE_COST = 125
KILL_REWARD = 5
LEVEL_COMPLETE_REWARD = 100

ANIMATION_STEPS = 8
ANIMATION_DELAY = 120

# Constantes para a Turret2 (Slow)
TURRET2_SLOW_AMOUNT = 0.5  # Porcentagem de redução da velocidade (ex: 0.5 = 50%)
TURRET2_SLOW_DURATION = 3000 # Duração do slow em milissegundos
TURRET2_SLOW_COOLDOWN_LEVEL1 = 5000 # Cooldown no level 1
TURRET2_SLOW_COOLDOWN_LEVEL2 = 4000 # Cooldown no level 2
TURRET2_SLOW_COOLDOWN_LEVEL3 = 3000 # Cooldown no level 3
TURRET2_SLOW_COOLDOWN_LEVEL4 = 2000 # Cooldown no level 4












# button.py

# import pygame as pg

# class Button():
#     def __init__(self, x, y, image, single_click):
#         self.image = image  # Imagem do botÃ£o
#         self.rect = self.image.get_rect()  # RetÃ¢ngulo da imagem
#         self.rect.topleft = (x, y)  # PosiÃ§Ã£o do botÃ£o
#         self.clicked = False  # Estado de clique
#         self.single_click = single_click  # Se o botÃ£o Ã© de clique Ãºnico

#     def draw(self, surface):
#         action = False  # AÃ§Ã£o a ser retornada (se o botÃ£o foi clicado)
#         # ObtÃ©m a posiÃ§Ã£o do mouse
#         pos = pg.mouse.get_pos()
        
#         # Verifica se o mouse estÃ¡ sobre o botÃ£o e se foi clicado
#         if self.rect.collidepoint(pos):
#             if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
#                 action = True  # O botÃ£o foi clicado
#                 # Se o botÃ£o for de clique Ãºnico, define clicked como True
#                 if self.single_click:
#                     self.clicked = True

#         # Reseta o estado de clique quando o botÃ£o do mouse Ã© solto
#         if pg.mouse.get_pressed()[0] == 0:
#             self.clicked = False

#         # Desenha o botÃ£o na tela
#         surface.blit(self.image, self.rect)

#         return action  # Retorna se o botÃ£o foi clicado




# enemy_data.py
# ENEMY_SPAWN_DATA = [
#     {"weak": 3, "medium": 0, "strong": 0, "elite": 0},   # Level 1
#     {"weak": 4, "medium": 0, "strong": 0, "elite": 0},   # Level 2
#     {"weak": 2, "medium": 3, "strong": 0, "elite": 0},   # Level 3
#     {"weak": 5, "medium": 5, "strong": 0, "elite": 0},   # Level 4
#     {"weak": 0, "medium": 10, "strong": 0, "elite": 0},  # Level 5
#     {"weak": 5, "medium": 5, "strong": 2, "elite": 0},   # Level 6
#     {"weak": 5, "medium": 2, "strong": 5, "elite": 0},   # Level 7
#     {"weak": 10, "medium": 5, "strong": 6, "elite": 0},  # Level 8
#     {"weak": 15, "medium": 10, "strong": 5, "elite": 0},  # Level 9
#     {"weak": 20, "medium": 10, "strong": 15, "elite": 1}, # Level 10
#     {"weak": 20, "medium": 10, "strong": 15, "elite": 1}  # Level 11 (if you have it)
# ]

# ENEMY_DATA = {
#     "weak": {"health": 80, "speed": 0.75},
#     "medium": {"health": 60, "speed": 0.9},
#     "strong": {"health": 40, "speed": 1.5},
#     "elite": {"health": 1000, "speed": 0.4}
# }





# turret_dat.py

# TURRET_DATA = [
#   {
#     #1
#     "range": 120,
#     "cooldown": 800,
#   },
#   {
#     #2
#     "range": 140,
#     "cooldown": 700,
#   },
#   {
#     #3
#     "range": 160,
#     "cooldown": 700,
#   },
#   {
#     #4
#     "range": 210,
#     "cooldown": 500,
#   }
# ]














# inimigo.py

# import pygame as pg
# from pygame.math import Vector2
# import constants as c
# from enemy_data import ENEMY_DATA

# class Enemy(pg.sprite.Sprite):
#     def __init__(self, enemy_type, waypoints, images):
#         pg.sprite.Sprite.__init__(self)
#         self.waypoints = waypoints
#         self.pos = Vector2(self.waypoints[0])  # Posição inicial
#         self.target_waypoint = 1
#         self.health = ENEMY_DATA.get(enemy_type)["health"]  # Vida do inimigo
#         self.speed = ENEMY_DATA.get(enemy_type)["speed"]  # Velocidade do inimigo

#         # Carrega os frames de animação
#         self.frames = images.get(enemy_type)  # Lista de frames
#         self.current_frame = 0
#         self.animation_speed = 0.2  # Velocidade da animação
#         self.image = self.frames[self.current_frame]  # Frame inicial
#         self.rect = self.image.get_rect(center=self.pos)  # Define o retângulo com base na posição

#     def update(self, world):
#         self.move(world)  # Move o inimigo
#         self.animate()  # Atualiza a animação
#         self.check_alive(world)  # Verifica se o inimigo ainda está vivo
#         self.rect.center = self.pos  # Atualiza a posição do retângulo

#     def move(self, world):
#         # Define o próximo waypoint como alvo
#         if self.target_waypoint < len(self.waypoints):
#             self.target = Vector2(self.waypoints[self.target_waypoint])
#             self.movement = self.target - self.pos
#         else:
#             # Inimigo chegou ao final do caminho
#             self.kill()  # Remove o inimigo do jogo
#             world.health -= 1  # Reduz a vida do jogador
#             world.missed_enemies += 1  # Incrementa o contador de inimigos que passaram

#         # Calcula a distância até o alvo
#         dist = self.movement.length()

#         # Move o inimigo em direção ao waypoint
#         if dist >= (self.speed * world.game_speed):
#             self.pos += self.movement.normalize() * (self.speed * world.game_speed)
#         else:
#             if dist != 0:
#                 self.pos += self.movement.normalize() * dist
#             self.target_waypoint += 1  # Avança para o próximo waypoint

#     def animate(self):
#         # Atualiza o frame da animação
#         self.current_frame += self.animation_speed
#         if self.current_frame >= len(self.frames):
#             self.current_frame = 0
#         self.image = self.frames[int(self.current_frame)]
#         self.rect = self.image.get_rect(center=self.pos)

#     def check_alive(self, world):
#         # Verifica se o inimigo ainda está vivo
#         if self.health <= 0:
#             world.killed_enemies += 1  # Incrementa o contador de inimigos mortos
#             world.money += c.KILL_REWARD  # Adiciona recompensa ao jogador
#             self.kill()  # Remove o inimigo do jogo
    