
import random
import pygame
from pygame.math import Vector2
import sys

player_acc=50
cell_size=35
cell_number=20
pygame.init()


clock=pygame.time.Clock()        
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*17),vsync=1)
bg_color=(250,250,250)
black=(0,0,0)
dino_run1=pygame.transform.scale(pygame.image.load('DinoRun1.png').convert_alpha(),(cell_size*1.8,cell_size*1.8))
dino_run2=pygame.transform.scale(pygame.image.load('DinoRun2.png').convert_alpha(),(cell_size*1.8,cell_size*1.8))
dino_jump=pygame.transform.scale(pygame.image.load('DinoJump.png').convert_alpha(),(cell_size*1.8,cell_size*1.8))
dino_dead=pygame.transform.scale(pygame.image.load('DinoDead.png').convert_alpha(),(cell_size*1.8,cell_size*1.8))
cloud=pygame.transform.scale(pygame.image.load('Cloud.png').convert_alpha(),(cell_size*3,cell_size*3))
Large_Cactus=pygame.transform.scale(pygame.image.load('LargeCactus1.png').convert_alpha(),(cell_size+5,cell_size+40))
floor=pygame.transform.scale(pygame.image.load('Track.png').convert_alpha(),(cell_size*50,cell_size))
small_cactus=pygame.transform.scale(pygame.image.load('SmallCactus1.png').convert_alpha(),(cell_size+10,cell_size+30))
small_cactus2=pygame.transform.scale(pygame.image.load('SmallCactus2.png').convert_alpha(),(cell_size+10,cell_size+30))
GameOver=pygame.image.load('GameOver.png').convert_alpha()
replay_button=pygame.image.load('Reset.png').convert_alpha()

imagearray=[Large_Cactus,small_cactus,small_cactus2]
Dino_RUN=[dino_run1,dino_run2]
game_over_rect=GameOver.get_rect()
game_over_rect.center=(10*cell_size,10*cell_number)
retry_rect=replay_button.get_rect()
retry_rect.center=(cell_size*10,cell_size*10)
pygame.draw.rect(screen,pygame.Color('red'),retry_rect)

class obstacles():
    def __init__(self,x,y,imageindex):
        global imagearray
        self.pos=Vector2(x,y)
        self.index=imageindex
        self.pos_backup=Vector2(x,y)
        self.cactusrec=imagearray[self.index].get_rect()
    def draw_obstacles(self):
        global imagearray,bg_speed
        self.cactusrec.center=(self.pos.x*cell_size,self.pos.y*cell_size)
        #pygame.draw.rect(screen,pygame.Color('red'),self.cactusrec) 
        image=imagearray[self.index]
        screen.blit(image,self.cactusrec)   
        self.pos+=bg_speed
        if self.pos.x<=-5:
            self.pos=Vector2(21,14)    
     

class runner():
    def __init__(self):
        self.pos=Vector2(2,14)
        self.acc=Vector2(0,player_acc)
        self.velocity=Vector2(0,0)
        self.hitbox=dino_run1.get_rect()
        self.cooldown=150
        self.isjump=False
        self.death=False
        
    def draw_runner(self):
        global frame
        global last_update
        global currentframe_time
        global running
        self.hitbox.center=(self.pos.x*cell_size,self.pos.y*cell_size)
        #pygame.draw.rect(screen,pygame.Color('green'),self.hitbox)
        #runner_shape=pygame.Rect(self.pos.x*cell_size,self.pos.y*cell_size,cell_size+5,cell_size)
        #pygame.draw.rect(screen,pygame.Color('green'),runner_shape) 
        if currentframe_time-last_update>=self.cooldown :
            last_update=currentframe_time
            frame+=1
            if frame>=len(Dino_RUN):
                frame=0
        if running==True and self.death==False:
            screen.blit(Dino_RUN[frame],self.hitbox)
        elif self.isjump==True :
            screen.blit(dino_jump,self.hitbox) 
        elif self.death==True:
            screen.blit(dino_dead,self.hitbox)   
            
        
    def movement(self):
        global running,dt
        keys=pygame.key.get_pressed()
        if self.isjump==False:
            if keys[pygame.K_SPACE] and self.pos.y==14 and self.death==False:
                self.isjump=True
                print("jump")
                running=False
                if self.isjump==True:
                    self.velocity.y = -43
        
        self.velocity += self.acc*(dt/1000)
        self.pos += (self.velocity+0.5*self.acc*0.9)*(dt/1000)
        if self.pos.y>14:
            self.pos.y=14
            self.isjump=False
            running=True
     
floor_rect=floor.get_rect()
floor2_rect=floor.get_rect()
floor_pos=Vector2(0,14.7)
floor2_pos=Vector2(50,14.7)
bg_speed=Vector2(-0.25,0)

