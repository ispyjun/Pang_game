import pygame
import os
#####################사용자 게임화면 초기화#########################################

def Gameplay():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    level=0
    score=0

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

    weapon_to_remove=-1
    ball_to_remove=-1

    #폰트
    game_font=pygame.font.Font(None,40)
    total_time=50
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"

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
                    if len(weapons) <1:
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
        if level<1:
            for ball_idx,ball_val in enumerate(balls):
                ball_pos_x = ball_val["pos_x"]
                ball_pos_y = ball_val["pos_y"]
                ball_img_idx = ball_val["img_idx"]

                ball_size=ball_images[ball_img_idx].get_rect().size
                ball_width=ball_size[0]
                ball_height=ball_size[1]

                #벽에 부딪힐 때
                if ball_pos_x <=0 or ball_pos_x > screen_width - ball_width:
                    ball_val["to_x"]=ball_val["to_x"]*-1
                
                #스테이지에 부딪힐 때
                if ball_pos_y>=screen_height-stage_height-ball_height:
                    ball_val["to_y"]=ball_val["init_spd_y"]

                else:#그 외 모든경우 속도 증가
                    ball_val["to_y"] +=0.5

                ball_val["pos_x"] += ball_val["to_x"]
                ball_val["pos_y"] += ball_val["to_y"]



        #캐릭터 rect정보 업데이트
        character_rect=character.get_rect()
        character_rect.left=character_x_pos
        character_rect.top=character_y_pos

        for ball_idx,ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left=ball_pos_x
            ball_rect.top=ball_pos_y

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball_rect):
                running =False
                break

            #공과 무기 충돌
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_x=weapon_val[0]
                weapon_y_pos=weapon_val[1]

                #무기 rect정보 업데이트
                weapon_rect = weapon.get_rect()
                weapon_rect.left=weapon_x_pos
                weapon_rect.top=weapon_y_pos

                if weapon_rect.colliderect(ball_rect):
                    if ball_img_idx==3:
                            score+=40
                    weapon_to_remove=weapon_idx
                    ball_to_remove=ball_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball_img_idx<3:
                        

                        ball_width=ball_rect.size[0]
                        ball_height=ball_rect.size[1]

                        small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                        small_ball_width=small_ball_rect.size[0]
                        small_ball_height=small_ball_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls.append({
                            "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                            "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),
                            "img_idx":ball_img_idx+1,
                            "to_x":-3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls.append({
                            "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                            "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),
                            "img_idx":ball_img_idx+1,
                            "to_x":3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball_img_idx+1]})
                        
                        if ball_img_idx==0:
                            score+=10
                        if ball_img_idx==1:
                            score+=20
                        if ball_img_idx==2:
                            score+=30
                    break
            else:
                continue
            break

        #충돌된 공,무기 없애기
        if ball_to_remove>-1:
            del balls[ball_to_remove]
            ball_to_remove=-1

        if weapon_to_remove>-1:
            del weapons[weapon_to_remove]
            weapon_to_remove=-1

        #모든 공을 없앤 경우
        if len(balls)==0:
            if level<1:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                running=False

            else:
                game_result="Mission Complete"
                running=False

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

        elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
        timer = game_font.render("Time : {}".format(int(total_time-elapsed_time)),True,(255,255,255))
        scoreout = game_font.render("Score : {}".format(int(score)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            game_result="Time Over"
            running=False
        
        pygame.display.update()

    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()

    pygame.time.delay(2000)
    return game_result

#####################기본 초기화#########################################
pygame.init() 

#화면 크기
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀
pygame.display.set_caption("Pang")

#FPS
clock = pygame.time.Clock()
game_result="Game Over"

running=True
while running:
    for event in pygame.event.get():
        #이동 키보드 입력
        if event.type==pygame.KEYDOWN:
            if event.key == ord('s'):
                game_result=Gameplay()
                break
            if event.key == ord('d'):
                running=False
                break
            if game_result=="Next Level":
                if event.key == ord('n'):
                    running=False
#ptgame 종료
pygame.quit()
