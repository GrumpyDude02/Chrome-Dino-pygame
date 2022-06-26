import pygame,random,sys
from pygame.math import Vector2

player_acc=0.033
cell_size=35
cell_number=30
pygame.init()

c=1
clock=pygame.time.Clock()        
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*17),vsync=1)
bg_color=(250,250,250)
score_color=(5,5,5)
clock=pygame.time.Clock()
fps=60


#Sounds
death_sound=pygame.mixer.Sound('sfx\Dino_Sounds_die.wav')
check_sound=pygame.mixer.Sound('sfx\point.wav')
jump_sound=pygame.mixer.Sound('sfx\Dino_Sounds_jump.wav')

#playerAssets
dino_scale=2.5
dino_run1=pygame.transform.scale(pygame.image.load('Dino\DinoRun1.png').convert_alpha(),(cell_size*dino_scale,cell_size*dino_scale))
dino_run2=pygame.transform.scale(pygame.image.load('Dino\DinoRun2.png').convert_alpha(),(cell_size*dino_scale,cell_size*dino_scale))
dino_jump=pygame.transform.scale(pygame.image.load('Dino\DinoJump.png').convert_alpha(),(cell_size*dino_scale,cell_size*dino_scale))
dino_dead=pygame.transform.scale(pygame.image.load('Dino\DinoDead.png').convert_alpha(),(cell_size*dino_scale,cell_size*dino_scale))
dino_duck1=pygame.transform.scale(pygame.image.load('Dino\DinoDuck1.png').convert_alpha(),(cell_size+72,cell_size+22))
dino_duck2=pygame.transform.scale(pygame.image.load('Dino\DinoDuck2.png').convert_alpha(),(cell_size+72,cell_size+22))

#Other Assets
cloud=pygame.transform.scale(pygame.image.load('Background\Cloud.png').convert_alpha(),(cell_size*3,cell_size*3))
floor=pygame.transform.scale(pygame.image.load('Background\Track.png').convert_alpha(),(cell_size*50,cell_size))

#Obstacle Assets
Large_Cactus=pygame.transform.scale(pygame.image.load('Obstacles\LargeCactus1.png').convert_alpha(),(cell_size+5,cell_size+40))
small_cactus=pygame.transform.scale(pygame.image.load('Obstacles\SmallCactus1.png').convert_alpha(),(cell_size+10,cell_size+30))
small_cactus2=pygame.transform.scale(pygame.image.load('Obstacles\SmallCactus2.png').convert_alpha(),(cell_size+10,cell_size+30))
small_cactus3=pygame.transform.scale(pygame.image.load('Obstacles\SmallCactus3.png').convert_alpha(),(cell_size+50,cell_size+40))
GameOver=pygame.image.load('GameOver\GameOver.png').convert_alpha()
replay_button=pygame.image.load('GameOver\Reset.png').convert_alpha()

imagearray=[ Large_Cactus , small_cactus , small_cactus2 , small_cactus3 , cloud ]

Dino_RUN=[dino_run1,dino_run2]
Dino_DUCK=[dino_duck1,dino_duck2]
Bird_sprites=[]

class obstacles():
    def __init__(self,x,y,imageindex):
        global imagearray
        self.pos=Vector2(x,y)
        self.index=imageindex
        self.pos_backup=Vector2(x,y)
        self.cactusrec=imagearray[self.index].get_rect()
    def draw_obstacles(self,speed):
        global imagearray
        self.cactusrec.center=(self.pos.x*cell_size,self.pos.y*cell_size) 
        image=imagearray[self.index]
        #pygame.draw.rect(screen,(255,0,0),self.cactusrec,2)
        screen.blit(image,self.cactusrec)  
        self.pos+=speed    
            
