import pygame
import sys
import os

'''
Variables
'''

#inicializar a tela
screen = pygame.display.set_mode((1280,720), 0)  # Tamanho da tela
VERM = (205,92,92)

fps = 40  # Atualizacao de frames por segundo
ani = 3  # Ciclos de animacao

ALPHA = (0,0,0)  # Alpha da imagem

'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0  #
        self.movey = 0  #
        self.frame = 0  # Numero utilizado para cada frame
        self.imagens = []  # Lista para guardar imagens do sprite
        for i in range(1, 9): # Pegar 8 imagens
            img = pygame.image.load(os.path.join('images', 'GB' + str(i) + '.png')).convert()  # Pegar frames GB+i da pasta images
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.imagens.append(img)
            self.image = self.imagens[0]
            self.rect = self.image.get_rect()

    # Controlar o movimento do player
    def control(self, x, y):

        self.movex += x  # Atualizar a distancia a se mover do player em X
        self.movey += y  # Atualizar a distancia a se mover do player em Y


    # Atualizar o frame e posição do player
    def update(self):

        self.rect.x = self.rect.x + self.movex  # Atualizar o posicao do retangulo do player(rect) em X
        self.rect.y = self.rect.y + self.movey  # Atualizar o posicao do retangulo do player(rect) em Y

        # Indo para esquerda
        if self.movex < 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani)+2
            if self.frame > (7*ani)+2: # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

        # Indo para direita
        if self.movex > 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani)+2
            if self.frame > (7*ani)+2:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

    def processar_movimentos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(-steps, 0)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(-steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(steps, 0)


'''
Main Loop
'''

if __name__ == "__main__":

    #fundo = pygame.image.load(os.path.join('images', 'stage.png')) # Fundo pela imagem stage da pasta images
    ret_fundo = screen.get_rect()
    clock = pygame.time.Clock()
    pygame.init()

    player = Player()  # Cria player
    player.rect.x = 500  # Posicao player no x
    player.rect.y = 100  # Posicao player no y
    player_list = pygame.sprite.Group()  # Grupo para os sprites
    player_list.add(player)  # Adicionar player ao grupo
    steps = 8

    pygame.init()

    while True:
        # Update do player
        player.update()

        # Pintar a tela
        screen.fill(VERM)  # Preencher fundo por uma unica cor
        #screen.blit(fundo, ret_fundo)  # Fundo por imagem
        player_list.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
        player.processar_movimentos(eventos)