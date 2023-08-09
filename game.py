#!/usr/bin/python3
import pygame
import pygame.mixer
import pygame.freetype
import pygame.joystick
import sys
import os
pygame.mixer.init()
MusicOn = True
global ctrl

try:
    pygame.joystick.init()
    pygame.joystick.get_count()
    c = [pygame.joystick.Joystick(c) for c in range(pygame.joystick.get_count())]
    ctrl = True
except:
    ctrl = False

time = 0
seconds = 0
minute = 0
'''
Variables
'''
crouch = 'crouch'
stand = 'stand'
walk = 'walk'
jump = 'jump'
lvl = 1
s = 'sound'
if MusicOn == True:
    music = pygame.mixer.music.load(os.path.join(s, 'music.ogg'))
    pygame.mixer.music.play(-1)

flag = pygame.mixer.Sound(os.path.join(s, 'flag.ogg'))
item = pygame.mixer.Sound(os.path.join(s, '1up.ogg'))
ouch = pygame.mixer.Sound(os.path.join(s, 'Hit.ogg'))
walk = pygame.mixer.Sound(os.path.join(s, 'walk.ogg'))
coin = pygame.mixer.Sound(os.path.join(s, 'coin.ogg'))
Fire = pygame.mixer.Sound(os.path.join(s, 'Fire.ogg'))
Jump = pygame.mixer.Sound(os.path.join(s, 'jump.ogg'))
worldx = 960
worldy = 720
enemyx = 400
enemyy = 605
fps = 30 
ani = 4
world = pygame.display.set_mode([worldx, worldy], pygame.RESIZABLE)
forwardx  = 600
backwardx = 120
BLUE = (80, 80, 155)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (153,102,255)

tx = 64
ty = 64

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts", 'font.ttf')
font_size = tx
pygame.freetype.init()
myfont = pygame.freetype.Font(font_path, font_size)


'''
Objects
'''

def stats(score, health, powerup):
    myfont.render_to(world, (4, 4), "Score "+str(score), BLACK, None, size=42)
    myfont.render_to(world, (4, 52), "Health "+str(health), BLACK, None, size=42)
    myfont.render_to(world, (4, 94), "Powerup "+str(powerup), BLACK, None, size=42)


class Throwable(pygame.sprite.Sprite):
    """
    Spawn a throwable object
    """
    def __init__(self, x, y, img, throw):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.firing = throw

    def update(self, worldy):
        '''
        throw physics
        '''
        if self.rect.y < worldy:
            if player.facing_right:
                self.rect.x += 15
            else:
                self.rect.x -= 15
            self.rect.y += 5
        else:
            self.kill()
            self.firing = 0


