import pygame
import os


# Inicializar a tela
screen = pygame.display.set_mode((960, 540), 0)  # Tamanho da tela


# Variaveis constantes globais
fps = 60  # Atualizacao de frames por segundo
ani = 4  # Ciclo de animacao
ani_soco = 5  # Ciclo de animacao do soco
steps = 6  # Pixels a serem andados com cada movimento

true_scroll = [0, 0]  #

class Jogo():

    def __init__(self, player):
        self.player = player # Iniciar player no jogo
        self.grass_img = pygame.image.load(os.path.join('images', 'chao_dna_fundo.png'))  # Pegar imagem da grama
        # (DEIXEI SEPARADO MESMO SENDO IGUAL PORQUE ACHO QUE A GENTE PODE FAZER UM BLOCO DIFERENTE QUE FICA POR CIMA DO CHAO)
        self.dirt_img = pygame.image.load(os.path.join('images', 'chao_dna_fundo.png'))  # Pegar imagem da terra
        self.grass_img = pygame.transform.scale(self.grass_img, (50, 25))  # Redimensionar imagem para 30x30
        self.dirt_img = pygame.transform.scale(self.dirt_img, (50, 25))  # Redimensionar imagem para 30x30

    # Escolher qual acao do sprite
    def update(self, action, clock):
        if (action == "andar"):
            player.update_andar()  # Atualizar o frame e posição do player
            self.gravidade()
        if (action == "soco"):
            player.update_soco(clock)  # Atualizar o frame do sprite do soco
        return action

    def load_map(self):  # Carregar o mapa com
        self.arquivo = open('map.txt', 'r')  # Abrir o arquivo map para leitura
        self.data = self.arquivo.read()  # data = conteúdo do arquivo
        self.arquivo.close()  # Fechar o arquivo
        self.data = self.data.split('\n')  # Separar data pelas linhas
        self.mapa = []
        for linha in self.data:  # Pesquisar em data as linhas
            self.mapa.append(list(linha))  # Adicionar as linhas ao mapa
        return self.mapa

    def movimento_camera(self, true_scroll):

        self.true_scroll = true_scroll

        self.true_scroll[0] += (player.rect.x - self.true_scroll[0] - 250)  # Movimento de camera em x travado no player
        self.true_scroll[1] = -268  # Movimento em y travado fixo em -268
        self.true_scroll[0] = int(self.true_scroll[0])  # Movimento da camera = parte inteira apenas

        self.blocos_rects = []  # Lista para blocos sem conteudo
        self.y = 0
        for linha in self.mapa:  # Para linha em mapa
            self.x = 0  # Valor para bloco
            for bloco in linha:  # Para bloco em linha
                if bloco == '1':
                    screen.blit(self.dirt_img, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '2':
                    screen.blit(self.grass_img, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco != '0':
                    self.blocos_rects.append(pygame.Rect(self.x * 50, self.y * 25, 50, 25))  # Adicionar bloco sem conteudo na lista
                self.x += 1  # Bloco + 1
            self.y += 1  # Linha + 1

        return self.true_scroll

    def colisao_chao(self, rect):
        self.rect_teste = rect  # Retangulo para o teste de colisoes
        self.lista_colisao = []  # Lista com colisoes
        for bloco in self.blocos_rects:  # Pesquisa por bloco em todos blocos
            if self.rect_teste.colliderect(bloco):  # Se o bloco colide com retangulo teste
                self.lista_colisao.append(bloco)  # Adiciona na lista de colisoes
        return self.lista_colisao

    def gravidade(self):
        player.altura += 1  # Gravidade puxando +1 para baixo
        if player.altura > 10:  # Máximo da gravidade
            player.altura = 10

        if player.tipo_colisao['baixo'] == True:  # Se colisao por baixo = true
            player.air_timer = 0  # Tempo no ar = 0
            player.altura = 0  # Gravidade nao puxa alem do bloco
        else:
            player.air_timer += 1  # Se nao esta no chao tempo no ar +1


class Sapinho(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.image = pygame.image.load(os.path.join('images', 'sapinho' + '.png'))
        self.image = pygame.transform.scale(self.image, (108, 80))  # Redimensionar imagem para 108x80

        self.rect = self.image.get_rect()  # Retangulo da hit box da imagem inicial a ser pintada
        self.rect.x = 500  # Posicao inicial do player em X
        self.rect.y = 200  # Posicao inicial do player em Y


class Player(pygame.sprite.Sprite):

    # Inicializacao do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.movex = 0  # Valor a ser andado em x por loop da main
        self.movey = 0  # Valor a ser movido em y por loop em main
        self.frame = 0  # Numero utilizado para cada frame
        self.air_timer = 0  # Tempo no ar
        self.altura = 0  # Valor da gravidade a ser movido

        self.imagens = []  # Lista para guardar imagens do sprite andar
        for i in range(1, 9):  # Pegar 8 imagens
            self.img = pygame.image.load(os.path.join('images', 'GB' + str(i) + '.png'))  # Pegar frames andar+i da pasta images
            self.img = pygame.transform.scale(self.img, (60, 60))  # Redimensionar imagem para 120x120
            self.imagens.append(self.img)  # Adicionar imagens na lista para o sprite andar

        self.socos = []  # Lista para guardar imagens do sprite soco
        for i in range(1, 4):  # Pegar 3 imagens do soco
            self.img = pygame.image.load(os.path.join('images', 'soco' + str(i) + '.png'))  # Pegar frames soco+i da pasta images
            self.img = pygame.transform.scale(self.img, (60, 60))  # Redimensionar imagem para 120x120
            self.socos.append(self.img)  # Adicionar imagens na lista para o sprite socar

        self.image = self.imagens[0]  # Imagem inicial a ser pintada eh a andar de indice 0
        self.rect = self.image.get_rect()  # Retangulo da hit box da imagem inicial a ser pintada

        self.rect.x = 0  # Posicao inicial do player em X
        self.rect.y = 140  # Posicao inicial do player em Y

    # Controlar o movimento do player
    def control(self, x):
        self.movex += x  # Atualizar a distancia a se mover do player em X

    # Atualizar o frame do sprite do soco
    def update_soco(self, clock):
        self.frame = 0
        while (self.frame < (2 * ani_soco) + 4):
            self.image = self.socos[self.frame // ani_soco]
            self.frame += 1
            classeFundo.desenhar_fundo()  # Pintar o fundo
            self.int_scroll = jogo.movimento_camera(true_scroll)  # Pegar scroll da camera
            screen.blit(self.image, (self.rect.x - int_scroll[0], self.rect.y - int_scroll[1]))  # Printar com movimento da camera
            pygame.display.update(screen.get_rect())  # Atuzalizar tela
            clock.tick(fps)
        self.frame = 0
        self.image = player.imagens[0]

        return action

    # Atualizar o frame e posição do player
    def update_andar(self):
        self.tipo_colisao = {'cima': False, 'baixo': False, 'direita': False, 'esquerda': False}  # Tipo de colisao

        self.rect.x += self.movex  # Atualizar o posicao do retangulo do player(rect) em X

        # Evitar que o player saia da tela
        if self.rect.left <= -150:  # Evita na esquerda (Aberto para testar morte pela queda)
            self.rect.left = -150
        if self.rect.right >= 112 * 50:  # Evita sair na direita
            self.rect.right = 112 * 50
        if self.rect.top >= 280:  # Morte por queda
            self.rect.x = 0
            self.rect.y = 140

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movex > 0:
                self.rect.right = tile.left
                # self.tipo_colisao['direita'] = True
            elif self.movex < 0:
                self.rect.left = tile.right
                # self.tipo_colisao['esquerda'] = True

        self.movey += self.altura
        self.rect.y += self.movey   # Atualizar o posicao do retangulo do player(rect) em Y

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movey > 0:
                self.rect.bottom = tile.top
                self.tipo_colisao['baixo'] = True
            elif self.movey < 0:
                self.rect.top = tile.bottom
                # self.tipo_colisao['cima'] = True

        # Indo para esquerda
        if self.movex < 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + (ani-1)
            if self.frame > (7*ani) + (ani-1): # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

        # Indo para direita
        if self.movex > 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + (ani-1)
            if self.frame > (7*ani) + (ani-1):  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[self.frame//ani]  # Pega o frame no grupo com as imagens

        self.movey = 0  # Movey = 0 apos ja ter atualizado o movimento
        pygame.display.update(self.image.get_rect())  # Atualizar tela

    # Processar os movimentos
    def processar_movimentos(self, eventos, action):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    action = "andar"
                    player.control(steps)  # Ira mover steps para direita
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    action = "andar"
                    player.control(-steps)  # Ira mover steps para esquerda
                if e.key == pygame.K_UP or e.key == ord('w'):
                    action = "andar"
                    if self.air_timer < 2:  # Se o tempo no ar for menor do que 2
                        self.altura = -20
                if e.key == pygame.K_SPACE:
                    action = "soco"
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    player.control(-steps)  # Ira mover -steps para direita (parando o personagem)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    player.control(steps)  # Ira mover -steps para esquerda (parando o personagem)
                if e.key == pygame.K_SPACE:
                    action = "andar"  # Apos pular acao volta a ser andar

        return action

class Fundo():

    # Inicializacao do Fundo
    def __init__(self):
        self.fundo = pygame.image.load(os.path.join('images', 'fundo_red.png')).convert()  # Fundo pela imagem stage da pasta images
        self.fundo = pygame.transform.scale(self.fundo, (960, 540))
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
    #sapinho = Sapinho()  # Cria sapinho
    jogo = Jogo(player)  # Cria o jogo

    player_list = pygame.sprite.Group()  # Grupo para os sprites
    #sapinho_list = pygame.sprite.Group()
    #sapinho_list.add(sapinho)
    player_list.add(player)  # Adicionar player ao grupo

    jogo.load_map()  # Carregar mapa
    true_scroll = [0, 0]  #  Valor inicial do scroll da camera

    action = "andar"  # Ação atual

    while True:
        # Pintar a tela
        classeFundo.desenhar_fundo()  # Pintar o fundo
        int_scroll = jogo.movimento_camera(true_scroll)  # Movimentar a tela de acrodo com o movimento do personagem
        screen.blit(player.image, (player.rect.x - int_scroll[0], player.rect.y - int_scroll[1]))  # Atualizar a tela com o movimento da camera

        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
        action = player.processar_movimentos(eventos, action)  # Processar movimentos

        # Update do player
        action = jogo.update(action, clock)  # Escolher acao