cactus1=obstacles(22,14,0)
cactus2=obstacles(23.4,14,0)
cactus3=obstacles(23.6,14,0)
smallcactus=obstacles(21,14,1)
smallcactus2=obstacles(21,14,2)

clusterarray=[cactus1,cactus2,cactus3]
smallarray=[smallcactus,smallcactus2,cactus1,cactus2]
small_array_backup=smallarray
r=random.randrange(0,4)

player = runner()
cloudpos = Vector2(21,random.randrange(2,9))
cloudpos2 = Vector2(25,random.randrange(2,9)) 
cloudpos3 = Vector2(35,random.randrange(2,9))
cloudpos4 = Vector2(30,random.randrange(2,9))
frame=0
running=True
last_update=0   
cloudmove=Vector2(-0.1,0)
clicked=False

def bg_reset(scrollspeed):
    global floor_pos
    global floor2_pos
    screen.fill(bg_color)
    floor_rect.center=(floor_pos.x*cell_size,floor_pos.y*cell_size)
    floor2_rect.center=(floor2_pos.x*cell_size,floor2_pos.y*cell_size)
    screen.blit(floor,floor_rect)
    screen.blit(floor,floor2_rect)
    floor_pos+=scrollspeed
    floor2_pos+=scrollspeed
    if floor_pos.x<=-25:
        floor_pos.x=floor2_pos.x+50
    if floor2_pos.x<=-25:
        floor2_pos.x=floor_pos.x+50

def move_cloud(cloudpos):
    global bg_speed,cloudmove
    cloud_cooldown=1500
    cloudrect=cloud.get_rect()
    cloudrect.center=(cloudpos.x*cell_size,cloudpos.y*cell_size)
    cloudpos+=cloudmove
    if cloudpos.x<=-5:
        cloudpos.x=random.randrange(21,28)
        cloudpos.y=random.randrange(2,9)
    screen.blit(cloud,cloudrect)
    if bg_speed==Vector2(0,0):
        cloudmove=Vector2(0,0)
        
def cluster(cluster_list):
    for i in range(len(cluster_list)):
        cluster_list[i].draw_obstacles()
        cluster_list[i].move_obstacles()
    if cluster_list[i].pos.x<=-1:
        for i in range(3):
            cluster_list[i].move_obstacles()
        if cluster_list[i].pos.x<=-1:
            for i in range(3):
                cluster_list[i].pos=Vector2(21+i*1.2,14)
                
def spawn_cactus():
    global smallarray,r,player,bg_speed,clicked,player
    cooldown=1000
    smallarray[r].draw_obstacles()   
    if checkcollision(player,smallarray[r]): 
        player.pos.y=14
        screen.blit(GameOver,game_over_rect)
        screen.blit(replay_button,retry_rect)
    elif smallarray[r].pos.x<=-1:
        r=random.randrange(0,4)
    
def checkcollision(player,obstacle):
    global bg_speed,cloudmove,clicked
    if player.hitbox.colliderect(obstacle.cactusrec):
        player.death=True
        bg_speed=Vector2(0,0)
        cloudmove=Vector2(0,0)
        return True
    else:
        acc=Vector2(-0.0001,0)*0.9
        bg_speed+=acc*(dt/1000)
        print(bg_speed)
        return False

def checkgame(retry_rect):
    global clicked,smallarray,bg_speed,cloudmove,player
    mouse_pos=pygame.mouse.get_pos()
    if retry_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0] and clicked==False:
            clicked=True
            if clicked:
                reseteverything() 
                clicked=False
                

def reseteverything():
    global small_array_backup,smallarray,cloudmove,player,bg_speed,running,cactus1,cactus2,smallcactus,smallcactus2,r
    cactus1=obstacles(22,14,0)
    cactus2=obstacles(22.4,14,0)
    smallcactus=obstacles(21,14,1)
    smallcactus2=obstacles(21,14,2)
    smallarray=[smallcactus,smallcactus2,cactus1,cactus2]
    player.death=False
    player.isjump=False
    running=True
    cloudmove=Vector2(-0.1,0)
    bg_speed=Vector2(-25000,0)
        
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    dt=clock.tick(10)
    bg_reset(bg_speed)
    #move_cloud(cloudpos2)
    player.movement()
    currentframe_time=pygame.time.get_ticks()
    move_cloud(cloudpos)
    move_cloud(cloudpos2)
    move_cloud(cloudpos3)
    move_cloud(cloudpos4)
    spawn_cactus()
    player.draw_runner()
    checkgame(retry_rect)
    pygame.display.flip()
   
