import pygame as pg
import json
from inimigo import Enemy
from mundo import World
from defesa import Turret
from button import Button
import constants as c
from menu import main_menu
import sys
from aliado import Aliado

# Inicialização do Pygame
pg.init()

# Inicializa o clock do pygame
clock = pg.time.Clock()  # Adicionado para corrigir o erro

# Configurações da janela
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Milson Defense")

# Variáveis para controle do limite de torres
tower_counts = {
    "torre1": 0,
    "torre2": 0,
    "torre3": 0
}

tower_limits = {
    "torre1": 3,
    "torre2": 2,
    "torre3": 1
}

# Carregue as imagens dos botões desativados
buy_turret1_image_disabled = pg.image.load('buttons/buy_turret_disabled.png').convert_alpha()
buy_turret2_image_disabled = pg.image.load('buttons/buy_turret2_disabled.png').convert_alpha()
buy_turret3_image_disabled = pg.image.load('buttons/buy_turret3_disabled.png').convert_alpha()

# Carrega a imagem do botão de venda
sell_image = pg.image.load('buttons/sell.png').convert_alpha()

# Exibe o menu principal
menu_result = main_menu(screen)

# Sai do jogo se o jogador escolher "Sair"
if menu_result == "quit":
    pg.quit()
    sys.exit()

# Variáveis do jogo
game_over = False
game_outcome = 0  # -1: derrota, 1: vitória
level_started = False
first_level = True  # Variável para controlar se é o primeiro nível
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = None
selected_turret = None
turret3_placed = False  # Variável para verificar se a torre 3 foi colocada
number_of_allies = 5

# Variáveis para controlar a invocação do aliado
can_spawn_allied = True
allied_cooldown = 8000
# Cooldown inicial em milissegundos (5 segundos)
last_allied_spawn = 1000
allied_damage = 80

# Carregamento de imagens
map_image = pg.image.load('levels/level.png').convert_alpha()

# Spritesheets das torres
turret1_spritesheets = []
turret2_spritesheets = []
turret3_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret1_sheet = pg.image.load(f'turrets/turret1_{x}.png').convert_alpha()
    turret1_spritesheets.append(turret1_sheet)
    turret2_sheet = pg.image.load(f'turrets/turret2_{x}.png').convert_alpha()
    turret2_spritesheets.append(turret2_sheet)
    turret3_sheet = pg.image.load(f'turrets/turret3_{x}.png').convert_alpha()
    turret3_spritesheets.append(turret3_sheet)

# Imagens do cursor
cursor_turret1 = pg.image.load('turrets/cursor_turret.png').convert_alpha()
cursor_turret2 = pg.image.load('turrets/slow_cursor.png').convert_alpha()
cursor_turret3 = pg.image.load('turrets/mage_cursor.png').convert_alpha()

# Inimigos
enemy_images = {
    "weak": [pg.image.load(f'Ataque/Milson/sprite_milson{i}.png').convert_alpha() for i in range(5)],
    "medium": [pg.image.load(f'Ataque/Silvia/silvia_{i}.png').convert_alpha() for i in range(3)],
    "strong": [pg.image.load(f'Ataque/Renata/sprite_{i}.png').convert_alpha() for i in range(21)],
    "elite": [pg.image.load(f'Ataque/Boss Milson/milson/sprite_{i}.png').convert_alpha() for i in range(5)]
}

# Aliados (carrega as imagens dos inimigos "fracos" para simplificar)
allied_images_level1 = [pg.image.load(f'invocations/sprite_russo4_{i}.png').convert_alpha() for i in range(3)]
allied_images_level2 = [pg.image.load(f'invocations/sprite_russo1_{i}.png').convert_alpha() for i in range(3)]
allied_images_level3 = [pg.image.load(f'invocations/sprite_russo2_{i}.png').convert_alpha() for i in range(3)]
allied_images_level4 = [pg.image.load(f'invocations/sprite_russo3_{i}.png').convert_alpha() for i in range(3)]

# Dicionário para armazenar as imagens dos aliados por nível da torre 3
allied_images_by_level = {
    1: allied_images_level1,
    2: allied_images_level2,
    3: allied_images_level3,
    4: allied_images_level4
}

