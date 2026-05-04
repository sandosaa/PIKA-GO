from settings import * 
from sprites import *
from groups import AllSprites
from support import *
from settime import Timer
from math import sin
from random import randint
from heartmanage import *
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pika Go!')
        self.clock = pygame.time.Clock()
        self.running = True
        self.count = 0
        
        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.flower_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.heart_sprites = pygame.sprite.Group()
        

        self.load_assests()
        self.setup()
        self.health_manager = HealthManager(self.heart_frames, self.heart_sprites)
        self.bat_timer = Timer(2000,func=self.create_bat,autostart=True,repeat=True)
       

    def create_bat(self):
        Bat(self.bat_frames,(self.level_width+ WINDOW_WIDTH,randint(0,self.level_height)),(self.all_sprites,self.enemy_sprites),randint(300,500))

    def create_bullet(self,pos,direction):
        Bullet(self.bullet_surf,pos,direction,(self.all_sprites,self.bullet_sprites))
        Fire(pos,self.fire_surf,self.all_sprites,self.player)
        self.audio['shooting'].play()

    def load_assests(self):
        self.player_frames = {'right':import_folder('assets','images','player','right'),
                              'left':import_folder('assets','images','player','left')}
        self.heart_frames = {
            'full': import_image('assets','images', 'heart', 'full'),
            'half': import_image('assets','images', 'heart', 'half'),
            'empty': import_image('assets','images', 'heart', 'empty')
        }
        self.pika_frames = {
            'normal':import_image('assets','images','pika','normal'),
            'sad':import_image('assets','images','pika','sad'),
            'happy':import_image('assets','images','pika','happy')
        }
        self.font = pygame.font.Font(join('assets',"font","deltarune.ttf"),40)
        self.font_mes = pygame.font.Font(join('assets',"font","deltarune.ttf"),30)
        self.bullet_surf = import_image('assets','images','gun','bullet',transform=True,scale=(35,25))
        self.fire_surf = import_image('assets','images','gun','fire',transform=True,scale=(25,25))
        self.bee_frames = import_folder('assets','images','enemies','bee')
        self.bat_frames = import_folder('assets','images','enemies','bat')
        self.worm_frames = import_folder('assets','images','enemies','worm')
        self.background = import_image('assets','images','mountain', transform=True, scale=(WINDOW_WIDTH+80, WINDOW_HEIGHT+100))
        self.audio= audio_importer('assets','audio')

    def score(self):
        self.text_surf = self.font.render('SCORE: '+ str(self.count),True, "#FFFFFF")
        self.text_rect = self.text_surf.get_frect(topleft= (45,20))
        self.display_surface.blit(self.text_surf,self.text_rect)
 

    def setup(self):
        tmx_map = load_pygame(join('assets','data','maps',"world2.tmx"))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        for x,y,image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,(self.all_sprites,self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Flowers'):
            Flower((obj.x,obj.y),obj.image,(self.all_sprites,self.flower_sprites))

        for obj in tmx_map.get_layer_by_name('Entities'):

            if obj.name == 'Pika':
                self.pika = Pika((obj.x,obj.y),self.pika_frames,self.all_sprites,self.collision_sprites)
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites,self.player_frames,self.create_bullet)
            if obj.name == 'Worm':
                Worm(self.worm_frames,pygame.FRect(obj.x,obj.y,obj.width,obj.height),(self.all_sprites,self.enemy_sprites))

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet,self.enemy_sprites,False,pygame.sprite.collide_mask)
            if sprite_collision:
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
                    self.audio['enemy_damage'].play()

        if pygame.sprite.spritecollide(self.player,self.enemy_sprites,False,pygame.sprite.collide_mask):
            self.player.get_damage(1)
            self.health_manager.update_hearts(self.player.health)
            self.audio['damage'].play()

        if self.player.rect.top > self.level_height:
            self.player.get_damage(1)
            self.health_manager.update_hearts(self.player.health)
            self.player.rect.topleft = (320, 320) 
            self.player.direction.y = 0
            self.audio['damage'].play()

        collided_flowers = pygame.sprite.spritecollide(self.player, self.flower_sprites, True,pygame.sprite.collide_mask)
        if collided_flowers:
            self.count+=10
            self.audio['flower'].play()

        if self.player.health <= 0:
            self.text_surf = self.font.render('GAME OVER', True, 'white')
            self.display_surface.blit(self.text_surf, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2))
            pygame.display.update()
            self.audio['lose'].play()
            pygame.time.wait(2800) 
            self.running = False   

        if self.player.rect.colliderect(self.pika.rect): 
            self.player.rect.x -= 20
            if self.count<200:
                self.pika.sad_timer =  2.0
                self.audio['sad'].play()
            else:
                self.pika.happy_timer = 3.0
                self.audio['happy'].play()
                
                

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

           
            self.bat_timer.update()
            self.all_sprites.update(dt)
            self.collision()
            self.display_surface.blit(self.background, (0,0)) 
            self.all_sprites.draw(self.player.rect.center)

            if self.pika.sad_timer > 0:
                self.pika.image = self.pika.frames['sad']
                self.text_surf = self.font_mes.render('YOU HAVE TO COLLECT 20 FLOWERS AT LEAST',True,'#ffffff')  
                self.text_rect = self.text_surf.get_frect(center= (WINDOW_WIDTH/2 , WINDOW_HEIGHT/2+100))
                self.display_surface.blit(self.text_surf, self.text_rect) 
            if self.pika.happy_timer > 0:
                self.pika.image = self.pika.frames['happy']
                self.text_surf = self.font_mes.render('YOU WIN THE GAME AND PIKA IS SO HAPPY!',True,'#ffffff')  
                self.text_rect = self.text_surf.get_frect(center= (WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100))
                self.display_surface.blit(self.text_surf, self.text_rect)  
                self.pika.check_end = True
            elif self.pika.check_end:
                self.running = False    

            self.heart_sprites.draw(self.display_surface)
            self.score()

            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 