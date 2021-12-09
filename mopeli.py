# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:10:09 2021
developed with pygame 2.0.1 (SDL 2.0.14, Python 3.8.10)
@author: t
"""


#import numpy as np
import pygame
from sys import exit, argv
from random import random,randint, choice
from scipy.stats import maxwell
import csv
import shelve
import pandas as pd 


#XDIM=960
#YDIM = 540

YDIM = 1080
XDIM = 1920
FPS = 60

XDIM2 = XDIM/2
YDIM2 = YDIM/2

trial_length = 60 


LOGFILE = 'trial_log.csv'
FRAMELOGFILE= 'frame_log.csv'
active_logfile = LOGFILE
active_framelogfile = FRAMELOGFILE

# transform natural coordinates to screen coordinates

# -1,1 -> xdim, ydim
def sx(x):
    return (x * 0.5 * XDIM + XDIM2)

def sy(y):
    return (-y * 0.5 * YDIM + YDIM2)


def isx(x):
    # xdim ->  -1, 1
    return 2*(x - XDIM2)/XDIM
    

def sc(x,y):
    return (sx(x), sy(y))

def sw(x):
    #transform width 
    return (x * 0.5 * XDIM)

def sh(y):
    # transform height
    return (y * 0.5 * YDIM)

def writelog(*args):
    with open(active_logfile, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(args)

class Orc(pygame.sprite.Sprite):
    # orcs that die when travelling off screen
    # position coordinates: screen edges are at -1 and 1
    # speed is given in halfscreens/second
    
    def __init__(self,x0,y0,vx,vy):
       super().__init__()
       col = pygame.Color(255, 255, 255) 
       
       size = 0.075
               
       self.size = sw(size)
       self.x0 = x0
       self.y0 = y0
       
       # save initial values (these are halfscreen-coordinates)
       self.vx0 = vx
       self.vy0 = vy
       
       
       self.vx = sw(vx)/FPS
       self.vy= sw(vy)/FPS

       
       self.image = pygame.Surface([self.size,self.size])
       self.image.set_colorkey((0,0,0))
       pygame.draw.circle(self.image,col,(self.size//2,self.size//2),self.size//2)
       self.image.convert_alpha()
       self.rect = self.image.get_rect(center=(sx(self.x0),sy(self.y0)))
       
       # since rect.x is forced int, we need these variables
       # to keep "precise" location information
       self.float_x = float(self.rect.x)
       self.float_y = float(self.rect.y)
       
       self.created_time = pygame.time.get_ticks() - start_time
       writelog(self.created_time,self.x0,self.y0,self.vx0,self.vy0)
              
    
    def update(self):
        self.float_x += self.vx
        self.float_y += self.vy
        
        self.rect.x = round(self.float_x)
        self.rect.y = round(self.float_y)
        
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
       
       size =0.075
       
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
       time = pygame.time.get_ticks() -start_time
       writelog(time,self.x0,self.y0,self.vx0,self.vy0)

        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.flip()
          
    def setspeeds(self):
        if self.mode==1:
            self.vy0=0
            self.vx0 = -self.x0 * maxwell.rvs(loc=0,scale =self.a)
            self.vx = sw( self.vx0 ) /FPS
            self.vy = 0
            
        if self.mode==2:
            self.vx0 = -self.x0 * maxwell.rvs(loc=0,scale =self.a)
            self.vy0 = choice([-1,1]) * maxwell.rvs(loc=0,scale =self.a)
            
            self.vx = sw( self.vx0 ) /FPS
            self.vy = sw( self.vy0 ) /FPS
        
    
    def flip(self):
        time = pygame.time.get_ticks() -start_time
        if self.rect.x >= XDIM:
            self.setspeeds()
            if self.vx > 0:
                self.rect.x = 1
            else:
                self.rect.x = XDIM-1
            
            self.rect.y = randint(0,YDIM-self.size)
            
            writelog(time,self.x0,self.y0,self.vx0,self.vy0)
            
        elif self.rect.x < (0-self.size):
            self.setspeeds()
            if self.vx > 0:
                self.rect.x = 1
            else:
                self.rect.x = XDIM-1
            self.rect.y = randint(0,YDIM-self.size)
            writelog(time,self.x0,self.y0,self.vx0,self.vy0)
            
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
       self.image = pygame.Surface( (sw(1/40),YDIM) )
       
       self.image.fill(self.col)
       self.image.convert_alpha()
       self.rect = self.image.get_rect(center = sc(0,0))
       
    def setcolor(self,col):
        self.col=col
        self.image.fill(self.col)
        
       
     
        
# def create_orcs(n_orcs,mode):
    
#     orclist = []
#     for i in range(n_orcs):
#         xspeed = choice([-1,1])*randint(10,50)/100
#         if mode ==2:
#             yspeed = choice([-1,1])*randint(10,50)/100
#         else:
#             yspeed = 0
            
#         orclist.append( Orc(sx(randint(-40,40)),sy(randint(-21,21)),xspeed,yspeed))
#     return orclist

def create_orcs_random(n_orcs,mode):
        
    orclist = []
    a=0.5
    for i in range(n_orcs):
        
        orclist.append( Orc_random(mode, a))
    return orclist    

def getstring(message):
    name = ""
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN:
                    return(name)
                else: 
                    name += evt.unicode
            elif evt.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        welcome_surface = myfont.render(message,False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0.1))
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
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0.9))
        screen.blit(welcome_surface,welcome_surface_rect)
        for k in dsort.keys():
            i+=1
            welcome_surface = myfont.render( (k + ':   ' + str(dsort[k]))  ,False,(128,128,128) )
            welcome_surface_rect = welcome_surface.get_rect(center = sc(0,(0.8-(i*0.1))))
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
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,-0.1))
        
        screen.blit(welcome_surface,welcome_surface_rect)
        
        pygame.display.update()
        
    
def start_countdown():
    while True:
        for evt in pygame.event.get():            
            if evt.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                return
        screen.fill((0, 0, 0))
        welcome_surface = myfont.render('Press space to start the game',False,(128,128,128) )        
        welcome_surface_rect = welcome_surface.get_rect(center = sc(0,0))
        screen.blit(welcome_surface,welcome_surface_rect)
        pygame.display.flip()
        
    
def readscene():
    ok = 0  # return null if cant read scenefile.. 
    while not ok:
        message = 'enter scenary file (default: scene1.csv)'
        scenefile = getstring(message)
        
        if not scenefile:
            scenefile = 'scene1.csv'
        try:
            df = pd.read_csv(scenefile,names=['time','x0','y0','vx0','vy0'])
            print('read ' + scenefile)
            ok=1
        
        except:
            print('problem reading ' + scenefile)
        #     ok=0
        df = df[df['x0']<888]
    return df

    
# main

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((XDIM,YDIM), flags=pygame.NOFRAME | pygame.SCALED)
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


myfont = pygame.font.SysFont('arial', 30)

#scores
d=shelve.open('score.txt')
scenarios_left = argv[1:]
scenefile = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
        # mainmenu
            if event.type == pygame.KEYDOWN or len(scenarios_left) > 0:
                scenefile = None
                if len(scenarios_left) > 0:
                    mode = 3
                    scenefile = scenarios_left.pop(0)
                    df = pd.read_csv(scenefile,names=['time','x0','y0','vx0','vy0'])
                    df = df[df['x0']<888]
                    rowindex = 0
                elif event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                elif event.key == pygame.K_3:
                    mode = 3
                    df = readscene()
                    trial_length = df['time'].iloc[-1] // 1000 + 3 
                    rowindex = 0
                elif event.key == pygame.K_h:
                    showhighscore()
                    
                if mode:
                    name = getname()
                    start_countdown()
                    start_time = pygame.time.get_ticks()
                    pressed = 1
                    #create new logfile
                    if scenefile:
                        active_logfile = scenefile + ".log"
                        active_framelogfile = scenefile + '_framelog.csv'
                    else:
                        active_logfile = LOGFILE
                        active_framelogfile = FRAMELOGFILE
                    with open(active_logfile, 'w+', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',',
                                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

                    orc_group = pygame.sprite.Group()

                    if mode < 3:
                        orc_group.add(create_orcs_random(7,mode))
                    score = 0
                    game_active = True
                    framenumber = 0
                    hit = 0
                    alreadyhit = 0
                    
                    # create dataframe for logging per frame stuff
                    maxorcs = 10
                    orccols=[]
                    for i in range(maxorcs):
                        s = str(i)    
                        orccols.extend(['x'+s,'y'+s,'vx'+s,'vy'+s])
                        
                    column_names = ['frame','time','pressed','hit','alreadyhit','score']
                    column_names.extend(orccols)
                    framelog = pd.DataFrame(columns=column_names)
                    
                    print("peli alkaa!")
                                        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active = False                
                
                print('peli loppuu!')
                mode = 0
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print('nappi pohjassa')
                if not pressed:
                    time = pygame.time.get_ticks() - start_time
                    writelog(time,888,0,0,0)
                    pressed = 1
                    
                    hit = 0 
                    alreadyhit = 0 
                                
                
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pressed = 0                
                time = pygame.time.get_ticks() - start_time
                writelog(time,999,0,0,0)
                
    if game_active:
        framenumber += 1
        time = pygame.time.get_ticks() - start_time
        
        timeleft = trial_length-time//1000
        
        if mode == 3:
            # try:
            #     row = df.iloc[rowindex]
            #     ok = 1
            # except:
                
            #     ok = 0
            #if row.time <= time and ok:
            try:
                row = df.iloc[rowindex]
                if row.time <= time:
                    print('row number: ' +str(rowindex) + ' ' + str(time))                    
                    orc_group.add( Orc(row.x0,row.y0,row.vx0,row.vy0) )
                    rowindex += 1
                ok = 1
            except:
                ok = 0
            
        
        # print("peli käy")
        screen.fill((0, 0, 0))
        
        road.sprite.setcolor("gray20")
        
        if not pressed:
            hitsprite = pygame.sprite.groupcollide(road, orc_group,False,False)
            if hitsprite:
                hit = 1
                road.sprite.setcolor('red')
            else:
                hit = 0
                alreadyhit = 0
                road.sprite.setcolor('yellow')

                # calculate score for this frame by summing ball speeds
                # ball travels half screen == 100 points
                # score increases until ball crosses midline
                
                for o in orc_group:
                    ox = isx(o.rect.center[0])
                    if (ox<0 and o.vx0>0) or (ox>0 and o.vx0<0):
                        score += abs(o.vx0)/FPS * 100
                        print(score)

            # first frame when ball hits the bar                                                    
            if hit and not alreadyhit:     
                alreadyhit = 1
                if score>100:
                    score -= 100
    
                
        road.update()
        road.draw(screen) 

        #framelog

        row = {'frame':framenumber,'time':time,'pressed':pressed,'hit':hit,'alreadyhit':alreadyhit,'score':score}
        orcrow = {}
        for i,o in enumerate(orc_group):
            ox = o.rect.center[0]
            oy = o.rect.center[1]
            orcrow.update( {'x'+str(i):ox})
            orcrow.update( {'y'+str(i):oy} )
            orcrow.update( {'vx'+str(i):o.vx} )
            orcrow.update( {'vy'+str(i):o.vy} )
        
        row.update(orcrow)        
        framelog = framelog.append(row,ignore_index=True)
        
            #screen.blit(road_surf, road_rect)
        
        
        orc_group.update()
        orc_group.draw(screen)        
        
        name_surface = myfont.render('Player: '+name,False,'gray')   
        name_surface_rect = name_surface.get_rect(topleft = (0,0))
        screen.blit(name_surface,name_surface_rect)
        
        score_surface = myfont.render('Score: ',False,'gray')
        score_surface_rect = score_surface.get_rect(topleft = (sx(-1),sy(-0.9)))
        screen.blit(score_surface,score_surface_rect)
        
        score_right_edge = score_surface_rect.midright 
        
        # coin radius 
        coinsize = 12 
        
        if(score>0):
            # 100 points == one ball width 
            l = (score/100) * 2 * coinsize 
        else:
            l=0
        coin_surface = pygame.Surface([l,coinsize*2])
        
        for i in range(100):
            pygame.draw.circle(coin_surface,'yellow',[coinsize+(coinsize*2)*i,coinsize],coinsize)
        
        coin_surface.set_colorkey((0,0,0))
        coin_surface.convert_alpha()
        coin_surface_rect = coin_surface.get_rect(midleft = score_right_edge)
        
        
        #coin_surface_rect.topright = (topr[0]+score//2,topr[1])
        
        screen.blit(coin_surface,coin_surface_rect)
               
        time_surface = myfont.render('time '+str(timeleft),False,'gray')
        time_surface_rect = score_surface.get_rect(topleft = (sx(-1),sy(0.9)))
        screen.blit(time_surface,time_surface_rect)
        

        
        #if (mode != 3 and timeleft <= 0) or (mode == 3 and not ok):
        
        if(timeleft<=0):
            framelog.to_csv(active_framelogfile)
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
        

