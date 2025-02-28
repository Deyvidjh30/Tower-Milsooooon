import pygame as pg
from pygame.math import Vector2
import constants as c

class Aliado(pg.sprite.Sprite):
    def __init__(self, waypoints, images):  # Removido allied_health
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        # Inverte a lista de waypoints para o aliado seguir o caminho inverso
        self.pos = Vector2(self.waypoints[-1])
        self.target_waypoint = len(self.waypoints) - 2
        self.speed = 1  # Velocidade do aliado
        self.frames = images  # Lista de frames de animação
        self.current_frame = 0
        self.animation_speed = 0.1  # Velocidade de animação mais lenta (ajuste conforme necessário)
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(center=self.pos)
        self.flip_image = True  # Inicialmente, espelhar a imagem horizontalmente

    def update(self, world):
        self.move(world)
        self.animate()
        self.rect.center = self.pos

    def move(self, world):
        if self.target_waypoint >= 0:
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Aliado chegou ao ponto inicial
            self.kill()
            return

        dist = self.movement.length()
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint -= 1

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        # Espelha a imagem horizontalmente se flip_image for True
        if self.flip_image:
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