class runner():
    def __init__(self):
        self.pos=Vector2(2,14)
        self.acc=Vector2(0,player_acc)
        self.velocity=Vector2(0,0)
        self.hitbox=dino_run1.get_rect()
        self.cooldown=100
        self.isjump=False
        self.death=False
        self.duck=False
        
    def draw_runner(self):
        global frame
        global last_update
        global currentframe_time
        global running
        self.hitbox.center=(self.pos.x*cell_size,self.pos.y*cell_size-20)
        if currentframe_time-last_update>=self.cooldown :
            last_update=currentframe_time
            frame+=1
            if frame>=len(Dino_RUN):
                frame=0
                
        if not self.death and running:
            self.hitbox=dino_run1.get_rect()
            self.hitbox.inflate_ip(-30,-30)
            self.hitbox.center=(self.pos.x*cell_size,self.pos.y*cell_size-20)
            #pygame.draw.rect(screen,(0,255,0),self.hitbox,2)
            screen.blit(Dino_RUN[frame],self.hitbox)
                
        elif self.duck and  not self.isjump and not running :
            self.hitbox=dino_duck1.get_rect()
            self.hitbox.inflate_ip(-30,-30)
            self.hitbox.center=(self.pos.x*cell_size,self.pos.y*cell_size-5)
            screen.blit(Dino_DUCK[frame],self.hitbox)
            #pygame.draw.rect(screen,(0,255,0),self.hitbox,2)
           
        if self.isjump:
            screen.blit(dino_jump,self.hitbox) 
            
        if self.death:
            screen.blit(dino_dead,self.hitbox)   
            
        
    def movement(self):
        global running
        keys=pygame.key.get_pressed()
        if self.isjump==False:
            if keys[pygame.K_SPACE] and self.pos.y==14 and self.death==False:
                self.isjump=True
                if self.isjump==True:
                    self.velocity.y = -0.60
                    jump_sound.play()
        if keys[pygame.K_DOWN] and not self.death:
            self.velocity.y=0.6
            self.duck=True
            running=False
        else:
            self.duck=False
            running=True
        self.velocity += self.acc
        self.pos += self.velocity+0.5*self.acc*0.9
        if self.pos.y>14:
            self.pos.y=14
            self.isjump=False
            
     
floor_rect=floor.get_rect()
floor2_rect=floor.get_rect()
floor_pos=Vector2(0,14.7)
floor2_pos=Vector2(50,14.7)
bg_speed=Vector2(-0.25,0)
cloud_speed=Vector2(-0.1,0)

#obstacles objects

obstacle=[]
clouds=[]
appending=True

#Dino

player = runner()

#globale variables

frame=0
score=0
running=True
last_update=0 
last_update_object=0   
last_cloud=0
last_c_increment=0
last_night_time=0
last_score=0
flashing_start=0
flashing=False
startFlashing=False
display_time=0
flashing_time=0
score_backup=0


clicked=False
collide=False
night=False
game_over=False


#functions................................................................................

