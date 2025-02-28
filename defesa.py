import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx, turret_type):
        pg.sprite.Sprite.__init__(self)
        self.turret_type = turret_type
        self.upgrade_level = 1
        self.shot_fx = shot_fx
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.selected = False
        self.target = None
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.rect.center = (self.x, self.y)
        # Remova a inicialização das imagens de alcance aqui. Elas serão criadas dinamicamente.
        self.is_animating = False
        self.last_shot = pg.time.get_ticks()  # Inicializa last_shot
        self.last_slow = pg.time.get_ticks()  # Inicializa last_slow
        self.load_turret_data()
        self.create_range_image()

    def load_turret_data(self):
        data = self.get_turret_data()
        self.range = data["range"]
        self.cooldown = data["cooldown"]
        self.damage = data["damage"]
        
        # Configurações específicas para a torre2
        if self.turret_type == "torre2":
            self.slow_amount = c.TURRET2_SLOW_AMOUNT
            self.slow_duration = c.TURRET2_SLOW_DURATION
            self.slow_cooldowns = {
                1: c.TURRET2_SLOW_COOLDOWN_LEVEL1,
                2: c.TURRET2_SLOW_COOLDOWN_LEVEL2,
                3: c.TURRET2_SLOW_COOLDOWN_LEVEL3,
                4: c.TURRET2_SLOW_COOLDOWN_LEVEL4
            }
        else:
            # Garante que esses atributos não existam para outras torres
            self.slow_amount = 0
            self.slow_duration = 0
            self.slow_cooldowns = {}


    def get_turret_data(self):
        return TURRET_DATA[self.turret_type][self.upgrade_level]

    def load_images(self, sprite_sheet):
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world):
        #if self.is_animating: #Remova essa linha
        self.play_animation() #Remova essa linha
        if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
            self.pick_target(enemy_group)
        
        if self.turret_type == "torre2":
            self.apply_slow(enemy_group, world)

    def pick_target(self, enemy_group):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(y_dist, x_dist))
                    self.target.health -= self.damage
                    self.shot_fx.play()
                    self.last_shot = pg.time.get_ticks()
                    self.is_animating = True
                    break

    def apply_slow(self, enemy_group, world):
        """Aplica slow aos inimigos dentro do alcance da torre."""
        #Verifica se o cooldown do slow já passou
        if pg.time.get_ticks() - self.last_slow > (self.slow_cooldowns[self.upgrade_level] / world.game_speed):
            for enemy in enemy_group:
                if enemy.health > 0:
                    x_dist = enemy.pos[0] - self.x
                    y_dist = enemy.pos[1] - self.y
                    dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                    if dist < self.range:
                        enemy.slow_down(self.slow_amount, self.slow_duration)
                        self.last_slow = pg.time.get_ticks()
                        break  # Aplica slow a um inimigo por vez

    def play_animation(self):
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.is_animating = False
            self.image = self.animation_list[self.frame_index]

    def create_range_image(self):
        """Cria uma imagem circular para representar o alcance da torre."""
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        pg.draw.circle(self.range_image, (128, 128, 128, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        """Desenha a torre e, se selecionada, seu alcance."""
        # Removendo a rotação da torre
        #self.image = pg.transform.rotate(self.original_image, -self.angle) #Removi essa linha
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def upgrade(self):
        """Aprimora a torre para o próximo nível."""
        if self.upgrade_level < c.TURRET_LEVELS:
            self.upgrade_level += 1
            self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
            self.frame_index = 0
            self.original_image = self.animation_list[self.frame_index]
            self.image = self.original_image #Adicione essa linha
            self.load_turret_data() # Recarrega os dados da torre (range, dano, cooldown)
            self.create_range_image() # Atualiza a imagem do alcance
