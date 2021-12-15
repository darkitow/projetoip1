import pygame as pg
from tiles import *
debug = False

# Colors
class colors:
    white = (255,255,255)
    black = (0,0,0)
    purple = (135,90,255)
backgroundColor = colors.white
pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 10)

# Resolution
GAME_RESOLUTION = (240,160)
WINDOW_RESOLUTION = (900,600)

# Intialize window and clock
pg.init()
window = pg.display.set_mode(WINDOW_RESOLUTION)
screen = pg.Surface((0,0))
clock = pg.time.Clock()

# Icon and Title
pg.display.set_caption('Trans rights')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

# Player Sprites
playerImg_left = pg.image.load('assets/player/player-left.png')
playerImg_right = pg.image.load('assets/player/player-right.png')
playerImg_down = pg.image.load('assets/player/player-down.png')
playerImg_up = pg.image.load('assets/player/player-up.png')

# Map
map = TileMap('assets/maps/testmap.csv')

# Player
class Player:
    def __init__(self):
        self.pos = [map.start_x,map.start_y]
        self.vel = [0,0]
        self.speed = 1.8
        self.img = playerImg_right
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.collect = {'coin':0,'purple_potion':False}

    def checkCollision(self):
        for tile in map.tiles:
            if self.rect.colliderect(tile.rect):
                return True
        for obj in map.objects:
            if self.rect.colliderect(obj.rect):
                if obj.color == backgroundColor:
                    return
                if obj.solid:
                    return True
                if obj.collectable:
                    if obj.id == 'coin':
                        if obj.display:
                            self.collect['coin'] += 1
                    else:
                        self.collect[obj.id] = True
                    obj.display = False
            

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.checkCollision():
            self.pos[0] -= self.vel[0]
            self.pos[1] -= self.vel[1]
player = Player()

# Update player position and check if out of game border
def drawPlayer():
    global player
    if player.pos[0] <= 0:
        player.pos[0] = 0
    if player.pos[0] >= GAME_RESOLUTION[0]-player.rect.width:
        player.pos[0] = GAME_RESOLUTION[0]-player.rect.width
    if player.pos[1] <= 0:
        player.pos[1] = 0
    if player.pos[1] >= GAME_RESOLUTION[1]-player.rect.height:
        player.pos[1] = GAME_RESOLUTION[1]-player.rect.height
    screen.blit(player.img, player.rect)

# Move player when key is hold
def playerControl():
    global player
    keys = pg.key.get_pressed()
    player.vel = (0,0)
    # Move player, change sprite based on direction
    if keys[pg.K_LEFT]:
        player.vel = (-player.speed,0)
        player.img = playerImg_left
    if keys[pg.K_RIGHT]:
        player.vel = (player.speed,0)
        player.img = playerImg_right
    if keys[pg.K_UP]:
        player.vel = (0,-player.speed)
        player.img = playerImg_up
    if keys[pg.K_DOWN]:
        player.vel = (0,player.speed)
        player.img = playerImg_down
    player.move()

def keyPress(e):
    global backgroundColor, crateImg, debug, player, map
    if e.key == pg.K_1:
        backgroundColor = colors.white
    if e.key == pg.K_2 and player.collect['purple_potion']:
        backgroundColor = colors.purple
    if e.key == pg.K_0:
        debug = not debug
    if e.key == pg.K_r:
        map = TileMap('assets/maps/testmap.csv')
        player=Player()

def draw():
    global screen
    screen = pg.Surface(GAME_RESOLUTION)
    screen.fill(backgroundColor)
    
    # map
    map.draw_map(screen)

    # objects
    for obj in map.objects:
        if obj.collectable:
            if not obj.display:
                continue
        obj.draw(screen)

    # player
    drawPlayer()

    # overlay
    pg.draw.rect(screen, colors.black, (19,19,18,10), 0)
    pg.draw.rect(screen, colors.white, (20,20,8,8), 0)
    if player.collect['purple_potion']:
        pg.draw.rect(screen, colors.purple, (28,20,8,8), 0)
    # coin text
    textsurface = myfont.render(f'{player.collect["coin"]} Coins', False, (0, 0, 0))
    screen.blit(textsurface,(20,28))

    
    # debug
    if debug:
        pg.draw.rect(screen, (255,0,0), player.rect, 1)
        for obj in map.objects:
            pg.draw.rect(screen, (0,255,0), obj.rect, 1)

    screen = pg.transform.scale(screen, WINDOW_RESOLUTION)
    window.blit(screen, (0,0))

# Game Loop
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            keyPress(event)

    playerControl()
    draw()

    pg.display.update()
    clock.tick(30)