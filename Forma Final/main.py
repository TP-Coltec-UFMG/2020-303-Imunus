import pygame
import os


# Inicializar a tela
screen = pygame.display.set_mode((960, 540), 0)  # Tamanho da tela
FUNDO = (89, 3, 3)  # Cor do fundo
AZUL = (133, 131, 131)
VERDE = (0 , 80, 0)
ROSA = (15, 15, 15)

# Variaveis constantes globais
fps = 100  # Atualizacao de frames por segundo
ani = 6  # Ciclo de animacao
#ani_soco = 5  # Ciclo de animacao do soco
steps = 5  # Pixels a serem andados com cada movimento


class Jogo():

    def __init__(self):
        self.true_scroll = [0, 0]
        if estado_jogo.menu.daltonismo == "images_comum":
            self.fundo = (89, 3, 3)
        if estado_jogo.menu.daltonismo == "images_deutan":
            self.fundo = (57, 43, 0)
        if estado_jogo.menu.daltonismo == "images_protan":
            self.fundo = (50, 45, 12)
        if estado_jogo.menu.daltonismo == "images_tritan":
            self.fundo = (88, 8, 0)

        self.img_andar = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'andar.png'))  # Pegar imagem da placa de andar
        self.img_pular = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'pular.png'))  # Pegar imagem da placa de pular
        self.img_socar = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'atacar.png'))  # Pegar imagem da placa de socar
        self.img_dna_chao = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'chao_dna_fundo.png'))  # Pegar imagem do chao
        self.img_chao_verm = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'chao_verm.png'))  # Pegar imagem do chao
        self.img_andar = pygame.transform.scale(self.img_andar, (320, 180))  # Redimensionar imagem para 320x180
        self.img_pular = pygame.transform.scale(self.img_pular, (320, 180))  # Redimensionar imagem para 320x180
        self.img_socar = pygame.transform.scale(self.img_socar, (320, 180))  # Redimensionar imagem para 320x180
        self.img_dna_chao = pygame.transform.scale(self.img_dna_chao, (50, 25))  # Redimensionar imagem para 30x30
        self.img_chao_verm = pygame.transform.scale(self.img_chao_verm, (50, 25))  # Redimensionar imagem para 320x180

        # Carregar o mapa do jogo
        self.arquivo = open('map.txt', 'r')  # Abrir o arquivo map para leitura
        self.data = self.arquivo.read()  # data = conteúdo do arquivo
        self.arquivo.close()  # Fechar o arquivo
        self.data = self.data.split('\n')  # Separar data pelas linhas
        self.mapa = []
        for linha in self.data:  # Pesquisar em data as linhas
            self.mapa.append(list(linha))  # Adicionar as linhas ao mapa

        # Carregar o mapa do jogo
        self.arquivo = open('map2.txt', 'r')  # Abrir o arquivo map para leitura
        self.data = self.arquivo.read()  # data = conteúdo do arquivo
        self.arquivo.close()  # Fechar o arquivo
        self.data = self.data.split('\n')  # Separar data pelas linhas
        self.mapa2 = []
        for linha in self.data:  # Pesquisar em data as linhas
            self.mapa2.append(list(linha))  # Adicionar as linhas ao mapa


    # Escolher qual acao do sprite
    def update(self):

        estado_jogo.hud.update()
        for enemy in estado_jogo.inimigos:
            if estado_jogo.screen_rect.colliderect(enemy.rect):
                if enemy.estado == True:
                    enemy.update()

        if estado_jogo.menu.player.action == "andar":
            estado_jogo.menu.player.update_andar()  # Atualizar o frame e posição do player
            for enemy in estado_jogo.inimigos:
                if estado_jogo.screen_rect.colliderect(enemy.rect):
                    estado_jogo.menu.player.colisao_inimigo()
                if estado_jogo.screen_rect.colliderect(enemy.chave.rect):
                    estado_jogo.menu.player.colisao_chave()
            if estado_jogo.screen_rect.colliderect(estado_jogo.porta):
                estado_jogo.menu.player.colisao_porta()
            if estado_jogo.estado_fases == 2 and estado_jogo.inicio_fase == False:
                if estado_jogo.screen_rect.colliderect(estado_jogo.gordura):
                    estado_jogo.menu.player.colisao_gordura()
                if estado_jogo.gordura.laranja.estado:
                    estado_jogo.menu.player.colisao_laranja()
                    estado_jogo.gordura.laranja.update()
                if estado_jogo.gordura.laranja.var_laranja:
                    if estado_jogo.menu.player.tiro.estado:
                        estado_jogo.menu.player.tiro.colisao_tiro()
                        estado_jogo.menu.player.tiro.update()
            self.gravidade()
        if estado_jogo.menu.player.action == "soco":
            estado_jogo.menu.player.update_soco() # Atualizar o frame do sprite do soco
            for enemy in estado_jogo.inimigos:
                if estado_jogo.screen_rect.colliderect(enemy.rect):
                    estado_jogo.menu.player.colisao_inimigo()
                if estado_jogo.screen_rect.colliderect(enemy.chave.rect):
                    estado_jogo.menu.player.colisao_chave()
            if estado_jogo.screen_rect.colliderect(estado_jogo.porta):
                estado_jogo.menu.player.colisao_porta()
            if estado_jogo.estado_fases == 2 and estado_jogo.inicio_fase == False:
                if estado_jogo.screen_rect.colliderect(estado_jogo.gordura):
                    estado_jogo.menu.player.colisao_gordura()
                if estado_jogo.gordura.laranja.estado:
                    estado_jogo.menu.player.colisao_laranja()
                    estado_jogo.gordura.laranja.update()



    def movimento_camera(self):

        self.true_scroll[0] += (estado_jogo.menu.player.rect.x - self.true_scroll[0] - 250)  # Movimento de camera em x travado no player
        self.true_scroll[1] = -screen.get_height() + (25 * (len(self.data)) )  # Movimento em y
        self.true_scroll[0] = int(self.true_scroll[0])  # Movimento da camera = parte inteira apenas

        self.blocos_rects = []  # Lista para blocos sem conteudo
        self.y = 0
        for linha in estado_jogo.mapa_atual:  # Para linha em mapa
            self.x = 0  # Valor para bloco
            for bloco in linha:  # Para bloco em linha
                if bloco == '1':
                    screen.blit(self.img_dna_chao, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '2':
                    screen.blit(self.img_chao_verm, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '3':
                    screen.blit(self.img_andar, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '4':
                    screen.blit(self.img_pular, (self.x * 50 - self.true_scroll[0], self.y * 25 - self.true_scroll[1]))  # Print bloco em relacao ao movimento do player
                if bloco == '5':
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
        estado_jogo.menu.player.altura += 1  # Gravidade puxando +1 para baixo
        if estado_jogo.menu.player.altura > 10:  # Máximo da gravidade
            estado_jogo.menu.player.altura = 10

        if estado_jogo.menu.player.tipo_colisao['baixo'] == True:  # Se colisao por baixo = true
            estado_jogo.menu.player.air_timer = 0  # Tempo no ar = 0
            estado_jogo.menu.player.altura = 0  # Gravidade nao puxa alem do bloco
        else:
            estado_jogo.menu.player.air_timer += 1  # Se nao esta no chao tempo no ar +1


class Player(pygame.sprite.Sprite):

    # Inicializacao do Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 5
        print('Vidas: ' + str(self.vida))
        self.movex = 0  # Valor a ser andado em x por loop da main
        self.movey = 0  # Valor a ser movido em y por loop em main
        self.frame = 0  # Numero utilizado para cada frame
        self.action = "andar"
        self.air_timer = 0  # Tempo no ar
        self.altura = 0  # Valor da gravidade a ser movido

        self.imagens = []  # Lista para guardar imagens do sprite andar
        for i in range(1, 9):  # Pegar 8 imagens
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'GB' + str(i) + '.png'))  # Pegar frames andar+i da pasta images
            print(estado_jogo.menu.daltonismo)
            self.img = pygame.transform.scale(self.img, (100, 100))  # Redimensionar imagem para 120x120
            self.imagens.append(self.img)  # Adicionar imagens na lista para o sprite andar

        self.socos = []  # Lista para guardar imagens do sprite soco
        for i in range(1, 4):  # Pegar 3 imagens do soco
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'soco' + str(i) + '.png'))  # Pegar frames soco+i da pasta images
            self.img = pygame.transform.scale(self.img, (100, 100))  # Redimensionar imagem para 120x120
            self.socos.append(self.img)  # Adicionar imagens na lista para o sprite socar

        self.at = 0  # Volta pra posição inicial

        self.image = self.imagens[0]  # Imagem inicial a ser pintada eh a andar de indice 0
        self.rect = self.image.get_rect()  # Retangulo da hit box da imagem inicial a ser pintada

        self.rect.x = 400  # Posicao inicial do player em X
        self.rect.y = 200  # Posicao inicial do player em Y

    # Controlar o movimento do player
    def control(self, x):
        self.movex += x  # Atualizar a distancia a se mover do player em X

    #colisao inimigo
    def colisao_inimigo(self):
        for enemy in estado_jogo.inimigos:
            if enemy.estado:
                self.teste_colisao = pygame.sprite.collide_mask(self, enemy)  # Variavel que verifica se colisao é true

                # Teste colisao do soco
                if estado_jogo.menu.player.action == 'soco':  # Se a imagem do soco colidir
                    if self.teste_colisao:
                        print('gameover')
                        enemy.kill()

                else:  # Se qualquer outra imagem colidir
                    if self.teste_colisao:
                        self.vida = self.vida - 1  # Tira uma vida do player
                        print('Vidas: ' + str(self.vida))
                        if self.movex > 0:  # Se estiver indo para direita
                            self.rect.x -= 100
                        if self.movex < 0:  # Se estiver indo para esquerda
                            self.rect.x += 100
                        if self.altura > 0:  # Se estiver indo para baixo
                            self.rect.x -= 100
                        if self.vida == 0:
                            print('Morreu')  # pra gente ver q perdeu tres vidas pq nn sei oq vai acontecer qnd ele morre
                        if self.vida <= 0:
                            estado_jogo.historia.update_gameover()

    # Testar colisao com a chave
    def colisao_chave(self):
        for enemy in estado_jogo.inimigos:
            self.teste_colisao_chave = pygame.sprite.collide_mask(self, enemy.chave)
            if enemy.chave.estado:
                if self.teste_colisao_chave:
                    enemy.chave.kill()
                    estado_jogo.porta.Nchaves += 1
                    print("Numero de chaves: " + str(estado_jogo.porta.Nchaves) + "/" + str(estado_jogo.max_chaves))

    # Colisao porta e leo
    def colisao_porta(self):
        self.teste_colisao_porta = pygame.sprite.collide_mask(self, estado_jogo.porta)  # Variavel que verifica se colisao é true
        if estado_jogo.porta.Nchaves == estado_jogo.max_chaves and self.teste_colisao_porta and estado_jogo.porta.estado:
            estado_jogo.porta.update()

    # Testar colisao com a chave
    def colisao_gordura(self):

        if estado_jogo.gordura.estado:
            self.teste_colisao_gordura = pygame.sprite.collide_mask(self,estado_jogo.gordura)  # Variavel que verifica se colisao é true
            if estado_jogo.menu.player.action == 'soco':
                if self.teste_colisao_gordura:
                    estado_jogo.gordura.kill()
            else:
                if self.teste_colisao_gordura:
                    if self.movex > 0:  # Se estiver indo para direita
                        self.rect.x -= 100
                    if self.movex < 0:  # Se estiver indo para esquerda
                        self.rect.x += 100
                    if self.altura > 0:  # Se estiver indo para baixo
                        self.rect.x -= 100

    # Testar colisao com a chave
    def colisao_laranja(self):
        self.teste_colisao_laranja = pygame.sprite.collide_mask(self, estado_jogo.gordura.laranja)
        if estado_jogo.gordura.laranja.estado:
            if self.teste_colisao_laranja:
                estado_jogo.gordura.laranja.kill()
                self.tiro = Tiro()
                estado_jogo.gordura.laranja.var_laranja = True


    # Atualizar o frame do sprite do soco

    def update_soco(self):
        self.at = self.at + 0.17 #basicamente o seu ani, pega o frame e deixa na velocidade do fps
        if self.at >= len(self.socos):  # testa o soco com a variavel atual
            self.at = 0 #volta pra posição inicial
            self.image = self.imagens[0]
            self.action = "andar"  # sew nn tiver socando passa a imagem soco1.png o tempo td( seria a imagem 1 da lista anda)
        self.image = self.socos[int(self.at)]
        if self.movex < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.movex  # Atualizar o posicao do retangulo do player(rect) em X

        self.lista_colisao = estado_jogo.menu.jogo.colisao_chao(estado_jogo.menu.player.rect)
        for tile in self.lista_colisao:
            if self.movex > 0:
                self.rect.right = tile.left
                self.tipo_colisao['direita'] = True
            elif self.movex < 0:
                self.rect.left = tile.right
                self.tipo_colisao['esquerda'] = True

        self.rect.y += self.movey  # Atualizar o posicao do retangulo do player(rect) em Y

        self.lista_colisao = estado_jogo.menu.jogo.colisao_chao(estado_jogo.menu.player.rect)
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

        if self.rect.top >= (25 * len(estado_jogo.menu.jogo.data)):  # Morte por queda
            self.vida = self.vida - 1  # Tira uma vida do player
            self.vida_antes = self.vida
            if estado_jogo.estado_fases == 1:
                print("ANTES")
                estado_jogo.def_fase1()
                print("DEPOIS")
                self.vida = self.vida_antes
            if estado_jogo.estado_fases == 2:
                estado_jogo.def_fase2()
                self.vida = self.vida_antes

        # Fim da fase
        if self.rect.right >= 72 * 50:  # Evita sair na direita
            self.rect.right = 72 * 50


        self.lista_colisao = estado_jogo.menu.jogo.colisao_chao(self.rect)
        for tile in self.lista_colisao:
            if self.movex > 0:
                self.rect.right = tile.left
                self.tipo_colisao['direita'] = True
            elif self.movex < 0:
                self.rect.left = tile.right
                self.tipo_colisao['esquerda'] = True

        self.movey += self.altura
        self.rect.y += self.movey   # Atualizar o posicao do retangulo do player(rect) em Y

        self.lista_colisao = estado_jogo.menu.jogo.colisao_chao(self.rect)
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


    # Processar os movimentos
    def processar_movimentos(self, eventos, action):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    estado_jogo.menu.player.action = "andar"
                    estado_jogo.menu.player.control(steps)  # Ira mover steps para direita
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    estado_jogo.menu.player.action = "andar"
                    estado_jogo.menu.player.control(-steps)  # Ira mover steps para esquerda
                if e.key == pygame.K_UP or e.key == ord('w'):
                    estado_jogo.menu.player.action = "andar"
                    if self.air_timer < 2:  # Se o tempo no ar for menor do que 2
                        self.altura = -20
                if e.key == pygame.K_SPACE:
                    if estado_jogo.estado_fases == 2:
                        if estado_jogo.gordura.laranja.var_laranja == False:
                            estado_jogo.menu.player.action = "soco"
                        if estado_jogo.gordura.laranja.var_laranja == True:
                            estado_jogo.menu.player.action = "andar"
                            self.tiro.tiro_esq = False
                            self.tiro.rect.x = estado_jogo.menu.player.rect.right - 50
                            self.tiro.rect.centery = estado_jogo.menu.player.rect.centery + 20
                            self.tiro.estado = True
                            if self.movex < 0:
                                self.tiro.rect.x = estado_jogo.menu.player.rect.left - 250
                                self.tiro.rect.centery = estado_jogo.menu.player.rect.centery + 20
                                self.tiro.estado = True
                                self.tiro.tiro_esq = True

                    else:
                        estado_jogo.menu.player.action = "soco"
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    estado_jogo.menu.player.control(-steps)  # Ira mover -steps para direita (parando o personagem)
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    estado_jogo.menu.player.control(steps)  # Ira mover -steps para esquerda (parando o personagem)
                if e.key == pygame.K_SPACE:
                    estado_jogo.menu.player.action = "andar"  # Apos pular acao volta a ser andar
                    self.image = self.imagens[0]

        return estado_jogo.menu.player.action


