import pygame as pg
import os, csv

class Tile:
    def __init__(self,image,x,y,solid=False,collectable=False,id=None,color=None):
        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.solid = solid
        self.collectable = collectable
        self.id = id
        self.color = color

    def draw(self, surf):
        surf.blit(self.image,(self.rect.x,self.rect.y))
        #pg.draw.rect(surf, (255,0,0), self.rect, 1)

class TileMap:
    def __init__(self, filename):
        self.tile_size = 16
        self.start_x, self.start_y = 0,0
        self.tiles, self.objects = self.load_tiles(filename)
        self.map_surface = pg.Surface((self.map_w,self.map_h))
        self.map_surface.fill((255,255,255))
        self.map_surface.set_colorkey((255,255,255))
        self.load_map()

    def read_csv(self, filename):
        map = list()
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = [] ; objects = []
        map = self.read_csv(filename)
        x,y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x*self.tile_size,y*self.tile_size
                if tile == '4':
                    tiles.append(Tile('assets/walltl.png',x*self.tile_size,y*self.tile_size))
                if tile == '5':
                    tiles.append(Tile('assets/wallt.png',x*self.tile_size,y*self.tile_size))
                if tile == '6':
                    tiles.append(Tile('assets/walltr.png',x*self.tile_size,y*self.tile_size))
                if tile == '14':
                    tiles.append(Tile('assets/walll.png',x*self.tile_size,y*self.tile_size))
                if tile == '24':
                    tiles.append(Tile('assets/wallbl.png',x*self.tile_size,y*self.tile_size))
                if tile == '25':
                    tiles.append(Tile('assets/wallb.png',x*self.tile_size,y*self.tile_size))
                if tile == '16':
                    tiles.append(Tile('assets/wallr.png',x*self.tile_size,y*self.tile_size))
                if tile == '26':
                    tiles.append(Tile('assets/wallbr.png',x*self.tile_size,y*self.tile_size))
                if tile == '7':
                    objects.append(Tile('assets/crate.png',x*self.tile_size,y*self.tile_size,solid=True))
                if tile == '8':
                    objects.append(Tile('assets/crate_purple.png',x*self.tile_size,y*self.tile_size,solid=True,color=(135,90,255)))
                if tile == '17':
                    objects.append(Tile('assets/potion.png',x*self.tile_size,y*self.tile_size,collectable=True,id='purple_potion'))
                if tile == '10':
                    objects.append(Tile('assets/coin.png',x*self.tile_size,y*self.tile_size,collectable=True,id='coin'))
                x += 1
            y += 1
        self.map_w, self.map_h = x*self.tile_size,y*self.tile_size
        return tiles, objects
    
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))