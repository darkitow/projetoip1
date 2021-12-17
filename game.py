import pygame as pg
from tiles import *
from config import *
debug = False

pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 10)

# Map
map = TileMap('assets/maps/testmap.csv')

# Player
class Player:
    def __init__(self, game):
        self.pos = [map.start_x,map.start_y]
        self.vel = [0,0]
        self.speed = 1
        
        self.collect = {'coin':0,'potion1':False, 'potion2': False}
        self.game = game
        
        self.sprites = {
            'left':[
                'assets/player/player-left1.png',
                'assets/player/player-left2.png',
                'assets/player/player-left3.png',
                'assets/player/player-left4.png',
            ],
            'right':[
                'assets/player/player-right1.png',
                'assets/player/player-right2.png',
                'assets/player/player-right3.png',
                'assets/player/player-right4.png',
            ],
            'up':[
                'assets/player/player-up1.png',
                'assets/player/player-up2.png',
                'assets/player/player-up3.png',
                'assets/player/player-up4.png',
            ],
            'down':[
                'assets/player/player-down1.png',
                'assets/player/player-down2.png',
                'assets/player/player-down3.png',
                'assets/player/player-down4.png',
            ],
        }
        self.loadSprites()
        self.img = self.sprites['right'][0]
        self.aniFrame = 0

        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = self.pos

    def loadSprites(self):
        for cod, frames in self.sprites.items():
            for i, sprite in enumerate(frames):
                self.sprites[cod][i] = pg.image.load(sprite).convert_alpha()

    def checkCollision(self):
        for tile in map.tiles:
            if self.rect.colliderect(tile.rect):
                return True
        for obj in map.objects:
            if self.rect.colliderect(obj.rect):
                if obj.color == self.game.bgColor:
                    continue
                if obj.solid:
                    return True
                if obj.collectable:
                    if obj.id == 'coin':
                        self.collect['coin'] += 1
                    else:
                        self.collect[obj.id] = True
                    map.objects.remove(obj)

    def animation(self):
        # reset animation when stopping
        if self.vel == (0,0):
            self.aniFrame = 0
        #left
        if self.vel[0] < 0:
            self.img = self.sprites['left'][int(self.aniFrame)]
        # right
        if self.vel[0] > 0:
            self.img = self.sprites['right'][int(self.aniFrame)]
        # up
        if self.vel[1] < 0:
            self.img = self.sprites['up'][int(self.aniFrame)]
        # down
        if self.vel[1] > 0:
            self.img = self.sprites['down'][int(self.aniFrame)]
        
        self.aniFrame += 4/60
        if self.aniFrame > 3:
            self.aniFrame = 0

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.checkCollision():
            self.pos[0] -= self.vel[0]
            self.pos[1] -= self.vel[1]
        
        self.animation()

# Game Loop
class Game:
    def __init__(self):
        self.playing = True
        self.debug = False
        pg.init()
        self.window = pg.display.set_mode(WINDOW_RESOLUTION)
        self.clock = pg.time.Clock()
        self.bgColor = colors.white
        self.player = Player(self)
    
    def colorOverlay(self, surf):
        pg.draw.rect(surf, colors.black, (19,19,28,10), 0)
        pg.draw.rect(surf, colors.white, (20,20,8,8), 0)
        if self.player.collect['potion1']:
            pg.draw.rect(surf, hue[1], (29,20,8,8), 0)
        if self.player.collect['potion2']:
            pg.draw.rect(surf, hue[2], (38,20,8,8), 0)

    # Move player when key is hold
    def playerControl(self):
        keys = pg.key.get_pressed()
        self.player.vel = (0,0)
        # Move player, change sprite based on direction
        if keys[pg.K_LEFT]:
            self.player.vel = (-self.player.speed,0)
        if keys[pg.K_RIGHT]:
            self.player.vel = (self.player.speed,0)
        if keys[pg.K_UP]:
            self.player.vel = (0,-self.player.speed)
        if keys[pg.K_DOWN]:
            self.player.vel = (0,self.player.speed)

    def keyPress(self,e):
        global map
        if e.key == pg.K_1:
            self.bgColor = colors.white
        if e.key == pg.K_2 and self.player.collect['potion1']:
            self.bgColor = hue[1]
        if e.key == pg.K_3 and self.player.collect['potion2']:
            self.bgColor = hue[2]
        if e.key == pg.K_0:
            self.debug = not self.debug
        if e.key == pg.K_r:
            map = TileMap('assets/maps/testmap.csv')
            self.player = Player(self)
        if e.key == pg.K_ESCAPE:
            self.playing = False

    def drawGame(self):
        self.screen = pg.Surface(GAME_RESOLUTION)
        self.screen.fill(self.bgColor)
        # map
        map.draw_map(self.screen)
        # objects
        for obj in map.objects:
            obj.draw(self.screen)
        # player
        self.player.move()
        self.screen.blit(self.player.img, self.player.rect)
        # overlay
        self.colorOverlay(self.screen)
        # coin text
        textsurface = myfont.render(f'{self.player.collect["coin"]} Coins', False, (0, 0, 0))
        self.screen.blit(textsurface,(20,28))
        # debug
        if self.debug:
            pg.draw.rect(self.screen, (255,0,0), self.player.rect, 1)
            for obj in map.objects:
                pg.draw.rect(self.screen, (0,255,0), obj.rect, 1)
        # scale screen
        self.screen = pg.transform.scale(self.screen, WINDOW_RESOLUTION)
        self.window.blit(self.screen, (0,0))

    def inGame(self):
        while self.playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                if event.type == pg.KEYDOWN:
                    self.keyPress(event)
            self.playerControl()
            self.drawGame()
            pg.display.update()
            self.clock.tick(60)