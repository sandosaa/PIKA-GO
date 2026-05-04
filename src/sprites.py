from settings import *
from settime import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self,surf, pos, direction, groups):
        super().__init__(pos, surf, groups)
        self.image = pygame.transform.flip(self.image,direction ==-1,False) 
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x +=self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, pos, surf, groups,player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.facing_right = player.facing_right
        self.timer = Timer(100,autostart=True,func=self.kill)

        if not self.player.facing_right:
            self.rect.midright = self.player.rect.midleft+pygame.Vector2(0, 10)
            self.image = pygame.transform.flip(self.image,True,False)
        else:
            self.rect.midleft = self.player.rect.midright+pygame.Vector2(0, 10)


    def update(self,_): 
        self.timer.update()

        if not self.player.facing_right:
            self.rect.midright = self.player.rect.midleft+pygame.Vector2(0, 10)
        else:
            self.rect.midleft = self.player.rect.midright+pygame.Vector2(0, 10)

        if self.facing_right != self.player.facing_right:
            self.kill()

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames= frames
        self.frame_index=0 
        self.animation_speed = 10
        super().__init__(pos, self.frames[self.frame_index], groups) #position, surf, group

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index)% len(self.frames)]

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200,func= self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self,dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
            self.constraint()

class Bat(Enemy):
    def __init__(self, frames, pos, groups,speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude= randint(500,600)
        self.frequency =randint(300,600)
    def move(self,dt):
        self.rect.x -=self.speed * dt
        self.rect.y +=sin(pygame.time.get_ticks()/self.frequency) * self.amplitude * dt
    def constraint(self):
        if self.rect.right <= 0:
            self.kill()
        
class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(150,200)
        self.direction = 1
    def move(self,dt):
        self.rect.x += self.direction * self.speed * dt
    def constraint(self):
        if self.rect.right > self.main_rect.right or self.rect.left < self.main_rect.left:
            self.direction*=-1
            self.frames= [pygame.transform.flip(surf,True,False) for surf in self.frames]

        

class Player(AnimatedSprite):
    def __init__(self, pos, groups,collision_sprites,frames,create_bullet):
        super().__init__(frames['right'], pos, groups)
        self.all_frames = frames 
        self.facing_right = True
        self.direction = pygame.math.Vector2()
        self.speed = 400 
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.on_floor = False
        self.create_bullet = create_bullet
        self.shoot_timer = Timer(500)
        self.health = 6  
        self.is_vulnerable = True
        self.hit_timer = Timer(600, func=self.make_vulnerable)
        self.jump = pygame.mixer.Sound(join('assets','audio','jump.mp3'))

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -20
            self.jump.play()
            
        if keys[pygame.K_SPACE] and not self.shoot_timer:
            self.create_bullet(self.rect.midright if self.facing_right else self.rect.midleft,1 if self.facing_right else -1)
            self.shoot_timer.activate()

    def move(self,dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.on_floor= False
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y 
        
        self.collision('vertical')

    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0 : self.rect.right = sprite.rect.left
                    if  self.direction.x < 0 : self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0 : 
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    if  self.direction.y < 0 : self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def animate(self, dt):

        current_frames = self.all_frames['right'] if self.facing_right else self.all_frames['left']
        if self.direction.x:
            self.frame_index+=self.animation_speed * dt
        else:
            self.frame_index = 0
        self.image = current_frames[int(self.frame_index) % len(current_frames)]

    def make_vulnerable(self):
        self.is_vulnerable = True

    def get_damage(self, amount):
        if self.is_vulnerable:
            self.health -= amount
            self.is_vulnerable = False
            self.hit_timer.activate()    
        
    def update(self, dt):
        self.shoot_timer.update() 
        self.hit_timer.update()  
        self.input()
        self.move(dt)   
        self.animate(dt)

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, heart_type, frames, groups):
        super().__init__(groups)
        self.frames = frames 
        self.image = self.frames[heart_type]
        self.rect = self.image.get_frect(topleft = pos)

    def update_type(self, heart_type):
        self.image = self.frames[heart_type]        
                       
class Flower(Sprite):
    def __init__(self, pos, surf, groups):
        scaled_surf = pygame.transform.scale_by(surf, 2) 
        super().__init__(pos, scaled_surf, groups)
        self.rect = self.image.get_rect(midbottom = (pos[0] + TILE_SIZE//2, pos[1] + TILE_SIZE))

class Pika(Sprite):
    def __init__(self, pos, frames, groups,collision):
        super().__init__(pos, frames['normal'], groups)
        self.rect = self.image.get_frect(bottomleft = pos)
        self.frames = frames
        self.sad_timer = 0
        self.happy_timer = 0
        self.check_end = False

    def update(self, dt):
        if self.sad_timer> 0:
            self.sad_timer -= dt
        elif self.happy_timer> 0:
            self.happy_timer -= dt
        else:
            self.image = self.frames['normal']




        
    