class Sapo(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)

        self.estado = True  # Estado True = vivo, False = morto
        self.frame = 0  # Frame atual do sapo

        self.imgs_sapo = []  # Lista para guardar imagens do sprite sapo
        for i in range(1, 6):  # Pegar 5 imagens
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'sapinho' + str(i) + '.png'))  # Pegar frames sapinho+i da pasta images
            self.img = pygame.transform.scale(self.img, (80, 80))  # Redimensionar imagem para 60x60
            self.imgs_sapo.append(self.img)  # Adicionar imagens na lista para o sprite do sapo


        self.image = self.imgs_sapo[0]
        self.rect = self.image.get_rect()  # Pegar rect do sapo

        self.rect.x = x
        self.rect.y = y
        self.chave = Chave(x, y - 30)

    def kill(self):
        self.estado = False
        self.chave.estado = True

    def update(self):
        if self.estado:
            self.frame = self.frame + 0.1
            if self.frame >= len(self.imgs_sapo):
                self.frame = 0
            self.image = self.imgs_sapo[int(self.frame)]

class Gripe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.estado = True # Estado True = vivo, False = morto
        self.frame = 0  # Frame atual do sapo

        self.img_gripe = []  # Lista para guardar imagens do sprite sapo
        for i in range(1, 5):  # Pegar 5 imagens
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'gripe' + str(i) + '.png'))  # Pegar frames sapinho+i da pasta images
            self.img = pygame.transform.scale(self.img, (130, 130))  # Redimensionar imagem para 60x60
            self.img_gripe.append(self.img)  # Adicionar imagens na lista para o sprite do sapo

        self.image = self.img_gripe[0]
        self.rect = self.image.get_rect()  # Pegar rect do sapo
        self.rect.x = x  # Posicao inicial do sapo em X
        self.init_x = x
        self.rect.y = y  # Posicao inicial do sapo em Y
        self.direcao = 1
        self.chave = Chave(x, y - 30)


    def kill(self):
        self.estado = False
        self.chave.estado = True

    def update(self):
        if self.estado:
            self.frame = self.frame + 0.1
            if self.frame >= len(self.img_gripe):
                self.frame = 0
            self.image = self.img_gripe[int(self.frame)]

            if self.direcao == 1:
                if self.rect.x >= self.init_x + 200:
                    self.direcao = 0
                self.rect.x = self.rect.x + 3
                self.image = pygame.transform.flip(self.image, True, False)
            if self.direcao == 0:
                if self.rect.x <= self.init_x - 200:
                    self.direcao = 1
                self.rect.x = self.rect.x - 3


