import pygame
import os


# Inicializar a tela
screen = pygame.display.set_mode((960,540), 0)  # Tamanho da tela


# Variaveis constantes globais
fps = 60  # Atualizacao de frames por segundo
ani = 5  # Ciclo de animacao
ani_soco = 5  # Ciclo de animacao do soco
steps = 5  # Pixels a serem andados com cada movimento

# Cores
PRETO = (0,0,0)


class Player(pygame.sprite.Sprite):

    # Inicializacao do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0  #
        self.movey = 0  #
        self.frame = 0  # Numero utilizado para cada frame

        self.imagens = []  # Lista para guardar imagens do sprite andar
        for i in range(1, 9):  # Pegar 8 imagens
            self.img = pygame.image.load(os.path.join('images', 'GB' + str(i) + '.png')).convert()  # Pegar frames andar+i da pasta images
            self.img.convert_alpha()  # Converter o alpha
            self.img.set_colorkey(PRETO)  # Setar cor para ficar transparente
            self.img = pygame.transform.scale(self.img, (120, 120))  # Redimensionar imagem para 150x150
            self.imagens.append(self.img)  # Adicionar imagens na lista para o sprite andar

        self.socos = []  # Lista para guardar imagens do sprite soco
        for i in range(1, 4):  # Pegar 3 imagens do soco
            self.img = pygame.image.load(os.path.join('images', 'soco' + str(i) + '.png')).convert()  # Pegar frames soco+i da pasta images
            self.img.convert_alpha()  # Converter o alpha
            self.img.set_colorkey(PRETO)  # Setar alpha
            self.img = pygame.transform.scale(self.img, (120, 120))  # Redimensionar imagem para 150x150
            self.socos.append(self.img)  # Adicionar imagens na lista para o sprite socar

        self.image = self.imagens[0]  # Imagem inicial a ser pintada eh a andar de indice 0
        self.rect = self.image.get_rect()  # Retangulo da hit box da imagem inicial a ser pintada

        self.rect.x = 0  # Posicao inicial do player em X
        self.rect.y = 0  # Posicao inicial do player em Y

    # Controlar o movimento do player
    def control(self, x, y):

        self.movex += x  # Atualizar a distancia a se mover do player em X
        self.movey += y  # Atualizar a distancia a se mover do player em Y

    # Escolher qual acao do sprite
    def update(self, action, player_list, clock):
        if (action == "andar"):
            self.update_andar()
        if (action == "soco"):
            self.update_soco(player_list, clock)
        return action

    # Atualizar o frame do sprite do soco
    def update_soco(self, player_list, clock):
        self.frame = 0
        while (self.frame < (2 * ani_soco) + 4):
            self.image = self.socos[self.frame // ani_soco]
            self.frame += 1
            classeFundo.desenhar_fundo()  # Pintar o fundo
            player_list.draw(screen)  # Pintar player
            pygame.display.update(self.image.get_rect())  # Atualizar tela
            clock.tick(fps)
        self.frame = 0
        self.image = player.imagens[0]

        return action

    # Atualizar o frame e posição do player
    def update_andar(self):

        self.rect.x = self.rect.x + self.movex  # Atualizar o posicao do retangulo do player(rect) em X
        self.rect.y = self.rect.y + self.movey  # Atualizar o posicao do retangulo do player(rect) em Y

        # Indo para esquerda
        if self.movex < 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + 3
            if self.frame > (7*ani) + 3: # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

        # Indo para direita
        if self.movex > 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + 3
            if self.frame > (7*ani) + 3:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

        # Indo para cima
        if self.movey < 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7 * ani) + 3
            if self.frame > (7 * ani) + 3:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame // ani]  # Pega o frame no grupo com as imagens

        # Indo para baixo
        if self.movey > 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7 * ani) + 3
            if self.frame > (7 * ani) + 3:  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame // ani]  # Pega o frame no grupo com as imagens

        pygame.display.update(self.image.get_rect())  # Atualizar tela

    # Processar os movimentos
    def processar_movimentos(self, eventos, action):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    action = "andar"
                    player.control(steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    action = "andar"
                    player.control(-steps, 0)
                if e.key == pygame.K_UP or e.key == ord('w'):
                    action = "andar"
                    player.control(0, -steps)
                if e.key == pygame.K_DOWN or e.key == ord('s'):
                    action = "andar"
                    player.control(0, steps)
                if e.key == pygame.K_SPACE:
                    action = "soco"
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(-steps, 0)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(steps, 0)
                if e.key == pygame.K_UP or e.key == ord('w'):
                    player.control(0, steps)
                if e.key == pygame.K_DOWN or e.key == ord('s'):
                    player.control(0, -steps)
                if e.key == pygame.K_SPACE:
                    action = "andar"

        return action

class Fundo():

    # Inicializacao do Fundo
    def __init__(self):
        self.fundo = pygame.image.load(os.path.join('images', 'stage.png')).convert()  # Fundo pela imagem stage da pasta images
        self.fundoX = 0  # Inicio do ciclo do primeiro fundo
        self.fundoX2 = self.fundo.get_width()  # Inicio do ciclo do segundo fundo

    def desenhar_fundo(self):
        self.fundoX -= 3  # Velocidade do fundo 1
        self.fundoX2 -= 3  # Velocidade do fundo 2

        if self.fundoX < self.fundo.get_width() * -1:  # Se o fundo chegar na esquerda recomeçar na direita
            self.fundoX = self.fundo.get_width()

        if self.fundoX2 < self.fundo.get_width() * -1:  # Se o fundo 2 chegar na esquerda recomeçar na direita
            self.fundoX2 = self.fundo.get_width()

        screen.blit(self.fundo, (self.fundoX, 0))  # Desenha o fundo 1
        screen.blit(self.fundo, (self.fundoX2, 0))  # Desenha o fundo 2

# Main
if __name__ == "__main__":

    pygame.init()  # Iniciar o pygame

    clock = pygame.time.Clock()  # Objeto de tempo
    classeFundo = Fundo()  #Cria o fundo
    player = Player()  # Cria player

    player_list = pygame.sprite.Group()  # Grupo para os sprites
    player_list.add(player)  # Adicionar player ao grupo

    action = "andar"  # Ação atual

    while True:
        # Pintar a tela
        classeFundo.desenhar_fundo()  # Pintar o fundo
        player_list.draw(screen)  # Pintar player
        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
        action = player.processar_movimentos(eventos, action)  # Processar movimentos

        # Update do player
        action = player.update(action, player_list, clock)  # Escolher acao
