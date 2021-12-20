import pygame
import sys
import os
pygame.mixer.init()#Inicializando a biblioteca da música

#Carregando as imagens de background
bg_image = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background_menu", "Spectre1.png")), (900, 600))
bg_image_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background_menu", "SpectreV.png")), (900, 600))

#Carregando a música
bg_music = pygame.mixer.Sound(os.path.join("assets", "musicadefundo.mpeg"))

#Criando a classe menu que será usada como base para as outras funções,
#em resumo, começa declarando a música assim que iniciar o menu, depois declara o display e os ângulos do cursor
class Menu:
    bg_music.play()

    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 130, 130)
        self.offset = - 100
        
#criando cursor de seleção das opções do menu
    def draw_cursor(self):
        self.game.draw_text('>', 20, self.cursor_rect.x, self.cursor_rect.y)
        
#Função para tela
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

#Classe de menu principal que irá atribuir variáveis
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Começar"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.tutorialx, self.tutorialy = self.mid_w, self.mid_h + 40
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 80
        self.exitx, self.exity = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        
#Laço de repetição para mostrar os textos do menu na tela
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(bg_image, (0, 0))
            self.game.draw_text("Começar", 20, self.startx, self.starty)
            self.game.draw_text('Comandos', 20, self.tutorialx, self.tutorialy)
            self.game.draw_text("Créditos", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Sair", 20, self.exitx, self.exity)
            self.game.draw_text("Voltar: Backspace", 10, self.mid_w - 200, self.mid_h + 190)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 190)
            self.draw_cursor()
            self.blit_screen()

#Função para organizar o movimento do cursor em cima/baixo
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Começar':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Comandos'
            elif self.state == 'Comandos':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Créditos'
            elif self.state == 'Créditos':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Começar'
        elif self.game.UP_KEY:
            if self.state == 'Começar':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Créditos'
            elif self.state == 'Comandos':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Começar'
            elif self.state == 'Créditos':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Comandos'

#Função para dar interação aos botões
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Começar':
                self.game.playing = True
            elif self.state == 'Comandos':
                self.game.curr_menu = self.game.options
            elif self.state == 'Créditos':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Sair':
                sys.exit()
            self.run_display = False

#Função para a opção "comando" ter um sub menu mostrando instruções de controle
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.tecladox, self.tecladoy = self.mid_w, self.mid_h + 0
        self.cimax, self.cimay = self.mid_w, self.mid_h + 60
        self.baixox, self.baixoy = self.mid_w, self.mid_h + 90
        self.esquerdax, self.esquerday = self.mid_w, self.mid_h + 120
        self.direitax, self.direitay = self.mid_w, self.mid_h + 150
        self.troca_corx, self.troca_cory = self.mid_w, self.mid_h + 180

#Função para dar vida às variáveis acima e mostrar as instruções
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(bg_image_2, (0, 0))
            self.game.draw_text("Comandos", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 120)
            self.game.draw_text("Teclado", 30, self.tecladox, self.tecladoy)
            self.game.draw_text("Andar para Cima : Seta Cima", 15, self.cimax, self.cimay)
            self.game.draw_text("Andar para Baixo : Seta Baixo", 15, self.baixox, self.baixoy)
            self.game.draw_text("Andar para Esquerda : Seta Esquerda", 15, self.esquerdax, self.esquerday)
            self.game.draw_text("Andar para Direita : Seta Direita", 15, self.direitax, self.direitay)
            self.game.draw_text("Trocar de cor : 1, 2 e 3", 15, self.troca_corx, self.troca_cory)
            self.game.draw_text("Voltar: Backspace", 10, self.mid_w - 200, self.mid_h + 250)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 250)
            self.draw_cursor()
            self.blit_screen()

#Função para fazer voltar do sub menu para o menu
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            pass

#Classe de créditos
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

#Função para dar vida aos créditos e mostrar na tela em seu sub menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(bg_image_2, (0, 0))
            self.game.draw_text("Créditos", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text("Allysson Fellype Gomes Muniz (afgm2)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text("Andreson Gomes de Lima (agl4)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text("Cesar Moura (chcm)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.game.draw_text("Jorge Francisco (jflj)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100)
            self.game.draw_text("Ruan Anselmo Santos de Lima (rasl)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 130)
            self.game.draw_text("Vitor de Almeida Ferreira (vaf)", 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 160)
            self.game.draw_text("Voltar: Backspace", 10, self.mid_w - 200, self.mid_h + 250)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 250)
            self.blit_screen()