class Chave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.estado = False  # Estado True = vivo, False = morto

        self.img_chave = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'chave1' + '.png'))  # Pegar frames sapinho+i da pasta images
        self.img_chave = pygame.transform.scale(self.img_chave, (36, 20))  # Redimensionar imagem para 60x60
        self.image = self.img_chave

        self.rect = self.image.get_rect()  # Pegar rect do sapo
        self.rect.x = x # Posicao inicial do sapo em X
        self.rect.y = y + 20  # Posicao inicial do sapo em Y


    def kill(self):
        self.estado = False

class Porta(pygame.sprite.Sprite):

    # Inicializacao Porta
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.Nchaves = 0
        self.estado = True
        self.img_porta = []
        for i in range(1, 5):
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'porta' + str(i) + '.png'))
            self.img = pygame.transform.scale(self.img, (300, 320))
            self.img_porta.append(self.img)

        self.image = self.img_porta[0]
        self.rect = self.image.get_rect()  # Pegar rect
        self.rect.x = x  # Posicao inicial
        self.rect.y = y

        self.frame = 0

    def update(self):
        self.frame = self.frame + 0.1
        self.image = self.img_porta[int(self.frame)]
        if int(self.frame) == 3:
            self.estado = False
            estado_jogo.estado_fases += 1
            estado_jogo.inicio_fase = True
            if estado_jogo.estado_fases > 2:
                estado_jogo.estado_fases = 6
                estado_jogo.historia.update_fim()


