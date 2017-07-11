# -*- coding: utf-8 -*-
# -----------------------------------
# Life game
# Copyright (c) 2017 Kazuki Minemura
# Written Kazuki Minemura
# ----------------------------------


import pygame
from pygame.locals import * # import defined values
import sys
import random
import matplotlib.pyplot as plt


SCREEN_SIZE = Rect(0, 0, 840,480) # tuple
CELL_SIZE = 10
NUM_ROW = SCREEN_SIZE.height / CELL_SIZE # row in surface
NUM_COL = (SCREEN_SIZE.width - 200) / CELL_SIZE # colmun in surface
DEAD, ALIVE_R, ALIVE_B, ALIVE_G = 0, 1, 10, 100
RAND_LIFE_R, RAND_LIFE_B, RAND_LIFE_G = 0.1, 0.9, 0.75


class lifegame:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE.size)
        pygame.display.set_caption('Life game v1 music:魔王魂')
        self.font = pygame.font.SysFont(None, 20)

        self.field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0 # generation
        self.pop_r = 0
        self.pop_w = 0
        self.run = False
        # initialize cell
        self.clear()
        self.rand()

        pygame.mixer.music.load("game_maoudamashii_1_battle34.mp3")
        pygame.mixer.music.play(-1)

        # main loop
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.birth = 0
            self.death = 0

            screen.fill((0,0,0))# fill in surface with green
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
                    elif event.key == K_r:
                        self.clear()
                        self.rand()


    def clear(self):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = DEAD

    def rand(self):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                clss = random.random()
                if clss < RAND_LIFE_R:
                    self.field[y][x] = ALIVE_R
                    self.pop_r += 1
                elif clss > RAND_LIFE_B:
                    self.field[y][x] = ALIVE_B
                    self.pop_w += 1
                #elif clss > RAND_LIFE_G:
                #    self.field[y][x] = ALIVE_G

    def update_cell(self):
        next_field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        next_pop_r = 0
        next_pop_w = 0
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

                num_r = num_alive_cells%10
                num_b = num_alive_cells/10
                num_g = 0
                if num_r > num_b and num_r >= num_g:
                    if num_r == 2: # keep
                        next_field[y][x] = self.field[y][x]
                        next_pop_r += 1
                    elif num_r == 3 or num_r == 4: # birth
                        next_field[y][x] = ALIVE_R
                        self.birth += 1
                        next_pop_r += 1
                    elif num_r > 4:
                        next_field[y][x] = DEAD
                        self.death += 1
                elif num_b > num_r and num_b >= num_g:
                    if num_b == 2: # keep
                        next_field[y][x] = self.field[y][x]
                        next_pop_w += 1
                    elif num_b == 3 or num_b == 4: # birth
                         next_field[y][x] = ALIVE_B
                         next_pop_w += 1
                         self.birth += 1
                    elif num_b > 4:
                        next_field[y][x] = DEAD
                        self.death += 1
                #lif num_g >= num_r and num_g >= num_b:
                #    if num_g == 2: # keep
                #        next_field[y][x] = self.field[y][x]
                #    elif num_g == 3: # birth
                #        next_field[y][x] = ALIVE_G
                #    else:
                #        next_field[y][x] = DEAD

        self.field = next_field
        self.generation += 1
        self.pop_r = next_pop_r
        self.pop_w = next_pop_w

    def draw_cell(self, screen):
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == ALIVE_R:
                    pygame.draw.rect(screen, (255,0,0), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                elif self.field[y][x] == ALIVE_B:
                    pygame.draw.rect(screen, (255,255,255), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
            #    elif self.field[y][x] == ALIVE_G:
            #        pygame.draw.rect(screen, (0,255,0), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                #elif self.field[y][x] == DEAD:
                #    pygame.draw.rect(screen, (0,0,0), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))

                # draw grid
                pygame.draw.rect(screen, (50,50,50), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE), 1)
        # game information
        screen.blit(self.font.render("generation:%d" % self.generation, True, (0,255,0)), (645,0))
        screen.blit(self.font.render("space : birth/kill: %d/%d" % (self.birth, self.death), True, (0,255,0)), (645,20))
        screen.blit(self.font.render("population R: %d" % (self.pop_r), True, (0,255,0)), (645,40))
        pygame.draw.rect(screen, (255,0,0), Rect(645,60,(self.pop_r*200)/(NUM_ROW*NUM_COL),15))
        screen.blit(self.font.render("population W: %d" % (self.pop_w), True, (0,255,0)), (645,80))
        pygame.draw.rect(screen, (255,255,255), Rect(645,100,(self.pop_w*200)/(NUM_ROW*NUM_COL),15))

if __name__ == '__main__':
    lifegame()
