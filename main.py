from turtle import position
import pygame
import os
import random
import math

pygame.font.init() #initialize font
pygame.mixer.init() #initialize sound 

WIDTH, HEIGHT = 600, 1000 #Window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Initialize Window
GAME_NAME = 'Ball Launcher'
pygame.display.set_caption(GAME_NAME)

#Timing Values
FPS = 60
BALL_VEL = 10

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
INDIGO = (20,10,40)
ORANGE = (255, 165, 0)

#Dimensions
BALL_SCALE = 20
CROSSHAIR_SCALE = 50
CROSSHAIR_LINE_LENGTH = 300
MIN_ANGLE = 25
ANCHOR_Y = (HEIGHT*.90)
ENEMY_WIDTH, ENEMY_HEIGHT = 100,100

#IMPORT IMAGES
# Ex: PLAYER_SPRITE = pygame.image.load(os.path.join('path','to','image'))
BG_TILE = pygame.image.load(os.path.join('Images','grass.jpg'))
CROSSHAIR_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Images','crosshair_1.png')),(CROSSHAIR_SCALE, CROSSHAIR_SCALE))
DEFAULT_BALL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Images','white_ball.png')),(BALL_SCALE, BALL_SCALE))

#AUDIO
# Ex: PLAYER_HIT_SOUND = pygame.mixer.Sound(os.path.join('path', 'to', 'audio'))

#BOUNDRIES
# BORDER_WIDTH = 10
# BORDER = pygame.Rect(WIDTH//2-BORDER_WIDTH//2,0,BORDER_WIDTH,HEIGHT)

#TEXT
# WINNER_FONT = pygame.font.SysFont('Ariel', 80)
# TEXT_PADDING = 15

