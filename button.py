import pygame as pg

class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image  # Imagem do botÃ£o
        self.rect = self.image.get_rect()  # RetÃ¢ngulo da imagem
        self.rect.topleft = (x, y)  # PosiÃ§Ã£o do botÃ£o
        self.clicked = False  # Estado de clique
        self.single_click = single_click  # Se o botÃ£o Ã© de clique Ãºnico

    def draw(self, surface):
        action = False  # AÃ§Ã£o a ser retornada (se o botÃ£o foi clicado)
        # ObtÃ©m a posiÃ§Ã£o do mouse
        pos = pg.mouse.get_pos()
        
        # Verifica se o mouse estÃ¡ sobre o botÃ£o e se foi clicado
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True  # O botÃ£o foi clicado
                # Se o botÃ£o for de clique Ãºnico, define clicked como True
                if self.single_click:
                    self.clicked = True

        # Reseta o estado de clique quando o botÃ£o do mouse Ã© solto
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Desenha o botÃ£o na tela
        surface.blit(self.image, self.rect)

        return action  # Retorna se o botÃ£o foi clicado
    