class Gordura(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.estado = True  # Estado True = vivo, False = morto

        self.gordura_img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'gordura.png'))  # Pegar imagem da placa de andar
        self.gordura_img = pygame.transform.scale(self.gordura_img, (165, 70))  # Redimensionar imagem para 320x180

        self.image = self.gordura_img
        self.rect = self.image.get_rect()  # Pegar rect da gordura
        self.rect.x = x
        self.rect.y = y
        #self.rect.x = 750 # Posicao inicial do sapo em X
        #self.rect.y = 270  # Posicao inicial do sapo em Y
        self.laranja = Laranja(x + 20, y + 10)

    def kill(self):
        self.estado = False
        self.laranja.estado = True


class Laranja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.estado = False  # Estado True = vivo, False = morto
        self.frame = 0
        self.var_laranja = False
        self.img_laranja = []
        for i in range(1, 9):  # Pegar 5 imagens
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'laranja' + str(i) + '.png'))  # Pegar frames sapinho+i da pasta images
            self.img = pygame.transform.scale(self.img, (50, 50))  # Redimensionar imagem para 60x60
            self.img_laranja.append(self.img)  # Adicionar imagens na lista para o sprite do sapo

        self.image = self.img_laranja[0]
        self.rect = self.image.get_rect()  # Pegar rect do sapo
        self.rect.x = x  # Posicao inicial do sapo em X
        self.rect.y = y  # Posicao inicial do sapo em Y

    def kill(self):
        self.estado = False

    def update(self):
        if self.estado:
            self.frame = self.frame + 0.1
            if self.frame >= len(self.img_laranja):
                self.frame = 0
            self.image = self.img_laranja[int(self.frame)]

