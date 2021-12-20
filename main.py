import game_module as gm
import pygame as pg

game_main = gm.Game()

while game_main.running:
    game_main.curr_menu.display_menu()
    game_main.inGame('assets/maps/map1.csv')

pg.quit()
