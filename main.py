import pygame as pg
from tiles import *
from game import *

# inicializar
pg.init()
game = Game()

# Icon and Title
pg.display.set_caption('Trans rights')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

# Game Loop
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            run = False
    
    game.inGame()
    pg.display.update()