#Tiro laranja
class Tiro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.estado = False  # Estado True = vivo, False = morto
        self.tiro_esq = False
        self.frame = 0
        self.img_tiro = []
        for i in range(1, 11):  # Pegar 5 imagens
            self.img = pygame.image.load(os.path.join('images', str(estado_jogo.menu.daltonismo), 'fogo' + str(i) + '.png'))  # Pegar frames sapinho+i da pasta images
            self.img = pygame.transform.scale(self.img, (260, 260))  # Redimensionar imagem para 60x60
            self.img_tiro.append(self.img)  # Adicionar imagens na lista para o sprite do sapo

        self.image = self.img_tiro[0]
        self.rect = self.image.get_rect()
        self.rect.x = estado_jogo.menu.player.rect.right - 50
        self.rect.centery = estado_jogo.menu.player.rect.centery
        self.speed = 0.5

    def update(self):
            if self.estado:
                if self.tiro_esq:
                    self.frame = self.frame + 0.3
                    if self.frame >= len(self.img_tiro):
                        self.frame = 0
                        self.kill()
                    self.image = self.img_tiro[int(self.frame)]
                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    self.frame = self.frame + 0.3
                    if self.frame >= len(self.img_tiro):
                        self.frame = 0
                        self.kill()
                    self.image = self.img_tiro[int(self.frame)]

    def kill(self):
        self.estado = False

    def colisao_tiro(self):
        for enemy in estado_jogo.inimigos:
            self.teste_colisao_tiro = pygame.sprite.collide_mask(self, enemy)
            if self.teste_colisao_tiro and enemy.estado:
                enemy.kill()

