# -----------------------------------
# Life game
# Copyright (c) 2017 Kazuki Minemura
# Written Kazuki Minemura
# ----------------------------------

import pygame
from pygame.locals import * # import defined values
import sys
import random


SCREEN_SIZE = Rect(0, 0, 640,480) # tuple
CELL_SIZE = 5
NUM_ROW = SCREEN_SIZE.height / CELL_SIZE # row in surface
NUM_COL = SCREEN_SIZE.width / CELL_SIZE # colmun in surface
DEAD, ALIVE_R, ALIVE_B = 0, 1, 10
RAND_LIFE_R, RAND_LIFE_B = 0.2, 0.8

class lifegame:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE.size)
        pygame.display.set_caption('Life game v1')
        self.font = pygame.font.SysFont(None, 16)

        self.field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.run = False
        # initialize cell
        self.clear()
        self.rand()

        # main loop
        while True:
            #screen.fill((0,255,0))# fill in surface with green
            if self.run:
                self.update_cell()
            self.draw_cell(screen)
            pygame.display.update() # update window

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_s:
                        self.run = not self.run


    def clear(self):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = DEAD

    def rand(self):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if random.random() < RAND_LIFE_R:
                    self.field[y][x] = ALIVE_R
                elif random.random() > RAND_LIFE_B:
                    self.field[y][x] = ALIVE_B

    def update_cell(self):
        next_field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if x==0 or x==NUM_COL-1 or y==0 or y==NUM_ROW-1:
                    num_alive_cells = 0;
                else:
                    sum = 0;
                    sum += self.field[y-1][x-1]
                    sum += self.field[y-1][x]
                    sum += self.field[y-1][x+1]
                    sum += self.field[y][x-1]
                    sum += self.field[y][x+1]
                    sum += self.field[y+1][x-1]
                    sum += self.field[y+1][x]
                    sum += self.field[y+1][x+1]
                    num_alive_cells = sum

                num_r = num_alive_cells % 10
                num_b = (num_alive_cells/10)
                if num_r >= num_b:
                    if num_r == 2: # keep
                        next_field[y][x] = self.field[y][x]
                    elif num_r == 3: # birth
                        next_field[y][x] = ALIVE_R
                    else:
                        next_field[y][x] = DEAD
                else:
                    if num_b == 2: # keep
                        next_field[y][x] = self.field[y][x]
                    elif num_b == 3: # birth
                        next_field[y][x] = ALIVE_B
                    else:
                        next_field[y][x] = DEAD

        self.field = next_field

    def draw_cell(self, screen):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == ALIVE_R:
                    pygame.draw.rect(screen, (255,0,0), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                elif self.field[y][x] == ALIVE_B:
                    pygame.draw.rect(screen, (0,0,255), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                elif self.field[y][x] == DEAD:
                    pygame.draw.rect(screen, (0,0,0), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))

                # draw grid
                pygame.draw.rect(screen, (50,50,50), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE), 1)

if __name__ == '__main__':
    lifegame()
