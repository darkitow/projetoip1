import pygame as pg
import os, csv
from config import *


# Icon and Title
pg.display.set_caption('Spectre')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

pg.init()
window = pg.display.set_mode(WINDOW_RESOLUTION)


def changeColor(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pg.BLEND_MIN)
    return finalImage


class Tile:
    def __init__(self, image, x, y, solid=False, collectable=False, id=None, color_id=None):  # novo parametro color_id
        self.image = pg.image.load(image).convert_alpha()
        # color_id : posicao da cor no dicionario hue
        # caso seja um bloco colorido
        self.color = None
        if color_id != None:
            self.color = hue[color_id]
            self.color_value = pg.Color(hue[color_id])
            self.image = changeColor(self.image, self.color_value)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.solid = solid
        self.collectable = collectable
        self.id = id

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))

class TileMap:
    def __init__(self, filename):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.tiles, self.objects = self.load_tiles(filename)
        self.map_surface = pg.Surface((self.map_w, self.map_h))
        self.map_surface.fill((255, 255, 255))
        self.map_surface.set_colorkey((255, 255, 255))
        self.load_map()

    def read_csv(self, filename):
        map = list()
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        objects = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                if tile == '4':
                    tiles.append(Tile('assets/tiles/walltl.png', x * self.tile_size, y * self.tile_size))
                if tile == '5':
                    tiles.append(Tile('assets/tiles/wallt.png', x * self.tile_size, y * self.tile_size))
                if tile == '6':
                    tiles.append(Tile('assets/tiles/walltr.png', x * self.tile_size, y * self.tile_size))
                if tile == '14':
                    tiles.append(Tile('assets/tiles/walll.png', x * self.tile_size, y * self.tile_size))
                if tile == '24':
                    tiles.append(Tile('assets/tiles/wallbl.png', x * self.tile_size, y * self.tile_size))
                if tile == '25':
                    tiles.append(Tile('assets/tiles/wallb.png', x * self.tile_size, y * self.tile_size))
                if tile == '16':
                    tiles.append(Tile('assets/tiles/wallr.png', x * self.tile_size, y * self.tile_size))
                if tile == '26':
                    tiles.append(Tile('assets/tiles/wallbr.png', x * self.tile_size, y * self.tile_size))
                if tile == '10':
                    objects.append(
                        Tile('assets/objetos/coin.png', x * self.tile_size, y * self.tile_size, collectable=True, id='coin'))
                if tile == '100':
                    objects.append(
                        Tile('assets/objetos/crate.png', x * self.tile_size, y * self.tile_size, solid=True, color_id=0))
                # tiles abaixo possuem o atributo color_id para modificar sua cor
                if tile == '101':
                    objects.append(
                        Tile('assets/objetos/crate.png', x * self.tile_size, y * self.tile_size, solid=True, color_id=1))
                if tile == '102':
                    objects.append(
                        Tile('assets/objetos/crate.png', x * self.tile_size, y * self.tile_size, solid=True, color_id=2))
                if tile == '201':
                    objects.append(Tile('assets/objetos/potion.png', x * self.tile_size, y * self.tile_size, collectable=True,
                                        id='potion1', color_id=1))
                if tile == '202':
                    objects.append(Tile('assets/objetos/potion.png', x * self.tile_size, y * self.tile_size, collectable=True,
                                        id='potion2', color_id=2))

                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles, objects

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))
