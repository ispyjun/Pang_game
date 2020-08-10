import pygame
import os
#####################기본 초기화#########################################
#2:11:10
pygame.init() 

#화면 크기
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀
pygame.display.set_caption("Pang")

#FPS
clock = pygame.time.Clock()

#####################사용자 게임화면 초기화#########################################

current_path=os.path.dirname(__file__)
image_path=os.path.join(current_path,"images")

#배경
background=pygame.image.load(os.path.join(image_path,"background.png"))
#스테이지
stage=pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size=stage.get_rect().size
stage_height=stage_size[1]

#캐릭터
character=pygame.image.load(os.path.join(image_path,"character.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos = screen_height - character_height-stage_height

character_to_x_LEFT=0
character_to_x_RIGHT=0
character_speed=7

#무기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size=weapon.get_rect().size
weapon_width=weapon_size[0]

weapons=[]

weapon_speed = 10

#공
ball_images=[pygame.image.load(os.path.join(image_path,"ball1.png")),
pygame.image.load(os.path.join(image_path,"ball2.png")),
pygame.image.load(os.path.join(image_path,"ball3.png")),
pygame.image.load(os.path.join(image_path,"ball4.png"))]

ball_speed_y=[-18,-15,-12,-9]

#공들
balls=[]

balls.append({
    "pos_x":50,
    "pos_y":50,
    "img_idx":0,
    "to_x":3,
    "to_y":-6,
    "init_spd_y":ball_speed_y[0]
})

#이벤트
running=True
while running:
    dt=clock.tick(30)
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #창이 닫히는 이벤트
            running=False
        
        #이동 키보드 입력
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT-=character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT+=character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos=character_x_pos+(character_width/2)-(weapon_width/2)
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0


    #게임 캐릭터 위치
    character_x_pos+=character_to_x_LEFT + character_to_x_RIGHT

    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width

    #무기 위치
    weapons=[[w[0],w[1]-weapon_speed] for w in weapons]
    weapons=[[w[0],w[1]] for w in weapons if w[1]>0]

    #공위치
    for ball_idx,ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]

        #벽에 부딪힐 때
        if ball_pos_x <=0 or ball_pos_x>screen_width - ball_width:
            ball_val["to_x"]=ball_val["to_x"]*-1
        
        #스테이지에 부딪힐 때
        if ball_pos_y>=screen_height-stage_height-ball_height:
            ball_val["to_y"]=ball_val["to_y"]*-1
        else:#그 외 모든경우
            ball_val["to_y"] +=0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    #r그리기
    screen.blit(background,(0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    for idx,val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))

    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    
    pygame.display.update()

#ptgame 종료
pygame.quit()
