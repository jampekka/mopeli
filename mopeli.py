# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:10:09 2021
developed with pygame 2.0.1 (SDL 2.0.14, Python 3.8.10)
@author: t
"""


#import numpy as np
import pygame
from sys import exit
from random import random,randint, choice
from scipy.stats import maxwell
import csv
import shelve
import pandas



YDIM = 1080
XDIM = 1920
FPS = 60

XDIM2 = XDIM/2
YDIM2 = YDIM/2

HORIZONTAL_FOV = 80
PIX_PER_DEGREE = XDIM / HORIZONTAL_FOV

LOGFILE = 'trial_log.csv'


# transform natural coordinates to screen coordinates

# -1,1 -> xdim, ydim
def sx(x):
    return round(x * 0.5 * XDIM + XDIM2)

def sy(y):
    return round(-y * 0.5 * YDIM + YDIM2)


#-80,80 -> xdim,ydim

def sc(x,y):
    return (round(x*PIX_PER_DEGREE + XDIM2),round(-y*PIX_PER_DEGREE + YDIM2))

def sw(x):
    #transform width 
    return round(x*PIX_PER_DEGREE)


class Orc(pygame.sprite.Sprite):
    # orcs that die when travelling off screen
    def __init__(self,x0,y0,vx,vy):
       super().__init__()
       col = pygame.Color(255, 255, 255) 
       
       # circle radius given as viewing angle (degrees)
       size = 3
               
       self.size = sw(size)
       self.x0 = x0
       self.y0 = y0
       
       self.vx0 = vx
       self.vy0 = vy

       self.vx = sw(vx)
       self.vy= sw(vy)

       
       self.image = pygame.Surface([self.size,self.size])
       self.image.set_colorkey((0,0,0))
       pygame.draw.circle(self.image,col,(self.size//2,self.size//2),self.size//2)
       self.image.convert_alpha()
       self.rect = self.image.get_rect(center=(sx(self.x0),sy(self.y0)))
       self.created_time = pygame.time.get_ticks() - start_time
       
       self.writelog()
       
           
    def writelog(self):
        
        with open(LOGFILE, 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([self.created_time,self.x0,self.y0,self.vx0,self.vy0])           
    
    def update(self):       
       self.rect.x += self.vx
       self.rect.y += self.vy
       self.flip()
    
    def flip(self):
       if self.rect.x >= XDIM and self.vx>0:
           
           self.kill()
       elif self.rect.x < (0-self.size) and self.vx<0:
           
           self.kill()
           
       if self.rect.y <= 0:
           self.vy = -self.vy
           self.rect.y += 1
       elif self.rect.y >= (YDIM-self.size):
           self.vy = -self.vy
           self.rect.y -= 1
           
           
class Orc_random(pygame.sprite.Sprite):
    def __init__(self,mode,a):
       super().__init__()
       col = pygame.Color(255, 255, 255) 
       
       # circle radius given as viewing angle (degrees)
       size = 3
       
       self.size = sw(size)
       self.mode = mode
       self.a = a
       
       
       
       self.image = pygame.Surface([self.size,self.size])
       self.image.set_colorkey((0,0,0))
       pygame.draw.circle(self.image,col,(self.size//2,self.size//2),self.size//2)
       self.image.convert_alpha()
       
       self.x0 = choice([-1,1])
       
       self.y0 = choice([-1,1])*random()
       self.setspeeds()
       
       self.rect = self.image.get_rect( center = (sx(self.x0),sy(self.y0)) )
           
       
       
       
      
    def writelog(self):
        self.created_time = pygame.time.get_ticks() -start_time
        
        with open(LOGFILE, 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([self.created_time,self.x0,self.y0,self.vx0,self.vy0])
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.flip()
          
    def setspeeds(self):
       if self.mode==1:
           self.vy0=0
           self.vx0 = -self.x0 * maxwell.rvs(loc=0,scale =self.a)
           self.vx = sw( self.vx0 )
           self.vy = 0
           
       if self.mode==2:
           self.vx0 = -self.x0 * maxwell.rvs(loc=0,scale =self.a)
           self.vy0 = choice([-1,1]) * maxwell.rvs(loc=0,scale =self.a)
           
           self.vx = sw( self.vx0 )
           self.vy = sw( self.vy0 )
       
    
    def flip(self):
       if self.rect.x >= XDIM:
           
           self.setspeeds()
           if self.vx > 0:
               self.rect.x = 1
           else:
               self.rect.x = XDIM-1
           self.rect.y = randint(0,YDIM-self.size)
           
           self.writelog()
           
       elif self.rect.x < (0-self.size):
           self.setspeeds()
           if self.vx > 0:
               self.rect.x = 1
           else:
               self.rect.x = XDIM-1
           self.rect.y = randint(0,YDIM-self.size)
           self.writelog()
           
           
       if self.rect.y <= 0:
           self.vy = -self.vy
           self.rect.y += 1
       elif self.rect.y >= (YDIM-self.size):
           self.vy = -self.vy
           self.rect.y -= 1           
           
class Road(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__()
       self.col = 'yellow'
       self.image = pygame.Surface( (sw(1),YDIM) )
       
       self.image.fill(self.col)
       self.image.convert_alpha()
       self.rect = self.image.get_rect(center = sc(0,0))
       
    def setcolor(self,col):
        self.col=col
        self.image.fill(self.col)
        
       
     
        
def create_orcs(n_orcs,mode):
    
    orclist = []
    for i in range(n_orcs):
        xspeed = choice([-1,1])*randint(10,50)/100
        if mode ==2:
            yspeed = choice([-1,1])*randint(10,50)/100
        else:
            yspeed = 0
            
        orclist.append( Orc(sx(randint(-40,40)),sy(randint(-21,21)),xspeed,yspeed))
    return orclist

def create_orcs_random(n_orcs,mode):
        
    orclist = []
    a=0.2
    for i in range(n_orcs):
        
        orclist.append( Orc_random(mode, a))
    return orclist    

def getstring(message):
    
    name = ""
        
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt .unicode
                elif evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN:
                    return(name)
            elif evt.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        welcome_surface = myfont.render(message,False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,2))
        screen.blit(welcome_surface,welcome_surface_rect)
          
        block = myfont.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()
    return name

           
def getname():
    message = 'Please enter your name and press enter'
    name = getstring(message)
    return name

def showhighscore():
    #make sure there is some scorefile
    d=shelve.open('score.txt')
    d['nul'] = 0
    d.close()

    
    d=shelve.open('score.txt')
    dsort = dict(reversed(sorted(d.items(), key=lambda item: item[1])))
    d.close()

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                return()
            elif evt.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        screen.fill((0, 0, 0))
        i=0
        welcome_surface = myfont.render('High scores',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,11))
        screen.blit(welcome_surface,welcome_surface_rect)
        for k in dsort.keys():
            i+=1
            welcome_surface = myfont.render( (k + ':   ' + str(dsort[k]))  ,False,(128,128,128) )
            welcome_surface_rect = welcome_surface.get_rect(center = sc(0,10-i))
            screen.blit(welcome_surface,welcome_surface_rect)
            if i>10:
                break
        pygame.display.flip()
        
            
def gameover(name,score):

    d=shelve.open('score.txt')
    if name in d:
        if score > d[name] :
            d[name] = score
    else:
        d[name] = score
        
    d.close()

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:                
                    return() 
            elif evt.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        
        welcome_surface = myfont.render('Game Over,  press esc for main menu',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
        
        screen.blit(welcome_surface,welcome_surface_rect)
        
        welcome_surface = myfont.render('Score: '+ str(score),False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,-2))
        
        screen.blit(welcome_surface,welcome_surface_rect)
        
        pygame.display.update()
        
    
def start_countdown():
    screen.fill((0, 0, 0))
    delaylen = 3
    delaystart = pygame.time.get_ticks()
    while True:
        for evt in pygame.event.get():            
            if evt.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        curtime = (pygame.time.get_ticks() - delaystart) //1000
        
        countdown = delaylen - curtime
                
        welcome_surface = myfont.render('Game starts: '+ str(countdown),False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
        screen.blit(welcome_surface,welcome_surface_rect)
        pygame.display.flip()
        if countdown <=0:
           return    
    
def readscene():
    ok = 0  # return null if cant read scenefile.. 
    while not ok:
        message = 'enter scenary file (default: scene1.csv)'
        scenefile = getstring(message)
        
        if not scenefile:
            scenefile = 'scene1.csv'
        try:
            df = pandas.read_csv(scenefile,names=['time','x0','y0','vx0','vy0'])
            print('read ' + scenefile)
            ok=1
        
        except:
            print('problem reading ' + scenefile)
            ok=0
        
    return df

    
# main

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((XDIM,YDIM))
pygame.display.set_caption('Mopeli')

clock = pygame.time.Clock()
game_active = False
score = 0


# road bar
roadsprite = Road()
#road = pygame.sprite.RenderPlain(roadsprite)
road = pygame.sprite.GroupSingle(roadsprite)
mode = 0
pressed = 0 

trial_length = 60 
myfont = pygame.font.SysFont('arial', 30)

#scores
d=shelve.open('score.txt')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active = False                
                print('peli loppuu!')
                mode = 0
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print('nappi pohjassa')
                pressed = 1
                
                
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pressed = 0
                # print('nappi ylös')
                
        else:
        # mainmenu
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                elif event.key == pygame.K_3:
                    mode = 3
                    df = readscene()
                    rowindex = 0
                elif event.key == pygame.K_h:
                    showhighscore()
                    
                if mode:   
                    
                    name = getname()
                    print("peli alkaa!")
                    start_countdown()
                    start_time = pygame.time.get_ticks()
                    with open(LOGFILE, 'w+', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',',
                                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

                    
                    orc_group = pygame.sprite.Group()
                    #orc_group.add(create_orcs(6,mode))
                    if mode < 3:
                        orc_group.add(create_orcs_random(7,mode))
                    score = 0
                    game_active = True
                                        
                    
                    
                    #create file
                        
                    

    if game_active:
        time = pygame.time.get_ticks() - start_time
        
        timeleft = trial_length-time//1000
        
        if mode == 3:
            try:
                row = df.iloc[rowindex]
                ok = 1
            except:
                
                ok = 0
            if row.time <= time and ok:
                print('row number: ' +str(rowindex) + ' ' + str(time))                    
                orc_group.add( Orc(row.x0,row.y0,row.vx0,row.vy0) )
                rowindex += 1
            
        
        # print("peli käy")
        screen.fill((0, 0, 0))
        
        road.sprite.setcolor("gray20")
        if pressed:
            hit = pygame.sprite.groupcollide(road, orc_group,False,False)
            
            if hit:
                road.sprite.setcolor('red')
                score -=4
               
            else:
                road.sprite.setcolor('yellow')
                score += 1
            
        road.update()
        road.draw(screen)          
            #screen.blit(road_surf, road_rect)
        
        
        orc_group.update()
        orc_group.draw(screen)        
        
        
        
        name_surface = myfont.render('Player: '+name,False,'gray')   
        name_surface_rect = name_surface.get_rect(topleft = (0,0))
        screen.blit(name_surface,name_surface_rect)
        
        score_surface = myfont.render('score '+str(score),False,'gray')        
        score_surface_rect = score_surface.get_rect(topleft = (0,sw(1.5)))        
        screen.blit(score_surface,score_surface_rect)
        
        
        time_surface = myfont.render('time '+str(timeleft),False,'gray')
        time_surface_rect = score_surface.get_rect(topleft = (0,sw(3)))
        screen.blit(time_surface,time_surface_rect)
        
        if timeleft <= 0:
            mode = 0
            game_active = False
            gameover(name,score)
         
                     
         
    else:
                
        screen.fill((0,0,0))
       
        welcome_surface = myfont.render('Welcome to mopeli, press 1 for horizontal movement, press 2 for random movement, press 3 to read scenario file,  press h for highscores',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
       
        screen.blit(welcome_surface,welcome_surface_rect)

        pressed = 0

        
    pygame.display.update()
    clock.tick(FPS)
        

