# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:10:09 2021

@author: t
"""
from __future__ import division

#import numpy as np
import pygame
from sys import exit
from random import randint, choice



YDIM = 1080
XDIM = 1920

FPS = 60


# precalculate to avoid gazillion (slow) divisions
XDIM2 = XDIM/2
YDIM2 = YDIM/2

HORIZONTAL_FOV = 80
PIX_PER_DEGREE = XDIM / HORIZONTAL_FOV


# transform viewing angle coordinates to screen coordinates

def sx(x):
    return round(x*PIX_PER_DEGREE + XDIM2)

def sy(y):
    return round(-y*PIX_PER_DEGREE + YDIM2)

def sc(x,y):
    return (round(x*PIX_PER_DEGREE + XDIM2),round(-y*PIX_PER_DEGREE + YDIM2))

def sw(x):
    #transform width 
    return round(x*PIX_PER_DEGREE)


class Orc(pygame.sprite.Sprite):
     def __init__(self,x0,y0,speed):
        super().__init__()
        col = pygame.Color(255, 255, 255) 
        
        # circle radius given as viewing angle (degrees)
        size = 3
        
        
        self.speed = speed
        
        self.image = pygame.Surface([sw(size),sw(size)])
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image,col,(sw(size)//2,sw(size)//2),sw(size)//2)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(x0,y0))

     def update(self):
        
        self.rect.x += sw(self.speed) 
        self.flip()

     def flip(self):
        if self.rect.x >= sx(40):
            self.rect.x = sx(-40)
        elif self.rect.x < sx(-40):
            self.rect.x = sx(40)

# main

pygame.init()
pygame.font.init()


screen = pygame.display.set_mode((XDIM,YDIM))
pygame.display.set_caption('Mopeli')

clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

n_orcs = 6


orclist = []
for i in range(n_orcs):
    speed = choice([-1,1])*randint(10,50)/100
    orclist.append( Orc(sx(randint(-40,40)),sy(randint(-21,21)),speed))
                   
                   
orc_group = pygame.sprite.Group()
orc_group.add(orclist)



# road bar
road_surf = pygame.Surface( (sw(1),YDIM) )
YELLOW = pygame.Color(255, 255, 0)
road_surf.fill(YELLOW)
road_rect = road_surf.get_rect(center = sc(0,0))

pressed = 0 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active = False
                print('peli loppuu!')
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print('nappi pohjassa')
                pressed = 1
                
                
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pressed = 0
                # print('nappi ylös')
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                print("peli alkaa!")


    if game_active:
        
        # print("peli käy")
        screen.fill((0, 0, 0))
        
        if pressed:
            screen.blit(road_surf, road_rect)
        
        orc_group.update()
        orc_group.draw(screen)        
                        
         
    else:
                
        screen.fill((0,0,0))
        myfont = pygame.font.SysFont('arial', 30)
       
        welcome_surface = myfont.render('Welcome to mopeli, press space to start',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
       
        screen.blit(welcome_surface,welcome_surface_rect)

        
    pygame.display.update()
    clock.tick(FPS)
        