def random_obstacle_gen():
    global last_update_object,currentframe_time,obstacle,player,bg_speed,appending,collide
    gen_cooldown=random.randrange(1000,1501)
    r=random.randrange(0,4)
    acc=Vector2(-0.00001,0)*0.9
    if currentframe_time-last_update_object>=gen_cooldown:
        last_update_object=currentframe_time
        if appending==True:
            obstacle.append(obstacles(32,14,r))
            r=random.randrange(0,4)
    for bumps in obstacle:
        player_last_pos=player.pos.y
        checkcollision(player,bumps)
        if collide==True:
            player.pos.y=player_last_pos
            game_over_rect=GameOver.get_rect()
            game_over_rect.center=((cell_number//2)*cell_size,8*cell_number)
            retry_rect=replay_button.get_rect()
            retry_rect.center=(cell_size*(cell_number//2),cell_size*10)
            screen.blit(GameOver,game_over_rect)
            screen.blit(replay_button,retry_rect)
            bumps.draw_obstacles(bg_speed)
            acc=Vector2(0,0)
            appending=False
            if checkgame(retry_rect):
                obstacle=[]
                appending=True
                break
        elif bumps.pos.x<=-40:
            obstacle.pop(obstacle.index(bumps))
        else:
            bumps.draw_obstacles(bg_speed)
            bg_speed+=acc

def night_time():
    global c,bg_color,currentframe_time,last_c_increment,bg_speed,last_night_time,night,game_over
    night_cooldown=5
    day_duration=50000
    if currentframe_time-last_night_time>=day_duration and night==False and game_over==False :
        night=True
        last_night_time=currentframe_time
    if c<5 and night==True and currentframe_time-last_c_increment>=night_cooldown :
        c+=0.05
        last_c_increment=currentframe_time
    if c>=5 and currentframe_time-last_night_time>=day_duration and game_over==False :
        night=False
        last_night_time=currentframe_time
    if night==False and c>1 and currentframe_time-last_c_increment>=night_cooldown :
        c-=0.05
        last_c_increment=currentframe_time  
    bg_color=(250/c,250/c,250/c)

def bg_reset(scrollspeed):
    global floor_pos,floor2_pos
    screen.fill(bg_color)
    floor_rect.center=(floor_pos.x*cell_size,floor_pos.y*cell_size)
    floor2_rect.center=(floor2_pos.x*cell_size,floor2_pos.y*cell_size)
    night_time()
    screen.blit(floor,floor_rect)
    screen.blit(floor,floor2_rect)
    floor_pos+=scrollspeed
    floor2_pos+=scrollspeed
    if floor_pos.x<=-25:
        floor_pos.x=floor2_pos.x+50
    if floor2_pos.x<=-25:
        floor2_pos.x=floor_pos.x+50

def move_cloud(app):
    global last_cloud,currentframe_time,cloud_speed
    cloud_cooldown=1000
    rc=random.randrange(2,11)
    if app:
        if currentframe_time-last_cloud>=cloud_cooldown:
            last_cloud=currentframe_time
            clouds.append(obstacles(32,rc,4))
    for cloud in clouds:
        cloud.draw_obstacles(cloud_speed)
        if cloud.pos.x<=-40:
            clouds.pop(clouds.index(cloud))  
          
def checkcollision(player,obstacle):
    global bg_speed,collide,cloud_speed,currentframe_time,game_over
    if player.hitbox.colliderect(obstacle.cactusrec) and collide==False:
        collide=True
        player.death=True
        bg_speed=Vector2(0,0)
        cloud_speed=Vector2(0,0)
        game_over=True
        death_sound.play()

def checkgame(retry_rect):
    global clicked,bg_speed,cloud_speed,player
    mouse_pos=pygame.mouse.get_pos()
    if retry_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0] and clicked==False:
            clicked=True
            if clicked:
                reseteverything() 
                clicked=False
                return True
                
def scorecounter(currenttime,sound):
    global score,last_score,c,score_color,flashing,flashing_start,startFlashing,display_time,flashing_time,score_backup
    fontt=pygame.font.Font('Font\PressStart2P-Regular.ttf',15)
    score_cooldown=75
    flashing_cooldown=400
    display_duration=800
    scorepoints=fontt.render("SCORE: "+str(score),1,score_color)
    score_color=(50*c,50*c,50*c)
    if currenttime-last_score>=score_cooldown and collide==False:
        last_score=currenttime
        score+=1
    if score%100==0:
        score_backup=score
        sound.set_volume(0.5)
        sound.play()
        flashing=True
        flashing_time=currenttime
    if flashing:
        if currenttime-flashing_start>=flashing_cooldown:
            startFlashing=True
        if currenttime-flashing_time>=3200 and startFlashing==False:
            flashing=False
    if flashing==False:
        screen.blit(scorepoints,(23*cell_size,0.5*cell_size)) 
    if startFlashing:
        scorepoints_backup=fontt.render('SCORE: '+str(score_backup),1,score_color)
        screen.blit(scorepoints_backup,(23*cell_size,0.5*cell_size))
    if currenttime-flashing_start>=display_duration:
            flashing_start=currenttime
            startFlashing=False

def reseteverything():
    global cloud_speed,player,bg_speed,running,collide,obstacle,clouds,game_over,score
    clouds=[]
    player.death=False
    player.isjump=False
    game_over=False
    running=True
    collide=False
    cloud_speed=Vector2(-0.1,0)
    bg_speed=Vector2(-0.25,0)
    score=0
        
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    player.movement()
    currentframe_time=pygame.time.get_ticks()
    bg_reset(bg_speed)
    player.draw_runner()
    random_obstacle_gen()
    move_cloud(appending)
    scorecounter(currentframe_time,check_sound)
    pygame.display.flip()
    clock.tick(60)