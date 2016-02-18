#  Copyright (c) 2015 Jon Cooper
#   
#  This file is part of pygame-platformer.
#  Documentation, related files, and licensing can be found at
# 
#      <https://github.com/joncoop/color-switch>.

import pygame
import random

pygame.init()

# window settings
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Color Switch")
FPS = 60
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0 , 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# physics
GRAVITY = 1
TERMINAL_VELOCITY = 10
BOUNCE_POWER = 10

class Ball():
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.vy = 0

    def bounce(self):
        self.vy = -BOUNCE_POWER

    def get_rect(self):
        return self.rect
    
    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def update(self):
        self.rect[1] += self.vy
        self.vy += GRAVITY

        self.vy = min(self.vy, TERMINAL_VELOCITY)
    
# blocks
class Block():
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def get_rect(self):
        return self.rect;
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.rect[0] -= 3

        if self.rect[0] < -200:
            self.rect[0] += 800


class Switcher():
    def __init__(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect;
    
    def draw(self, surface):
        half_x = self.rect[2] / 2
        half_y = self.rect[3] / 2
        
        rect_ul = [self.rect[0], self.rect[1], half_x, half_y]
        rect_ur = [self.rect[0] + half_x, self.rect[1], half_x, half_y]
        rect_lr = [self.rect[0] + half_x, self.rect[1] + half_y, half_x, half_y]
        rect_ll = [self.rect[0], self.rect[1] + half_y, half_x, half_y]
        
        pygame.draw.rect(surface, RED, rect_ul)
        pygame.draw.rect(surface, YELLOW, rect_ur)
        pygame.draw.rect(surface, GREEN, rect_lr)
        pygame.draw.rect(surface, BLUE, rect_ll)

    def get_rand_color(self):
        return random.choice([RED, GREEN, BLUE, YELLOW])
    
    def update(self):
        pass

    
def intersects(a, b):
    rect1 = a.get_rect()
    rect2 = b.get_rect()

    left1 = rect1[0]
    right1 = rect1[0] + rect1[2]
    top1 = rect1[1]
    bottom1 = rect1[1] + rect1[3]

    left2 = rect2[0]
    right2 = rect2[0] + rect2[2]
    top2 = rect2[1]
    bottom2 = rect2[1] + rect2[3]

    return not (right1 < left2 or
                left1 > right2 or
                bottom1 < top2 or
                top1 > bottom2)

# game objects
ball = Ball([290, 400, 20, 20], YELLOW)

block1 = Block([0, 300, 200, 20], RED)
block2 = Block([200, 300, 200, 20], GREEN)
block3 = Block([400, 300, 200, 20], BLUE)
block4 = Block([600, 300, 200, 20], YELLOW)

block_list = [block1, block2, block3, block4]

switcher1 = Switcher([285, 100, 30, 30])
switcher2 = Switcher([285, 500, 30, 30])

switcher_list = [switcher1, switcher2]

# game loop
done = False

while not done:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.bounce()

    # game logic
    ball.update()

    for block in block_list:
        block.update()

    if ball.rect[1] > 600 - ball.rect[3]:
        ball.rect[1] = 600 - ball.rect[3]
        ball.vy = GRAVITY
        
    for block in block_list:
        if intersects(block, ball):
            if ball.color != block.color:
                if ball.rect[1] < block.rect[1]:
                    ball.rect[1] = block.rect[1] - ball.rect[3]
                    ball.vy = GRAVITY
                else:
                    ball.rect[1] = block.rect[1] + block.rect[3]
                    ball.vy = GRAVITY

    for switcher in switcher_list:
        if intersects(ball, switcher):
            ball.color = switcher.get_rand_color()
        
    #drawing
    screen.fill(BLACK)

    ball.draw(screen)

    for block in block_list:
        block.draw(screen)

    for switcher in switcher_list:
        switcher.draw(screen)
    
    # update screen
    pygame.display.update()
    clock.tick(FPS)

# close window on quit
pygame.quit ()