class Ball(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, launch_timer):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = DEFAULT_BALL_IMAGE
        self.rect = pygame.Rect(spawn_x, spawn_y, BALL_SCALE, BALL_SCALE)
        self.mask = pygame.mask.from_surface(self.image)
        self.launch_timer = launch_timer
        self.x = spawn_x
        self.y = spawn_y
        self.direction_x = 1 #for LEFT: 1, for RIGHT: -1
        self.direction_y = 1 #for UP: 1, for DOWN: -1

    def calculate_movement(self,crosshair_angle):
        '''
        Calculate the distance required to move on x and y planes using BALL_VEL and crosshair_angle. 
        Then calculate the new x,y coordinates by finding the difference from the old coordinates and the distance to travel. 
        
        EX:
        BALL_VEL = 10           <--- This is the hypotenuse
        crosshair_angle = 50    <--- Angle in degrees

        x_movement -> cos(50) = x/10 -> cos(50)*10 = x -> x = 6.427876096865393
        y_movement -> sin(50) = x/10 -> sin(50)*10 = x -> x = 7.66044443118978

        self.x = self.x - x_movement * self.direction_x  <--- self.direction_x (LEFT = 1, for RIGHT = -1)
        self.y = self.y - y_movement * self.direction_y  <--- self.direction_y (UP = 1, for DOWN = -1)
        '''
        print('ANGLE')
        print(crosshair_angle)
        print('X Before')
        print(self.x)
        print('Y Before')
        print(self.y)
        x_movement = math.cos(math.degrees(crosshair_angle))*BALL_VEL
        y_movement = math.sin(math.degrees(crosshair_angle))*BALL_VEL
        self.x = self.x - x_movement*self.direction_x
        self.y = self.y - y_movement*self.direction_y
        print('X Movement')
        print(x_movement)
        print('X After')
        print(self.x)
        print('Y Movement')
        print(y_movement)
        print('Y After')
        print(self.y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image: pygame.Surface, spawn_x, spawn_y, hp=10):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = enemy_image
        self.rect = pygame.Rect(spawn_x, spawn_y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = hp

    def take_damage(self, damage_amount):
        self.hp -= damage_amount
        if self.hp < 0: #Ensure HP doesn't drop to negatives value
            self.hp = 0
            
class Game(object):
    def __init__(self):
        self.anchor_x = WIDTH//2
        self.anchor_y = ANCHOR_Y
        self.crosshair_x = self.anchor_x
        self.crosshair_y = self.anchor_y
        self.crosshair_angle = 90
        self.balls = []
        self.shooting = False
        self.game_setup()
        self.main()

    def game_setup(self): 
        '''Resets game values after restart'''
        self.anchor_x = WIDTH//2
        self.anchor_y = ANCHOR_Y
        self.shooting = False
        ball = Ball(self.anchor_x,self.anchor_y,0)
        self.balls = [ball]

    def handle_collisions(self):
        '''
        Handle collisions of all objects
        
        Example for rectangle collision:
        if rect_obj.colliderect(other_rect_obj):
            <handle action here>

        Example for sprite collision:
        if pygame.sprite.spritecollide(sprite_1,sprite_1,False,pygame.sprite.collide_mask):
            <handle action here>
        '''
        pass

    def draw_window(self):
        '''
        Draw the game window and objects. Must end with pygame.display.update()

        Example of drawing a surface:
        WIN.blit(surface_image,(position_x,position_y))

        Example of drawing a rectangle:
        pygame.draw.rect(WIN, rgb_color, rect_obj)
        '''
        self.render_tile_background(BG_TILE)
        if self.shooting == True:
            #Draw ball moving at BALL_VEL towards crosshair
            for ball in self.balls:
                ball.launch_timer -= 1
                if ball.launch_timer < 0:
                    ball.calculate_movement(self.crosshair_angle)
                    WIN.blit(ball.image,(ball.x-BALL_SCALE//2,ball.y-BALL_SCALE//2))
        else:
            self.draw_ball_crosshair()

        pygame.display.update()

    def main(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN: #Launch Balls
                    self.shooting = True            
            self.handle_collisions()
            self.draw_window()

    def render_tile_background(self, tile_image: pygame.Surface):
        tile_width = tile_image.get_width()
        tile_height = tile_image.get_height()
        num_width = WIDTH % tile_width
        num_height = HEIGHT % tile_height
        for bg_row in range(0,num_height):
            for bg_column in range(0,num_width):
                WIN.blit(tile_image,(bg_row*tile_height,bg_column*tile_width))

    def draw_ball_crosshair(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        cursor_distance_x = abs(self.anchor_x-mouse_x) #ADJACENT side
        cursor_distance_y = abs(self.anchor_y-mouse_y) #OPPOSITE side
        if cursor_distance_x == 0:
            self.crosshair_angle = 90
        else:
            self.crosshair_angle = math.degrees(math.atan(cursor_distance_y/cursor_distance_x)) # Angle = tan(opposite/adjacent)
            if self.crosshair_angle < 30:
                self.crosshair_angle = 30
            else:
                self.crosshair_angle = int(self.crosshair_angle)
        if self.crosshair_angle >= MIN_ANGLE and self.anchor_y>mouse_y: 
            self.crosshair_x = mouse_x
            self.crosshair_y = mouse_y
        max_x = int(math.cos(math.radians(self.crosshair_angle))*CROSSHAIR_LINE_LENGTH)
        max_y = int(math.sin(math.radians(self.crosshair_angle))*CROSSHAIR_LINE_LENGTH)
        if mouse_x > self.anchor_x:
            max_x = max_x*-1
            for ball in self.balls:
                ball.direction_x = -1
        else:
            for ball in self.balls:
                ball.direction_x = 1
        WIN.blit(CROSSHAIR_IMAGE,((self.anchor_x-max_x)-CROSSHAIR_SCALE//2,(self.anchor_y-max_y)-CROSSHAIR_SCALE//2))
        pygame.draw.line(WIN,WHITE,(self.anchor_x,self.anchor_y),(self.anchor_x-max_x,self.anchor_y-max_y))

if __name__ == '__main__':
    game = Game()
    game.main()