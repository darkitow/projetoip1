import game_module as gm
import pygame as pg

while gm.game_main.running:
    gm.game_main.curr_menu.display_menu()
    gm.game_main.inGame()

pg.quit()
