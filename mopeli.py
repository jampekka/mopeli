# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:10:09 2021

@author: t
"""
import numpy as np
import pygame
from sys import exit





YDIM = 1080
XDIM = 1920

# precalculate to avoid gazillion (slow) divisions
XDIM2 = XDIM/2
YDIM2 = YDIM/2

HORIZONTAL_FOV = 80
DEGREES_PER_PIX = HORIZONTAL_FOV/XDIM
PIX_PER_DEGREE = XDIM / HORIZONTAL_FOV

# coordinates:  X,Y refer to screen pixels, 0 0 is left upper corner
#
X=np.arange(XDIM)
Y=np.arange(YDIM)

# VX, VY coordinates have origin at the screen center and values refer to viewing angle from the center

VX=(X-XDIM/2)*DEGREES_PER_PIX
VY=-(Y-YDIM/2)*DEGREES_PER_PIX


# transform viewing angle coordinates to screen coordinates

def sx(x):
    return round(x*PIX_PER_DEGREE + XDIM2)

def sy(y):
    return round(y*PIX_PER_DEGREE + YDIM2)

def sc(x,y):
    return (round(x*PIX_PER_DEGREE + XDIM2),round(y*PIX_PER_DEGREE + YDIM2))




# main

pygame.init()
pygame.font.init()


screen = pygame.display.set_mode((XDIM,YDIM))
pygame.display.set_caption('Mopeli')

clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active = False
                print("peli loppuu!")


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                print("peli alkaa!")


    if game_active:
        
        # print("peli käy")
        screen.fill((0, 0, 0))
                  
        # player.draw(screen)
        # player.update()
   
        # orc_group.draw(screen)
        # orc_group.update()
   
        # game_active = collision_sprite()
         
    else:
                
        screen.fill((0,0,0))
        myfont = pygame.font.SysFont('arial', 30)
       
        welcome_surface = myfont.render('Welcome to mopeli, press space to start',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
       
        screen.blit(welcome_surface,welcome_surface_rect)

        
    pygame.display.update()
    clock.tick(120)
        