# Botões
buy_turret1_image = pg.image.load('buttons/buy_turret.png').convert_alpha()
buy_turret2_image = pg.image.load('buttons/buy_turret2.png').convert_alpha()
buy_turret3_image = pg.image.load('buttons/buy_turret3.png').convert_alpha()
cancel_image = pg.image.load('buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('buttons/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('buttons/begin.png').convert_alpha()
restart_image = pg.image.load('buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('buttons/fast_forward.png').convert_alpha()
#sell_image = pg.image.load('buttons/sell.png').convert_alpha()

# Interface gráfica
heart_image = pg.image.load("gui/heart.png").convert_alpha()
coin_image = pg.image.load("gui/coin.png").convert_alpha()

# Carrega os sons
shot_fx = pg.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(10)

# Carrega os dados do nível a partir do arquivo JSON
with open('levels/level.tmj') as file:
    world_data = json.load(file)

# Carrega as fontes para exibir texto na tela
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36, bold=True)

# Funções auxiliares
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    pg.draw.rect(screen, "black", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    draw_text("NIVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)
    

def create_turret(mouse_pos, turret_type):
    global turret3_placed  # Referencia a variável global
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            if tower_counts[turret_type] < tower_limits[turret_type]:  # Verifica se o limite foi atingido
                if turret_type == "torre1":
                    if world.money >= c.BUY_COST_TORRE1:
                        new_turret = Turret(turret1_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, "torre1")
                        world.money -= c.BUY_COST_TORRE1
                        tower_counts["torre1"] += 1  # Incrementa o contador de torres
                    else:
                        return False
                elif turret_type == "torre2":
                    if world.money >= c.BUY_COST_TORRE2:
                        new_turret = Turret(turret2_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, "torre2")
                        world.money -= c.BUY_COST_TORRE2
                        tower_counts["torre2"] += 1  # Incrementa o contador de torres
                    else:
                        return False
                elif turret_type == "torre3":
                    if world.money >= c.BUY_COST_TORRE3:
                        new_turret = Turret(turret3_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, "torre3")
                        world.money -= c.BUY_COST_TORRE3
                        turret3_placed = True  # Define que a torre 3 foi colocada
                        tower_counts["torre3"] += 1  # Incrementa o contador de torres
                    else:
                        return False
                turret_group.add(new_turret)
                return True
            else:
                print(f"Limite de torres {turret_type} atingido!")  # Mensagem caso o limite tenha sido atingido
                return False
        return False

def spawn_allies():
    # Determina o nível da torre 3 (se houver)
    turret3_level = 0
    for turret in turret_group:
        if turret.turret_type == "torre3":
            turret3_level = turret.upgrade_level + 1  # Nível da torre é upgrade_level + 1
            break

    # Seleciona as imagens dos aliados com base no nível da torre 3
    if turret3_level > 0 and turret3_level <= 4:
        images = allied_images_by_level[turret3_level]
    else:
        images = allied_images_level1  # Imagens padrão caso não haja torre3

    # Cria aliados
    for _ in range(number_of_allies):
        aliado = Aliado(world.waypoints, images)
        allied_group.add(aliado)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
    return None

def clear_selection():
    for turret in turret_group:
        turret.selected = False

def sell_turret(turret):
    if turret.turret_type != "torre3":  # Impede a venda da torre3
        if turret.turret_type == "torre1":
            world.money += int(c.BUY_COST_TORRE1 * 0.7)  # Exemplo: 70% do valor original
            tower_counts["torre1"] -= 1  # Decrementa o contador de torres
        elif turret.turret_type == "torre2":
            world.money += int(c.BUY_COST_TORRE2 * 0.7)  # Exemplo: 70% do valor original
            tower_counts["torre2"] -= 1  # Decrementa o contador de torres
        turret_group.remove(turret)
        turret.kill()  # Remove o sprite da memória
        return True
    else:
        print("Torre3 não pode ser vendida!")
        return False

def check_tower_limit(turret_type):
    if tower_counts[turret_type] >= tower_limits[turret_type]:
        return True
    else:
        return False

# Cria o mundo
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Cria os grupos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
allied_group = pg.sprite.Group()

# Cria os botões
turret1_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret1_image, True)
turret2_button = Button(c.SCREEN_WIDTH + 30, 180, buy_turret2_image, True)
turret3_button = Button(c.SCREEN_WIDTH + 30, 240, buy_turret3_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 300, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 370, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 500, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 500, fast_forward_image, False)
sell_button = Button(c.SCREEN_WIDTH + 5, 430, sell_image, True)  # Ajuste as coordenadas conforme necessário

# Loop principal do jogo
run = True
while run:
    clock.tick(c.FPS)

    #########################
    # SEÇÃO DE ATUALIZAÇÃO
    #########################

    if not game_over:
        if world.health <= 0:
            game_over = True
            game_outcome = -1

        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1

        enemy_group.update(world)
        turret_group.update(enemy_group, world)
        allied_group.update(world)

        # Lógica para invocar aliados com cooldown, só se a Torre 3 foi posicionada
        current_time = pg.time.get_ticks()
        if turret3_placed:
            if current_time - last_allied_spawn > allied_cooldown:
                spawn_allies()
                last_allied_spawn = current_time

        # Verificação de colisão entre aliados e inimigos
        for aliado in allied_group:
            collision = pg.sprite.spritecollide(aliado, enemy_group, False)
            if collision:
                enemy = collision[0]
                turret3_level = 0
                for turret in turret_group:
                    if turret.turret_type == "torre3":
                        turret3_level = turret.upgrade_level + 1
                        break
                damage = allied_damage + (turret3_level * 10)
                enemy.health -= damage
                aliado.kill()

        if selected_turret:
            selected_turret.selected = True

    #########################
    # SEÇÃO DE DESENHO
    #########################

    world.draw(screen)
    enemy_group.draw(screen)

    for turret in turret_group:
        turret.draw(screen)

    for aliado in allied_group:
        aliado.draw(screen)

    display_data()

    if not game_over:
        if not level_started:
            # Mostra o botão de "Jogar" apenas no primeiro nível
            if first_level:
                if begin_button.draw(screen):
                    level_started = True
                    first_level = False  # Desativa o botão para os próximos níveis
            else:
                # Pula automaticamente para o próximo nível após completar o nível
                level_started = True
        else:
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 2

            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

            if world.check_level_complete():
                world.money += c.LEVEL_COMPLETE_REWARD
                world.level += 1
                level_started = False
                last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()

        # Botões de compra de torres
        draw_text(str(c.BUY_COST_TORRE1), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))
        if check_tower_limit("torre1"):
            screen.blit(buy_turret1_image_disabled, (c.SCREEN_WIDTH + 30, 120))
        else:
            if turret1_button.draw(screen):
                placing_turrets = "torre1"

        draw_text(str(c.BUY_COST_TORRE2), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
        if check_tower_limit("torre2"):
            screen.blit(buy_turret2_image_disabled, (c.SCREEN_WIDTH + 30, 180))
        else:
            if turret2_button.draw(screen):
                placing_turrets = "torre2"

        draw_text(str(c.BUY_COST_TORRE3), text_font, "grey100", c.SCREEN_WIDTH + 215, 255)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 250))
        if check_tower_limit("torre3"):
            screen.blit(buy_turret3_image_disabled, (c.SCREEN_WIDTH + 30, 240))
        else:
            if turret3_button.draw(screen):
                placing_turrets = "torre3"

        # Botão de cancelar compra
        if placing_turrets:
            cursor_pos = pg.mouse.get_pos()
            cursor_rect = cursor_turret1.get_rect()
            cursor_rect.center = cursor_pos
            # Removida a condição que fazia o botão sumir no painel: if cursor_pos[0] <= c.SCREEN_WIDTH:
            if placing_turrets == "torre1":
                screen.blit(cursor_turret1, cursor_rect)
            elif placing_turrets == "torre2":
                screen.blit(cursor_turret2, cursor_rect)
            elif placing_turrets == "torre3":
                screen.blit(cursor_turret3, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = None

        # Desenha o botão de upgrade e venda apenas se uma torre estiver selecionada
        if selected_turret:
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 380)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 380))
                if upgrade_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST

                        # Reduz o cooldown do aliado a cada upgrade da torre 3
                        if selected_turret.turret_type == "torre3":
                            allied_cooldown = max(1000, allied_cooldown - 500)
                            print(f"Cooldown do aliado reduzido para: {allied_cooldown}ms")

            # Botão de Venda
            if selected_turret.turret_type != "torre3":  # Não mostra o botão de venda na torre 3
                if sell_button.draw(screen):  # Se o botão de vender for pressionado
                    if selected_turret:  # Se uma torre estiver selecionada
                        sell_turret(selected_turret)  # Vende a torre
                        selected_turret = None  # Deseleciona a torre

    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
        if game_outcome == -1:
            draw_text("VOCÊ PERDEU!", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("VOCÊ VENCEU!", large_font, "grey0", 315, 230)

    if game_over:
        if restart_button.draw(screen):
            game_over = False
            game_outcome = 0
            world.health = c.HEALTH
            world.money = c.MONEY
            world.level = 0
            level_started = False
            first_level = True  # Reseta a variavel
            world.reset_level()
            world.spawned_enemies = 0
            last_enemy_spawn = pg.time.get_ticks()
            enemy_group.empty()
            turret_group.empty()
            allied_group.empty()
            turret3_placed = False  # Garante que a torre 3 pode ser colocada novamente
            tower_counts["torre1"] = 0
            tower_counts["torre2"] = 0
            tower_counts["torre3"] = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    if placing_turrets == "torre1":
                        if world.money >= c.BUY_COST_TORRE1:
                            if create_turret(mouse_pos, "torre1"):
                                placing_turrets = None
                    elif placing_turrets == "torre2":
                        if world.money >= c.BUY_COST_TORRE2:
                            if create_turret(mouse_pos, "torre2"):
                                placing_turrets = None
                    elif placing_turrets == "torre3":
                        if world.money >= c.BUY_COST_TORRE3:
                            if create_turret(mouse_pos, "torre3"):
                                placing_turrets = None
                else:
                    selected_turret = select_turret(mouse_pos)

                    # Lógica para o botão de venda
                    if selected_turret:
                        if sell_button.draw(screen):  # Se o botão de vender for pressionado
                            if selected_turret:  # Se uma torre estiver selecionada
                                sell_turret(selected_turret)  # Vende a torre
                                selected_turret = None  # Deseleciona a torre

    pg.display.flip()

pg.quit()
sys.exit()
