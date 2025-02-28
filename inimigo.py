import pygame as pg
from pygame.math import Vector2
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])  # Posição inicial
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]  # Vida do inimigo
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]  # Velocidade do inimigo
        self.original_speed = self.speed  # Armazena a velocidade original
        self.slowed_until = 0 # Tempo em que o slow ficará ativo (0 = sem slow)


        # Carrega os frames de animação
        self.frames = images.get(enemy_type)  # Lista de frames
        self.current_frame = 0
        self.animation_speed = 0.2  # Velocidade da animação
        self.image = self.frames[self.current_frame]  # Frame inicial
        self.rect = self.image.get_rect(center=self.pos)  # Define o retângulo com base na posição

    def update(self, world):
        self.move(world)  # Move o inimigo
        self.animate()  # Atualiza a animação
        self.check_alive(world)  # Verifica se o inimigo ainda está vivo
        self.rect.center = self.pos  # Atualiza a posição do retângulo

    def move(self, world):
        # Se estiver slowed, usa a velocidade reduzida
        if pg.time.get_ticks() < self.slowed_until:
            speed = self.speed
        else:
            speed = self.original_speed
            self.speed = self.original_speed  # Garante que a velocidade seja restaurada corretamente

        # Define o próximo waypoint como alvo
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Inimigo chegou ao final do caminho
            self.kill()  # Remove o inimigo do jogo
            world.health -= 1  # Reduz a vida do jogador
            world.missed_enemies += 1  # Incrementa o contador de inimigos que passaram

        # Calcula a distância até o alvo
        dist = self.movement.length()

        # Move o inimigo em direção ao waypoint
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1  # Avança para o próximo waypoint

    def animate(self):
        # Atualiza o frame da animação
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(center=self.pos)

    def check_alive(self, world):
        # Verifica se o inimigo ainda está vivo
        if self.health <= 0:
            world.killed_enemies += 1  # Incrementa o contador de inimigos mortos
            world.money += c.KILL_REWARD  # Adiciona recompensa ao jogador
            self.kill()  # Remove o inimigo do jogo
            
    def slow_down(self, slow_amount, duration):
        """Reduz a velocidade do inimigo por um tempo limitado."""
        self.speed = self.original_speed * (1 - slow_amount)
        self.slowed_until = pg.time.get_ticks() + duration