class Menu():
    def __init__(self):
        self.img_menu = pygame.image.load(os.path.join('images', 'slides', 'menu.png'))
        self.img_menu = pygame.transform.scale(self.img_menu, (960, 540))
        self.img_cel = pygame.image.load(os.path.join('images', 'slides', 'celula_botao.png'))
        self.img_cel = pygame.transform.scale(self.img_cel, (40, 40))
        self.cel_rect = self.img_cel.get_rect()
        self.teste_cel = False
        self.daltonismo = "images_comum"

        self.list_rect = []
        self.rect_iniciar = pygame.Rect(365, 240, 230, 50)  # Rect iniciar
        self.list_rect.append(self.rect_iniciar)
        self.rect_deutan = pygame.Rect(395, 370, 170, 35)  # Rect deutan
        self.list_rect.append(self.rect_deutan)
        self.rect_protan = pygame.Rect(395, 410, 170, 35)  # Rect protan
        self.list_rect.append(self.rect_protan)
        self.rect_tritan = pygame.Rect(380, 450, 200, 35)  # Rect tritan
        self.list_rect.append(self.rect_tritan)

    def processar_movimentos(self, eventos):
        self.teste_cel = False
        for botao in self.list_rect:
            self.mouse_pos = pygame.mouse.get_pos()
            if botao.collidepoint(self.mouse_pos):
                self.teste_cel = True
                self.cel_rect.x = botao.x - 40
                self.cel_rect.y = botao.y
        for e in eventos:
            for botao in self.list_rect:
                self.mouse_pos = pygame.mouse.get_pos()
                if botao.collidepoint(self.mouse_pos):
                    #screen.blit(self.img_cel, (530, 400))
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if botao == self.list_rect[0]:
                            estado_jogo.estado_fases = 3
                            self.jogo = Jogo()
                            self.player = Player()  # Cria player
                            #self.menu.jogo = Jogo()  # Cria o jogo
                        if botao == self.list_rect[1]:
                            self.daltonismo = "images_tritan"
                        if botao == self.list_rect[2]:
                            self.daltonismo = "images_protan"
                        if botao == self.list_rect[3]:
                            self.daltonismo = "images_deutan"



class Historia():
    def __init__(self):
        self.imagens = []
        for i in range(1, 5):
            self.img = pygame.image.load(os.path.join('images', 'slides', 'historia' + str(i) + '.png'))
            self.img = pygame.transform.scale(self.img, (960, 540))
            self.imagens.append(self.img)
        self.img_gameover = pygame.image.load(os.path.join('images', 'slides', 'gameover.png'))
        self.img_gameover = pygame.transform.scale(self.img_gameover, (960, 540))
        self.img_fim = pygame.image.load(os.path.join('images', 'slides', 'fim.png'))
        self.img_fim = pygame.transform.scale(self.img_fim, (960, 540))

        self.image = self.imagens[0]
        self.rect = self.image.get_rect()
        self.frame = 0

    def update_historia(self):
        self.frame = self.frame + 1
        if self.frame == 4:
            self.frame = 3
            estado_jogo.estado_fases = 1
        self.image = self.imagens[self.frame]

    def update_gameover(self):
        self.image = self.img_gameover
        estado_jogo.estado_fases = 4
        estado_jogo.menu.player.movex = 0

    def update_fim(self):
        self.image = self.img_fim
        estado_jogo.estado_fases = 6

