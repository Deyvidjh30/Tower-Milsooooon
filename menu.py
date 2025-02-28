import pygame as pg

def main_menu(screen):
    # Carrega a imagem de fundo
    background_image = pg.image.load("tela inicial/menu_numero1.jpg")
    background_image = pg.transform.scale(background_image, (720, 720))

    # Carrega a imagem do botão "Play"
    play_button_image = pg.image.load("tela inicial/botton de play.png")
    play_button_rect = play_button_image.get_rect(center=(720 // 2, 720 // 2 + 200))

    menu_running = True  # Variável para controlar o loop do menu

    while menu_running:
        # Desenha a imagem de fundo
        screen.blit(background_image, (0, 0))

        # Desenha a imagem do botão "Play"
        screen.blit(play_button_image, play_button_rect.topleft)

        # Atualiza a tela
        pg.display.flip()

        # Verifica eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):  # Verifica clique na imagem do botão
                    menu_running = False  # Sai do loop do menu
                    return "start"  # Inicia o jogo

# Inicializa o Pygame e cria a tela
pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Tower Milsons Defence")

# Chama o menu apenas uma vez e armazena o resultado
result = main_menu(screen)

# Se "start" for retornado, inicia o jogo
if result == "start":
    print("Iniciando o jogo...")  # Aqui você coloca a lógica para iniciar o jogo
elif result == "quit":
    print("Fechando o jogo...")

pg.quit()
