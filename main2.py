import pygame
import os


#inicializar a tela
screen = pygame.display.set_mode((1280,720), 0)  # Tamanho da tela

VERMELHO = (205,92,92)

fps = 40  # Atualizacao de frames por segundo
ani = 3  # Ciclo de animacao

ALPHA = (0,0,0)  # Alpha da imagem


class Player(pygame.sprite.Sprite):

    # Inicializacao do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0  #
        self.movey = 0  #
        self.frame = 0  # Numero utilizado para cada frame
        self.imagens = []  # Lista para guardar imagens do sprite
        for i in range(1, 9): # Pegar 8 imagens
            img = pygame.image.load(os.path.join('images', 'GB' + str(i) + '.png')).convert()  # Pegar frames GB+i da pasta images
            img.convert_alpha()  # Converter o alpha
            img.set_colorkey(ALPHA)  # Setar alpha
            img = pygame.transform.scale(img, (250, 250))  # Redimensionar imagem
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

        # Indo para cima
        if self.movey < 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7 * ani) + 2
            if self.frame > (7 * ani) + 2:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame // ani]  # Pega o frame no grupo com as imagens

        # Indo para baixo
        if self.movey > 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7 * ani) + 2
            if self.frame > (7 * ani) + 2:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame // ani]  # Pega o frame no grupo com as imagens

    # Processar os movimentos
    def processar_movimentos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(-steps, 0)
                if e.key == pygame.K_UP or e.key == ord('w'):
                    player.control(0, -steps)
                if e.key == pygame.K_DOWN or e.key == ord('s'):
                    player.control(0, steps)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(-steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(steps, 0)
                if e.key == pygame.K_UP or e.key == ord('w'):
                    player.control(0, steps)
                if e.key == pygame.K_DOWN or e.key == ord('s'):
                    player.control(0, -steps)

# Main
if __name__ == "__main__":

    #fundo = pygame.image.load(os.path.join('images', 'stage.png')) # Fundo pela imagem stage da pasta images
    ret_fundo = screen.get_rect()
    clock = pygame.time.Clock()
    pygame.init()

    player = Player()  # Cria player
    player.rect.x = 0  # Posicao player no x
    player.rect.y = 0  # Posicao player no y
    player_list = pygame.sprite.Group()  # Grupo para os sprites
    player_list.add(player)  # Adicionar player ao grupo
    steps = 6

    pygame.init()

    while True:
        # Update do player
        player.update()

        # Pintar a tela
        screen.fill(VERMELHO)  # Preencher fundo por uma unica cor
        #screen.blit(fundo, ret_fundo)  # Fundo por imagem
        player_list.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
        player.processar_movimentos(eventos)  # Processar movimentos