# Processar os movimentos
    def processar_movimentos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if estado_jogo.estado_fases == 4:
                        estado_jogo.estado_fases = 1
                        estado_jogo.def_fase1()
                    else:
                        self.update_historia()

class Hud():
    def __init__(self):
        self.img_vida = pygame.image.load('images/'+str(estado_jogo.menu.daltonismo)+'/vida.png')
        self.img_vida = pygame.transform.scale(self.img_vida, (50, 50))
        self.img_chave = pygame.image.load('images/'+str(estado_jogo.menu.daltonismo)+'/chave1.png')
        self.img_chave = pygame.transform.scale(self.img_chave, (55, 30))

        self.smallfont = pygame.font.SysFont('Corbel',35)
        self.text_vida = self.smallfont.render(': ' + str(estado_jogo.menu.player.vida), True, 000000)
        self.text_chave = self.smallfont.render(': ' + str(estado_jogo.porta.Nchaves) + '/' + str(estado_jogo.max_chaves), True, 000000)

    def update(self):
        self.text_vida = self.smallfont.render(': ' + str(estado_jogo.menu.player.vida), True, 000000)
        self.text_chave = self.smallfont.render(': ' + str(estado_jogo.porta.Nchaves) + '/' + str(estado_jogo.max_chaves), True, 000000)