# x location, y location, img width, img height, img file
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.powerup = None
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.damage = 0
        self.score = 0
        self.facing_right = True
        self.is_jumping = True
        self.is_double_jump = True
        self.is_falling = True
        self.images = []
        self.anim = walk
        for i in range(1, 7):
            if self.anim == walk:
                img = pygame.image.load(os.path.join('images', 'walk' + str(i) + '.png')).convert()
                img.convert_alpha()
                img.set_colorkey(ALPHA)
                self.images.append(img)
                self.image = self.images[0]
                self.rect = self.image.get_rect()

        if self.anim == stand:
            img = pygame.image.load(os.path.join('images', 'walk5.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[4]
            self.rect = self.image.get_rect()
        if self.anim == jump:
            img = pygame.image.load(os.path.join('images', 'walk6.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[5]
            self.rect = self.image.get_rect()
        if self.anim == crouch:
            img = pygame.image.load(os.path.join('images', 'walk7.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[6]
            self.rect = self.image.get_rect()




    def gravity(self):
        if self.is_jumping:
            self.movey += 5

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x

    def jump(self):
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True
            self.is_double_jump = False
            self.anim = jump
            pygame.mixer.Sound.play(Jump)
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

    def update(self):
        """
        Update sprite position
        """
        if self.health <= 0:
            pygame.quit()
        # moving left
        if self.movex < 0:
            self.anim = walk
            self.is_jumping = True
            self.is_double_jump = False
            self.frame += 1
            if self.frame >= 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.anim = walk
            self.is_jumping = True
            self.is_double_jump = False
            self.frame += 1
            if self.frame >= 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]

        # collisions
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        if self.damage == 0:
            for enemy in enemy_hit_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)
        if self.damage == 1:
            idx = self.rect.collidelist(enemy_hit_list)
            if idx == -1:
                self.damage = 0   # set damage back to 0
                pygame.mixer.Sound.play(ouch)
                if self.powerup == None:
                    if self.health > 1:
                        self.health -= 1  # subtract 1 hp
                    else:
                        pygame.quit()
                else:
                    self.powerup = None

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False  # stop jumping
            self.is_double_jump = False
            self.anim == stand

        # fall off the world
        if self.rect.y > worldy:
            self.health -=1
            if self.health <= 0:
                pygame.quit()
            if self.facing_right == True:
                self.rect.x = tx
            else:
                self.rect.x = -tx
            self.rect.y = ty

        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
        for p in plat_hit_list:
            self.is_jumping = False  # stop jumping
            self.is_double_jump = False
            self.movey = 0
            if self.rect.bottom <= p.rect.bottom:
               self.rect.bottom = p.rect.top
            else:
               self.movey += 3.2

        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.movey -= 44  # how high to jump

        if self.is_jumping and self.is_falling is False and self.is_double_jump is True:
            self.is_falling = True
            self.movey -= 5  # how high to jump

        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1
            pygame.mixer.Sound.play(coin)

        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)

        self.rect.x += self.movex
        self.rect.y += self.movey

        flag_hit_list = pygame.sprite.spritecollide(self, flag_list, False)
        for flagpole in flag_hit_list:
            flag_list.remove(flagpole)
            self.score += 10
            self.health = 10
            pygame.mixer.Sound.play(flag)

        item_hit_list = pygame.sprite.spritecollide(self, item_list, False)
        for powerup in item_hit_list:
            pygame.mixer.Sound.play(item)
            item_list.remove(powerup)
            self.score += 10
            self.powerup = 'fireflower'


             

class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def move(self):
        """
        enemy movement
        """
        distance = 10
        speed = 8

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

    def update(self, firepower, enemy_list):
        """
        detect firepower collision
        """
        fire_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fire_hit_list:
            enemy_list.remove(self)
            player.score += 10
            pygame.mixer.Sound.play(ouch)


class Level:
    def ground(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i], worldy - ty, tx, ty, 'tile-ground.png')
                ground_list.add(ground)
                i = i + 1

        if lvl == 2:
            while i < len(gloc):
                ground = Platform(gloc[i], worldy - ty, tx, ty, 'tile-ground.png') # you can change the ground look for different levels btw
                ground_list.add(ground)
                i = i + 1

        return ground_list

    def bad(lvl, eloc):
        if lvl == 1:
            enemy_list = pygame.sprite.Group()
            enemy = Enemy(enemyx*1, enemyy*1, 'enemy.png')
            enemy_list.add(enemy)


        if lvl == 2:
            enemy_list = pygame.sprite.Group()
            enemy = Enemy(enemyx*1, enemyy*1, 'enemy.png')
            enemy_list.add(enemy)

        return enemy_list

    # x location, y location, img width, img height, img file
    def platform(lvl, tx, ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0
        if lvl == 1:
            ploc.append((200, worldy - ty - 128, 4.5))
            ploc.append((300, worldy - ty - 256, 4.5))
            ploc.append((800, worldy - ty - 64, 4.5))
            ploc.append((864, worldy - ty - 128, 2.5))
            ploc.append((928, worldy - ty - 192, .5))
                    
            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, 'tile.png')
                    plat_list.add(plat)
                    j += 1
                i += 1

        if lvl == 2:
            ploc.append((200, worldy - ty - 128, 2))
            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, 'tile.png')
                    plat_list.add(plat)
                    j += 1
                i += 1


        return plat_list

    def loot(lvl):
        if lvl == 1:
            loot_list = pygame.sprite.Group()
            loot = Platform(tx*6, ty*5, tx, ty, 'loot_1.png')
            loot_list.add(loot)



        if lvl == 2:
            loot_list = pygame.sprite.Group()
            loot = Platform(tx*5, ty*5, tx, ty, 'loot_1.png')
            loot_list.add(loot)

        return loot_list

    def flagpole(lvl):
        if lvl == 1:
            flag_list = pygame.sprite.Group()
            flagpole = Platform(tx*5, ty*8.8, tx, ty, 'flag.png')
            flag_list.add(flagpole)

        if lvl == 2:
            print("Level: ",lvl)

        return flag_list


    def powerup(lvl):
        if lvl == 1:
            item_list = pygame.sprite.Group()
            powerup = Platform(tx*5, ty*5.8, tx, ty, 'powerup.png')
            item_list.add(powerup)


        if lvl == 2:
            print("Level: ",lvl)

        return item_list
        

'''
Setup
'''
try:
    if ctrl == True:
        joystick = pygame.joystick.Joystick(0)
except:
    ctrl = False

backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True


player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = 30  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10
fire = Throwable(player.rect.x, player.rect.y, 'fire.png', 0)
firepower = pygame.sprite.Group()

eloc = []
eloc = [enemyx, enemyy]
enemy_list = Level.bad(1, eloc)
gloc = []
i = 0
while i <= (worldx - tx):# + tx:
    gloc.append(i * tx)
    i = i + 1

ground_list = Level.ground(1, gloc, tx, ty)
flag_list = Level.flagpole(1)
item_list = Level.powerup(1)
plat_list = Level.platform(1, tx, ty)
enemy_list = Level.bad( 1, eloc )
loot_list = Level.loot(1)

Butn_A = 0
Butn_B = 1
Butn_X = 2
Butn_Y = 3
Butn_LB = 4
Butn_RB = 5
Butn_Back = 6
Butn_Start = 7


'''
menu Loop
'''

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if ctrl == True:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == Butn_A or event.button == Butn_B:
                    player.jump()
                    player.anim = jump
                if event.button == Butn_X or event.button == Butn_RB or event.button == Butn_LB:
                    if player.powerup == 'fireflower':
                        if not fire.firing:
                            fire = Throwable(player.rect.x, player.rect.y, 'fire.png', 1)
                            firepower.add(fire)
                            pygame.mixer.Sound.play(Fire) 
                if event.button == Butn_Y and player.is_jumping == True:
                    player.movey = (tx - 20)
                                                               
            if event.type == pygame.JOYHATMOTION:
                for i in range(hats):
                   hat = joystick.get_hat(i)
    
                if hat[0] == 1 or hat[1] == 1:
                    player.facing_right = True
                    player.control(steps, 0)
                    player.anim = walk
                if hat[0] == -1 or hat[1] == -1:
                    player.facing_right = False
                    player.control(-steps, 0)
                    player.anim = walk
                if hat == (0, 0):
                    if player.facing_right == False:
                        player.control(steps, 0)
                        player.facing_right = False
                        player.anim = stand
                    if player.facing_right == True:
                        player.control(-steps, 0)
                        player.facing_right = True
                        player.anim = stand
                                                            
            if event.type == pygame.JOYBUTTONUP:
                player.anim = stand
            else:
                player.anim = stand
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.facing_right = False
                player.control(-steps, 0)
                player.anim = walk
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.facing_right = True
                player.control(steps, 0)
                player.anim = walk
            if event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE:
                player.jump()
                player.anim = jump
            if event.key == ord('s') or event.key == pygame.K_DOWN and player.is_jumping == True:
                player.movey = (tx - 20)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
                player.facing_right = False
                player.anim = stand
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
                player.facing_right = True
                player.anim = stand
            if event.key == ord('x'):
                if player.powerup == 'fireflower':
                    if not fire.firing:
                        fire = Throwable(player.rect.x, player.rect.y, 'fire.png', 1)
                        firepower.add(fire)
                        pygame.mixer.Sound.play(Fire) 
            player.anim = stand



    # scroll the world forward
    if player.rect.x >= forwardx:
        scroll = player.rect.x - forwardx
        player.rect.x = forwardx
        for p in plat_list:
            p.rect.x -= scroll
        for e in enemy_list:
            e.rect.x -= scroll
        for l in loot_list:
            l.rect.x -= scroll
        for f in flag_list:
            f.rect.x -= scroll
        for i in item_list:
            i.rect.x -= scroll
        for g in ground_list:
            g.rect.x -= scroll
    # scroll the world backward
    if player.rect.x <= backwardx:
        scroll = backwardx - player.rect.x
        player.rect.x = backwardx
        for p in plat_list:
            p.rect.x += scroll
        for e in enemy_list:
            e.rect.x += scroll
        for l in loot_list:
            l.rect.x += scroll
        for f in flag_list:
            f.rect.x += scroll
        for i in item_list:
            i.rect.x += scroll
        for g in ground_list:
            g.rect.x += scroll            
            

    world.blit(backdrop, backdropbox)
    player.update()
    player.gravity()
    player_list.draw(world)
    if fire.firing:
        fire.update(worldy)
        firepower.draw(world)
    enemy_list.draw(world)
    enemy_list.update(firepower, enemy_list)
    loot_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)
    flag_list.draw(world)
    item_list.draw(world)
    try:
        if ctrl == True:
            hats = joystick.get_numhats()
    except:
        pass
    for e in enemy_list:
        e.move()
    stats(player.score, player.health, player.powerup)
    pygame.display.flip()
    clock.tick(fps * worldx)
    if player.anim == stand:
        img = pygame.image.load(os.path.join('images', 'walk5.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        player.images.append(img)
        player.image = player.images[4]
        if player.is_jumping == True:
            player.anim = jump
    if player.anim == jump:
        img = pygame.image.load(os.path.join('images', 'walk6.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        player.images.append(img)
        player.image = player.images[5]
    if player.anim == crouch:
        img = pygame.image.load(os.path.join('images', 'walk7.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        player.images.append(img)
        player.image = player.images[6]
    time = time + 0.1

