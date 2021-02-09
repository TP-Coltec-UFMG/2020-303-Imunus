import pygame
import os


# Inicializar a tela
screen = pygame.display.set_mode((960, 540), 0)  # Tamanho da tela
VERMELHO = (89, 3, 3)  # Cor do fundo

# Variaveis constantes globais
fps = 100  # Atualizacao de frames por segundo
ani = 6  # Ciclo de animacao
#ani_soco = 5  # Ciclo de animacao do soco
steps = 5  # Pixels a serem andados com cada movimento

true_scroll = [0, 0]  #

class Jogo():

    def __init__(self, player):
        self.player = player # Iniciar player no jogo
        self.img_andar = pygame.image.load(os.path.join('images', 'andar.png'))  # Pegar imagem da placa de andar
        self.img_pular = pygame.image.load(os.path.join('images', 'pular.png'))  # Pegar imagem da placa de pular
        self.img_socar = pygame.image.load(os.path.join('images', 'socar.png'))  # Pegar imagem da placa de socar
        self.img_dna_chao = pygame.image.load(os.path.join('images', 'chao_dna_fundo.png'))  # Pegar imagem do chao
        self.img_andar = pygame.transform.scale(self.img_andar, (320, 180))  # Redimensionar imagem para 320x180
        self.img_pular = pygame.transform.scale(self.img_pular, (320, 180))  # Redimensionar imagem para 320x180
        self.img_socar = pygame.transform.scale(self.img_socar, (320, 180))  # Redimensionar imagem para 320x180
        self.img_dna_chao = pygame.transform.scale(self.img_dna_chao, (50, 25))  # Redimensionar imagem para 30x30

        # Carregar o mapa do jogo
        self.arquivo = open('map.txt', 'r')  # Abrir o arquivo map para leitura
        self.data = self.arquivo.read()  # data = conteúdo do arquivo
        self.arquivo.close()  # Fechar o arquivo
        self.data = self.data.split('\n')  # Separar data pelas linhas
        self.mapa = []
        for linha in self.data:  # Pesquisar em data as linhas
            self.mapa.append(list(linha))  # Adicionar as linhas ao mapa

    # Escolher qual acao do sprite
    def update(self, action, clock):
        if sapo.estado == True:
            sapo.update()
        if action == "andar":
            player.update_andar()  # Atualizar o frame e posição do player
            player.colisao_inimigo()
            self.gravidade()
        if action == "soco":
            player.update_soco(clock) # Atualizar o frame do sprite do soco
            player.colisao_inimigo()
        return action

    def movimento_camera(self, true_scroll):

        self.true_scroll = true_scroll
        self.true_scroll[0] += (player.rect.x - self.true_scroll[0] - 250)  # Movimento de camera em x travado no player
        self.true_scroll[1] = -screen.get_height() + (25 * len(self.data))  # Movimento em y travado fixo em -268
        self.true_scroll[0] = int(self.true_scroll[0])  # Movimento da camera = parte inteira apenas

        self.blocos_rects = []  # Lista para blocos sem conteudo
        self.y = 0
        for linha in self.mapa:  # Para linha em mapa
            self.x = 0  # Valor para bloco
            for bloco in linha:  # Para bloco em linha
                if bloco == '1':
                    screen.blit(self.img_dna_chao, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '2':
                    screen.blit(self.img_andar, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '3':
                    screen.blit(self.img_pular, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '4':
                    screen.blit(self.img_socar, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
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


class Player(pygame.sprite.Sprite):

    # Inicializacao do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 3
        self.movex = 0  # Valor a ser andado em x por loop da main
        self.movey = 0  # Valor a ser movido em y por loop em main
        self.frame = 0  # Numero utilizado para cada frame
        self.air_timer = 0  # Tempo no ar
        self.altura = 0  # Valor da gravidade a ser movido

        self.imagens = []  # Lista para guardar imagens do sprite andar
        for i in range(1, 9):  # Pegar 8 imagens
            self.img = pygame.image.load(os.path.join('images', 'GB' + str(i) + '.png'))  # Pegar frames andar+i da pasta images
            self.img = pygame.transform.scale(self.img, (100, 100))  # Redimensionar imagem para 120x120
            self.imagens.append(self.img)  # Adicionar imagens na lista para o sprite andar

        self.socos = []  # Lista para guardar imagens do sprite soco
        for i in range(1, 4):  # Pegar 3 imagens do soco
            self.img = pygame.image.load(
                os.path.join('images', 'soco' + str(i) + '.png'))  # Pegar frames soco+i da pasta images
            self.img = pygame.transform.scale(self.img, (100, 100))  # Redimensionar imagem para 120x120
            self.socos.append(self.img)  # Adicionar imagens na lista para o sprite socar

        self.at = 0  # Volta pra posição inicial

        self.image = self.imagens[0]  # Imagem inicial a ser pintada eh a andar de indice 0
        self.rect = self.image.get_rect()  # Retangulo da hit box da imagem inicial a ser pintada

        self.rect.x = 400  # Posicao inicial do player em X
        self.rect.y = 140  # Posicao inicial do player em Y

    # Controlar o movimento do player
    def control(self, x):
        self.movex += x  # Atualizar a distancia a se mover do player em X

    #colisao inimigo
    def colisao_inimigo(self):
        if sapo.estado:
            self.teste_colisao = pygame.sprite.collide_mask(self, sapo)  # Variavel que verifica se colisao é true

            # Teste colisao do soco
            if action == 'soco':  # Se a imagem do soco colidir
                if self.teste_colisao:
                    print('gameover')
                    sapo.kill()

            else:  # Se qualquer outra imagem colidir
                if self.teste_colisao:
                    self.vida = self.vida - 1  # Tira uma vida do player
                    if self.movex > 0:  # Se estiver indo para direita
                        self.rect.x -= 100
                    if self.movex < 0:  # Se estiver indo para esquerda
                        self.rect.x += 100
                    if self.altura > 0:  # Se estiver indo para baixo
                        self.rect.x -= 100
                    if self.vida == 0:
                        print('Morreu')  # pra gente ver q perdeu tres vidas pq nn sei oq vai acontecer qnd ele morre

    # Atualizar o frame do sprite do soco

    def update_soco(self, action):
        self.action = action
        self.at = self.at + 0.17 #basicamente o seu ani, pega o frame e deixa na velocidade do fps
        if self.at >= len(self.socos):  # testa o soco com a variavel atual
            self.at = 0 #volta pra posição inicial
            self.image = self.imagens[0]
            self.action = "andar"  # sew nn tiver socando passa a imagem soco1.png o tempo td( seria a imagem 1 da lista anda)
        self.image = self.socos[int(self.at)]

        self.rect.x += self.movex  # Atualizar o posicao do retangulo do player(rect) em X

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movex > 0:
                self.rect.right = tile.left
                self.tipo_colisao['direita'] = True
            elif self.movex < 0:
                self.rect.left = tile.right
                self.tipo_colisao['esquerda'] = True

        self.rect.y += self.movey  # Atualizar o posicao do retangulo do player(rect) em Y

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movey > 0:
                self.rect.bottom = tile.top
                self.tipo_colisao['baixo'] = True
            elif self.movey < 0:
                self.rect.top = tile.bottom
                self.tipo_colisao['cima'] = True

        return self.action

    # Atualizar o frame e posição do player
    def update_andar(self):
        self.tipo_colisao = {'cima': False, 'baixo': False, 'direita': False, 'esquerda': False}  # Tipo de colisao

        self.rect.x += self.movex  # Atualizar o posicao do retangulo do player(rect) em X

        # Evitar que o player saia da tela
        if self.rect.left <= 250:  # Evita na esquerda
            self.rect.left = 250
        if self.rect.right >= 112 * 50:  # Evita sair na direita
            self.rect.right = 112 * 50
        if self.rect.top >= (25 * len(jogo.data)):  # Morte por queda
            self.rect.x = 0
            self.rect.y = 140

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movex > 0:
                self.rect.right = tile.left
                self.tipo_colisao['direita'] = True
            elif self.movex < 0:
                self.rect.left = tile.right
                self.tipo_colisao['esquerda'] = True

        self.movey += self.altura
        self.rect.y += self.movey   # Atualizar o posicao do retangulo do player(rect) em Y

        self.lista_colisao = jogo.colisao_chao(player.rect)
        for tile in self.lista_colisao:
            if self.movey > 0:
                self.rect.bottom = tile.top
                self.tipo_colisao['baixo'] = True
            elif self.movey < 0:
                self.rect.top = tile.bottom
                self.tipo_colisao['cima'] = True

        # Indo para esquerda
        if self.movex < 0:
            self.frame -= 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + (ani-1)
            if self.frame > (7*ani) + (ani-1): # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[int(self.frame//ani)]  # Pega o frame no grupo com as imagens

        # Indo para direita
        if self.movex > 0:
            self.frame += 1
            if self.frame < 0:  # Se o ciclo acabar para baixo (0) o indice volta ao maior frame (7)
                self.frame = (7*ani) + (ani-1)
            if self.frame > (7*ani) + (ani-1):  # Se o ciclo acabar para cima (7) o indice volta ao menor frame (0)
                self.frame = 0
            self.image = self.imagens[int(self.frame//ani)]  # Pega o frame no grupo com as imagens

        self.movey = 0  # Movey = 0 apos ja ter atualizado o movimento

        #pygame.display.update(self.image.get_rect())  # Atualizar tela

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
                    self.image = self.imagens[0]

        return action


class Sapo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.estado = True  # Estado True = vivo, False = morto
        self.frame = 0  # Frame atual do sapo

        self.imgs_sapo = []  # Lista para guardar imagens do sprite sapo
        for i in range(1, 6):  # Pegar 5 imagens
            self.img = pygame.image.load(os.path.join('images', 'sapinho' + str(i) + '.png'))  # Pegar frames sapinho+i da pasta images
            self.img = pygame.transform.scale(self.img, (80, 80))  # Redimensionar imagem para 60x60
            self.imgs_sapo.append(self.img)  # Adicionar imagens na lista para o sprite do sapo

        self.image = self.imgs_sapo[0]
        self.rect = self.image.get_rect()  # Pegar rect do sapo
        self.rect.x = 2625  # Posicao inicial do sapo em X
        self.rect.y = 270  # Posicao inicial do sapo em Y

    def kill(self):
        self.estado = False
        for i in self.imgs_sapo:  # Pegar 5 imagens
            self.imgs_sapo.remove(i)

        #pygame.sprite.Sprite.kill(self)
        #self.die_sound.play()

    def update(self):
        if self.estado:
            self.frame = self.frame + 0.1
            if self.frame >= len(self.imgs_sapo):
                self.frame = 0
            self.image = self.imgs_sapo[int(self.frame)]



# Main
if __name__ == "__main__":

    pygame.init()  # Iniciar o pygame

    clock = pygame.time.Clock()  # Objeto de tempo
    player = Player()  # Cria player
    sapo = Sapo()
    jogo = Jogo(player)  # Cria o jogo

    true_scroll = [0, 0]  #  Valor inicial do scroll da camera

    action = "andar"  # Ação atual


    while True:
        # Pintar a tela
        screen.fill(VERMELHO)  # Pintar o fundo
        int_scroll = jogo.movimento_camera(true_scroll)  # Movimentar a tela de acrodo com o movimento do personagem
        if sapo.estado:
            screen.blit(sapo.image, (sapo.rect.x - int_scroll[0], sapo.rect.y - int_scroll[1]))
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