class EstadoJogo():  # Escolha e main das fases

    def __init__(self):
        self.estado_fases = 5  # Inicia pela fase 1
        self.menu = Menu()
        self.historia = Historia()
        self.inicio_fase = True


    def def_fase1(self):
        #self.menu.jogo = Jogo()
        self.inimigos = []
        self.menu.player.vida = 5
        self.max_chaves = 0
        self.menu.player.rect.x = 0
        self.menu.player.rect.y = 140
        self.mapa_atual = self.menu.jogo.mapa

        self.inimigos.append(Sapo(2625, 400))
        self.max_chaves += 1
        self.inimigos.append(Sapo(3125, 400))
        self.max_chaves += 1
        self.porta = Porta(3400, 240)
        self.hud = Hud()

        self.inicio_fase = False


    def def_fase2(self):
        self.mapa_atual = self.menu.jogo.mapa2
        self.max_chaves = 0
        self.menu.player.rect.x = 0
        self.menu.player.rect.y = 140
        self.inimigos.clear()
        self.inimigos.append(Gripe(2150, 380))
        self.max_chaves += 1
        self.inimigos.append(Sapo(1470, 149))
        self.max_chaves += 1
        self.inimigos.append(Sapo(2160, 35))
        self.max_chaves += 1
        self.inimigos.append(Gripe(2650, 30))
        self.max_chaves += 1
        self.porta = Porta(3420, 40)
        self.gordura = Gordura(1150, 405)
        print("AQUI")

        self.inicio_fase = False

    def main_menu(self):
        screen.blit(self.menu.img_menu, screen.get_rect().topleft)  # Printar player com o movimento da camera
        if self.menu.teste_cel:
            screen.blit(self.menu.img_cel, (self.menu.cel_rect.x, self.menu.cel_rect.y))
        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

        self.menu.processar_movimentos(eventos)

    def main_historia(self):
        screen.blit(self.historia.image, screen.get_rect().topleft)  # Printar player com o movimento da camera

        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

        self.historia.processar_movimentos(eventos)  # Processar movimentos

    def main_fase1(self):  # Main fase 1
        # Pintar a tela
        screen.fill(self.menu.jogo.fundo)  # Pintar o fundo
        self.int_scroll = self.menu.jogo.movimento_camera()  # Movimentar a tela de acrodo com o movimento do personagem
        screen.blit(self.menu.player.image, (self.menu.player.rect.x - self.int_scroll[0],self.menu.player.rect.y - self.int_scroll[1]))  # Printar player com o movimento da camera
        self.screen_rect = pygame.Rect(self.int_scroll[0], self.int_scroll[1], 960, 540)
        for enemy in self.inimigos:
            if self.screen_rect.colliderect(enemy.rect) and enemy.estado:
                    screen.blit(enemy.image, (enemy.rect.x - self.int_scroll[0], enemy.rect.y - self.int_scroll[1]))
            if self.screen_rect.colliderect(enemy.chave.rect) and enemy.chave.estado:
                    screen.blit(enemy.chave.image, (enemy.chave.rect.x - self.int_scroll[0], enemy.chave.rect.y - self.int_scroll[1]))
        if self.screen_rect.colliderect(self.porta.rect):
            screen.blit(self.porta.image, (self.porta.rect.x - self.int_scroll[0], self.porta.rect.y - self.int_scroll[1]))
        pygame.draw.rect(screen, AZUL, pygame.Rect(730, 0, 230, 50))
        screen.blit(self.hud.img_vida, (730, 0))
        screen.blit(self.hud.text_vida, (785, 3))
        screen.blit(self.hud.img_chave, (830, 8))
        screen.blit(self.hud.text_chave, (890, 5))



        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

        self.menu.player.action = self.menu.player.processar_movimentos(eventos, self.menu.player.action)  # Processar movimentos

        # Update do player
        self.menu.jogo.update()  # Escolher acao

    def main_fase2(self):  # Main fase 1
        # Pintar a tela
        screen.fill(self.menu.jogo.fundo)
        self.int_scroll = self.menu.jogo.movimento_camera()  # Movimentar a tela de acrodo com o movimento do personagem
        screen.blit(self.menu.player.image, (self.menu.player.rect.x - self.int_scroll[0],self.menu.player.rect.y - self.int_scroll[1]))  # Printar player com o movimento da camera
        self.screen_rect = pygame.Rect(self.int_scroll[0], self.int_scroll[1], 960, 540)
        for enemy in self.inimigos:
            if self.screen_rect.colliderect(enemy.rect) and enemy.estado:
                    screen.blit(enemy.image, (enemy.rect.x - self.int_scroll[0], enemy.rect.y - self.int_scroll[1]))
            if self.screen_rect.colliderect(enemy.chave.rect) and enemy.chave.estado:
                    screen.blit(enemy.chave.image, (enemy.chave.rect.x - self.int_scroll[0], enemy.chave.rect.y - self.int_scroll[1]))
        if self.screen_rect.colliderect(self.porta.rect):
            screen.blit(self.porta.image, (self.porta.rect.x - self.int_scroll[0], self.porta.rect.y - self.int_scroll[1]))
        if self.screen_rect.colliderect(self.gordura.rect) and self.gordura.estado:
            screen.blit(self.gordura.image,(self.gordura.rect.x - self.int_scroll[0], self.gordura.rect.y - self.int_scroll[1]))
        if self.screen_rect.colliderect(self.gordura.laranja.rect) and self.gordura.laranja.estado:
            screen.blit(self.gordura.laranja.image, (self.gordura.laranja.rect.x - self.int_scroll[0], self.gordura.laranja.rect.y - self.int_scroll[1]))
        if self.gordura.laranja.var_laranja:
            if self.menu.player.tiro.estado:
                screen.blit(self.menu.player.tiro.image, (self.menu.player.tiro.rect.x - self.int_scroll[0], self.menu.player.tiro.rect.y - self.int_scroll[1]))
        pygame.draw.rect(screen, AZUL, pygame.Rect(730, 0, 230, 50))
        screen.blit(self.hud.img_vida, (730, 0))
        screen.blit(self.hud.text_vida, (785, 3))
        screen.blit(self.hud.img_chave, (830, 8))
        screen.blit(self.hud.text_chave, (890, 5))

        pygame.display.update(screen.get_rect())  # Atuzalizar tela
        clock.tick(fps)

        # Captura de movimentos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

        self.menu.player.action = self.menu.player.processar_movimentos(eventos, self.menu.player.action)  # Processar movimentos

        # Update do player
        self.menu.jogo.update()  # Escolher

    def selecao_estado(self):  # Escolha da fase
        if self.estado_fases == 6:
            self.main_historia()
        if self.estado_fases == 5:
            self.main_menu()
        if self.estado_fases == 4:
            self.main_historia()
        if self.estado_fases == 3:
            self.main_historia()
        if self.estado_fases == 1:
            if self.inicio_fase:
                self.def_fase1()
            self.main_fase1()
        if self.estado_fases == 2:
            if self.inicio_fase:
                self.def_fase2()
            self.main_fase2()

# Main
if __name__ == "__main__":

    pygame.init()  # Iniciar o pygame

    estado_jogo = EstadoJogo()
    #player = Player()  # Cria player
    clock = pygame.time.Clock()  # Objeto de tempo


    #true_scroll = [0, 0]  #  Valor inicial do scroll da camera

    while True:
        estado_jogo.selecao_estado()
