import pygame
import os
from random import *
#####################사용자 게임화면 초기화#########################################
current_path=os.path.dirname(__file__)
image_path=os.path.join(current_path,"images")
level=1
score=0
ranking=[]
n=0
shot=1
shield=0
def Gameplay():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    global level
    global score
    global ranking
    global rankingname
    global n
    global shot
    global shield

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
    ball_images=[pygame.image.load(os.path.join(image_path,"ball1_1.png")),
    pygame.image.load(os.path.join(image_path,"ball2_1.png")),
    pygame.image.load(os.path.join(image_path,"ball3_1.png")),
    pygame.image.load(os.path.join(image_path,"ball4_1.png"))]

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
    total_time=30
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"
    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))

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
                    if len(weapons) <shot:
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
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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
            if level<5:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level+=1
                shot=1
                score+=int(total_time-elapsed_time)
                running=False

            else:
                game_result="Mission Complete"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level=1
                print("{} 점입니다.".format(score))
                ranking.append("***"+str(score)+"***")
                ranking.append(input("이름을 입력하세요 : "))
                score=0
                n+=1
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
        levelout = game_font.render("Level : {}".format(int(level)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(levelout,(260,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            game_result="Time Over"
            msg=game_font.render(game_result,True,(255,255,0))
            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
            screen.blit(msg,msg_rect)
            pygame.display.update()
            level=1
            print("{} 점입니다.".format(score))
            ranking.append(score)
            ranking.append(input("이름을 입력하세요 : "))
            score=0
            n+=1
            shot=1
            running=False
        
        pygame.display.update()

    
    screen.blit(msg,msg_rect)
    pygame.display.update()

    pygame.time.delay(2000)
    return game_result
def Gameplay2():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    global level
    global score
    global ranking
    global rankingname
    global n
    global shot

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
    ball_images=[pygame.image.load(os.path.join(image_path,"ball1_2.png")),
    pygame.image.load(os.path.join(image_path,"ball2_2.png")),
    pygame.image.load(os.path.join(image_path,"ball3_2.png")),
    pygame.image.load(os.path.join(image_path,"ball4_2.png"))]

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
    total_time=30
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"
    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))

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
                    if len(weapons) <shot:
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
            if ball_pos_x <=0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"]=ball_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball_pos_y>=screen_height-stage_height-ball_height:
                ball_val["to_y"]=ball_val["init_spd_y"]

            else:#그 외 모든경우 속도 증가
                ball_val["to_y"] +=0.5

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

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
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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
                            score+=45
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
                            score+=21
                        if ball_img_idx==2:
                            score+=33
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
            if level<5:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level+=1
                score+=int(total_time-elapsed_time)
                shot=1
                running=False

            else:
                game_result="Mission Complete"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level=1
                print("{} 점입니다.".format(score))
                ranking.append("***"+str(score)+"***")
                ranking.append(input("이름을 입력하세요 : "))
                score=0
                n+=1
                shot=1
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
        levelout = game_font.render("Level : {}".format(int(level)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(levelout,(260,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            game_result="Time Over"
            msg=game_font.render(game_result,True,(255,255,0))
            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
            screen.blit(msg,msg_rect)
            pygame.display.update()
            level=1
            print("{} 점입니다.".format(score))
            ranking.append(score)
            ranking.append(input("이름을 입력하세요 : "))
            score=0
            shot=1
            n+=1
            running=False
        
        pygame.display.update()

    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()

    pygame.time.delay(2000)
    return game_result
def Gameplay3():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    global level
    global score
    global ranking
    global rankingname
    global n
    global shot
    global shield
    global bomb

    #배경
    background=pygame.image.load(os.path.join(image_path,"background2.png"))
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
    ball_images=[pygame.image.load(os.path.join(image_path,"ball1_1.png")),
    pygame.image.load(os.path.join(image_path,"ball2_1.png")),
    pygame.image.load(os.path.join(image_path,"ball3_1.png")),
    pygame.image.load(os.path.join(image_path,"ball4_1.png"))]

    ball_speed_y=[-18,-15,-12,-9]

    #공들
    balls=[]
    balls2=[]

    balls.append({
        "pos_x":50,
        "pos_y":50,
        "img_idx":0,
        "to_x":3,
        "to_y":-6,
        "init_spd_y":ball_speed_y[0]
    })
    balls2.append({
        "pos_x":430,
        "pos_y":50,
        "img_idx":0,
        "to_x":-3,
        "to_y":-6,
        "init_spd_y":ball_speed_y[0]
    })

    weapon_to_remove=-1
    ball_to_remove=-1
    ball2_1_to_remove=-1

    #폰트
    game_font=pygame.font.Font(None,40)
    total_time=30
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"
    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))

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
                    if len(weapons) <shot:
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
            if ball_pos_x <=0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"]=ball_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball_pos_y>=screen_height-stage_height-ball_height:
                ball_val["to_y"]=ball_val["init_spd_y"]

            else:#그 외 모든경우 속도 증가
                ball_val["to_y"] +=0.5

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_size=ball_images[ball2_1_img_idx].get_rect().size
            ball2_1_width=ball2_1_size[0]
            ball2_1_height=ball2_1_size[1]

            #벽에 부딪힐 때
            if ball2_1_pos_x <=0 or ball2_1_pos_x > screen_width - ball2_1_width:
                ball2_1_val["to_x"]=ball2_1_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball2_1_pos_y>=screen_height-stage_height-ball2_1_height:
                ball2_1_val["to_y"]=ball2_1_val["init_spd_y"]

            else:#그 외 모든경우 속도 증가
                ball2_1_val["to_y"] +=0.5

            ball2_1_val["pos_x"] += ball2_1_val["to_x"]
            ball2_1_val["pos_y"] += ball2_1_val["to_y"]


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
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
                    running =False
                    break
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
        
        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_rect = ball_images[ball2_1_img_idx].get_rect()
            ball2_1_rect.left=ball2_1_pos_x
            ball2_1_rect.top=ball2_1_pos_y
        

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball2_1_rect):
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
                    running =False
                    break
                break

            #공과 무기 충돌
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_x=weapon_val[0]
                weapon_y_pos=weapon_val[1]

                #무기 rect정보 업데이트
                weapon_rect = weapon.get_rect()
                weapon_rect.left=weapon_x_pos
                weapon_rect.top=weapon_y_pos

                if weapon_rect.colliderect(ball2_1_rect):
                    if ball2_1_img_idx==3:
                            score+=40
                    weapon_to_remove=weapon_idx
                    ball2_1_to_remove=ball2_1_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball2_1_img_idx<3:
                        

                        ball2_1_width=ball2_1_rect.size[0]
                        ball2_1_height=ball2_1_rect.size[1]

                        small_ball2_1_rect=ball_images[ball2_1_img_idx+1].get_rect()
                        small_ball2_1_width=small_ball2_1_rect.size[0]
                        small_ball2_1_height=small_ball2_1_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":-3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball2_1_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball2_1_img_idx+1]})
                        
                        if ball2_1_img_idx==0:
                            score+=10
                        if ball2_1_img_idx==1:
                            score+=20
                        if ball2_1_img_idx==2:
                            score+=30
                    break
            else:
                continue
            break

        #충돌된 공,무기 없애기
        if ball_to_remove>-1:
            del balls[ball_to_remove]
            ball_to_remove=-1

        if ball2_1_to_remove>-1:
            del balls2[ball2_1_to_remove]
            ball2_1_to_remove=-1

        if weapon_to_remove>-1:
            del weapons[weapon_to_remove]
            weapon_to_remove=-1

        #모든 공을 없앤 경우
        if len(balls)==0 and len(balls2)==0:
            if level<5:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level+=1
                shot=1
                score+=int(total_time-elapsed_time)
                running=False

            else:
                game_result="Mission Complete"
                level=1
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                print("{} 점입니다.".format(score))
                ranking.append("***"+str(score)+"***")
                ranking.append(input("이름을 입력하세요 : "))
                score=0
                shot=1
                n+=1
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

        for idx2,val2 in enumerate(balls2):
            ball2_1_pos_x = val2["pos_x"]
            ball2_1_pos_y = val2["pos_y"]
            ball2_1_img_idx = val2["img_idx"]
            screen.blit(ball_images[ball2_1_img_idx],(ball2_1_pos_x,ball2_1_pos_y))

        screen.blit(stage,(0,screen_height-stage_height))
        screen.blit(character,(character_x_pos,character_y_pos))

        elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
        timer = game_font.render("Time : {}".format(int(total_time-elapsed_time)),True,(255,255,255))
        scoreout = game_font.render("Score : {}".format(int(score)),True,(255,255,255))
        levelout = game_font.render("Level : {}".format(int(level)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(levelout,(260,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            game_result="Time Over"
            msg=game_font.render(game_result,True,(255,255,0))
            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
            screen.blit(msg,msg_rect)
            pygame.display.update()
            level=1
            print("{} 점입니다.".format(score))
            ranking.append(score)
            ranking.append(input("이름을 입력하세요 : "))
            score=0
            n+=1
            running=False
        
        pygame.display.update()

    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()

    pygame.time.delay(2000)
    return game_result
def Gameplay4():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    global level
    global score
    global ranking
    global rankingname
    global n
    global shot

    #배경
    background=pygame.image.load(os.path.join(image_path,"background2.png"))
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
    ball_images=[pygame.image.load(os.path.join(image_path,"ball1_1.png")),
    pygame.image.load(os.path.join(image_path,"ball2_1.png")),
    pygame.image.load(os.path.join(image_path,"ball3_1.png")),
    pygame.image.load(os.path.join(image_path,"ball4_1.png"))]

    ball2_images=[pygame.image.load(os.path.join(image_path,"ball1_2.png")),
    pygame.image.load(os.path.join(image_path,"ball2_2.png")),
    pygame.image.load(os.path.join(image_path,"ball3_2.png")),
    pygame.image.load(os.path.join(image_path,"ball4_2.png"))]

    ball_speed_y=[-24,-21,-18,-15]

    #공들
    balls=[]
    balls2=[]

    balls.append({
        "pos_x":50,
        "pos_y":50,
        "img_idx":0,
        "to_x":5,
        "to_y":-2,
        "init_spd_y":ball_speed_y[0]
    })
    balls2.append({
        "pos_x":430,
        "pos_y":50,
        "img_idx":0,
        "to_x":-3,
        "to_y":-9,
        "init_spd_y":ball_speed_y[0]
    })

    weapon_to_remove=-1
    ball_to_remove=-1
    ball2_1_to_remove=-1

    #폰트
    game_font=pygame.font.Font(None,40)
    total_time=40
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"
    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))

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
                    if len(weapons) <shot:
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
            if ball_pos_x <=0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"]=ball_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball_pos_y>=screen_height-stage_height-ball_height:
                ball_val["to_y"]=ball_val["init_spd_y"]

            if ball_pos_y<=0:
                ball_val["to_y"]=ball_val["init_spd_y"]*-1

            else:#그 외 모든경우 속도 증가
                ball_val["to_y"] +=0.5

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_size=ball2_images[ball2_1_img_idx].get_rect().size
            ball2_1_width=ball2_1_size[0]
            ball2_1_height=ball2_1_size[1]

            #벽에 부딪힐 때
            if ball2_1_pos_x <=0 or ball2_1_pos_x > screen_width - ball2_1_width:
                ball2_1_val["to_x"]=ball2_1_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball2_1_pos_y>=screen_height-stage_height-ball2_1_height:
                ball2_1_val["to_y"]=ball2_1_val["init_spd_y"]

            if ball2_1_pos_y<=0:
                ball2_1_val["to_y"]=ball2_1_val["init_spd_y"]*-1

            else:#그 외 모든경우 속도 증가
                ball2_1_val["to_y"] +=0.5

            ball2_1_val["pos_x"] += ball2_1_val["to_x"]
            ball2_1_val["pos_y"] += ball2_1_val["to_y"]


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
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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
        
        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_rect = ball2_images[ball2_1_img_idx].get_rect()
            ball2_1_rect.left=ball2_1_pos_x
            ball2_1_rect.top=ball2_1_pos_y
        

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball2_1_rect):
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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

                if weapon_rect.colliderect(ball2_1_rect):
                    if ball2_1_img_idx==3:
                            score+=45
                    weapon_to_remove=weapon_idx
                    ball2_1_to_remove=ball2_1_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball2_1_img_idx<3:
                        

                        ball2_1_width=ball2_1_rect.size[0]
                        ball2_1_height=ball2_1_rect.size[1]

                        small_ball2_1_rect=ball2_images[ball2_1_img_idx+1].get_rect()
                        small_ball2_1_width=small_ball2_1_rect.size[0]
                        small_ball2_1_height=small_ball2_1_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":-3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball2_1_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_y[ball2_1_img_idx+1]})
                        
                        if ball2_1_img_idx==0:
                            score+=10
                        if ball2_1_img_idx==1:
                            score+=21
                        if ball2_1_img_idx==2:
                            score+=33
                    break
            else:
                continue
            break

        #충돌된 공,무기 없애기
        if ball_to_remove>-1:
            del balls[ball_to_remove]
            ball_to_remove=-1

        if ball2_1_to_remove>-1:
            del balls2[ball2_1_to_remove]
            ball2_1_to_remove=-1

        if weapon_to_remove>-1:
            del weapons[weapon_to_remove]
            weapon_to_remove=-1

        #모든 공을 없앤 경우
        if len(balls)==0 and len(balls2)==0:
            if level<5:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level+=1
                shot=1
                score+=int(total_time-elapsed_time)
                running=False

            else:
                game_result="Mission Complete"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level=1
                ranking.append("***"+str(score)+"***")
                print("{} 점입니다.".format(score))
                ranking.append(input("이름을 입력하세요 : "))
                score=0
                n+=1
                shot=1
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

        for idx2,val2 in enumerate(balls2):
            ball2_1_pos_x = val2["pos_x"]
            ball2_1_pos_y = val2["pos_y"]
            ball2_1_img_idx = val2["img_idx"]
            screen.blit(ball2_images[ball2_1_img_idx],(ball2_1_pos_x,ball2_1_pos_y))

        screen.blit(stage,(0,screen_height-stage_height))
        screen.blit(character,(character_x_pos,character_y_pos))

        elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
        timer = game_font.render("Time : {}".format(int(total_time-elapsed_time)),True,(255,255,255))
        scoreout = game_font.render("Score : {}".format(int(score)),True,(255,255,255))
        levelout = game_font.render("Level : {}".format(int(level)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(levelout,(260,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            level=1
            game_result="Time Over"
            msg=game_font.render(game_result,True,(255,255,0))
            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
            screen.blit(msg,msg_rect)
            pygame.display.update()
            print("{} 점입니다.".format(score))
            ranking.append(score)
            ranking.append(input("이름을 입력하세요 : "))
            score=0
            shot=1
            n+=1
            running=False
        
        pygame.display.update()

    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()

    pygame.time.delay(2000)
    return game_result
def Gameplay5():
    current_path=os.path.dirname(__file__)
    image_path=os.path.join(current_path,"images")

    global level
    global score
    global ranking
    global rankingname
    global n
    global shot
    global shield

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
    ball_images=[pygame.image.load(os.path.join(image_path,"ball1_3.png")),
    pygame.image.load(os.path.join(image_path,"ball2_3.png")),
    pygame.image.load(os.path.join(image_path,"ball3_3.png"))]

    ball2_images=[pygame.image.load(os.path.join(image_path,"ball1_2.png")),
    pygame.image.load(os.path.join(image_path,"ball2_2.png")),
    pygame.image.load(os.path.join(image_path,"ball3_2.png")),
    pygame.image.load(os.path.join(image_path,"ball4_2.png"))]

    ball3_images=[pygame.image.load(os.path.join(image_path,"ball1_1.png")),
    pygame.image.load(os.path.join(image_path,"ball2_1.png")),
    pygame.image.load(os.path.join(image_path,"ball3_1.png")),
    pygame.image.load(os.path.join(image_path,"ball4_1.png"))]
    ball_speed_x=[-18,-15,-12,-9]

    #공들
    balls=[]
    balls2=[]
    balls3=[]

    balls.append({
        "pos_x":50,
        "pos_y":20,
        "img_idx":0,
        "to_x":3,
        "init_spd_x":ball_speed_x[0]
    })
    balls2.append({
        "pos_x":430,
        "pos_y":50,
        "img_idx":0,
        "to_x":-3,
        "to_y":-9,
        "init_spd_y":ball_speed_x[0]
    })

    balls3.append({
        "pos_x":50,
        "pos_y":50,
        "img_idx":0,
        "to_x":3,
        "to_y":-6,
        "init_spd_y":ball_speed_x[0]
    })

    #보스 총알
    bullet = pygame.image.load(os.path.join(image_path,"bullet.png"))
    bullet_size=bullet.get_rect().size
    bullet_width=bullet_size[0]

    bullets=[]
    bullet_speed=10

    bullet2 = pygame.image.load(os.path.join(image_path,"bullet.png"))
    bullet2_size=bullet.get_rect().size
    bullet2_width=bullet_size[0]

    bullets2=[]
    bullet2_speed=10

    weapon_to_remove=-1
    ball_to_remove=-1
    ball2_1_to_remove=-1
    ball3_to_remove=-1
    bullet_to_remove=-1
    bullet2_to_remove=-1

    #폰트
    game_font=pygame.font.Font(None,40)
    total_time=70
    start_ticks=pygame.time.get_ticks()

    game_result="Game Over"
    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))

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
                    
                    if len(weapons) <shot :
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
            ball_img_idx = ball_val["img_idx"]

            ball_size=ball_images[ball_img_idx].get_rect().size
            ball_width=ball_size[0]
            ball_height=ball_size[1]

            #벽에 부딪힐 때
            if ball_pos_x <=0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"]=ball_val["to_x"]*-1

            ball_val["pos_x"] += ball_val["to_x"]

        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_size=ball2_images[ball2_1_img_idx].get_rect().size
            ball2_1_width=ball2_1_size[0]
            ball2_1_height=ball2_1_size[1]

            #벽에 부딪힐 때
            if ball2_1_pos_x <=0 or ball2_1_pos_x > screen_width - ball2_1_width:
                ball2_1_val["to_x"]=ball2_1_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball2_1_pos_y>=screen_height-stage_height-ball2_1_height:
                ball2_1_val["to_y"]=ball2_1_val["init_spd_y"]

            if ball2_1_pos_y<=0:
                ball2_1_val["to_y"]=ball2_1_val["init_spd_y"]*-1

            else:#그 외 모든경우 속도 증가
                ball2_1_val["to_y"] +=0.5

            ball2_1_val["pos_x"] += ball2_1_val["to_x"]
            ball2_1_val["pos_y"] += ball2_1_val["to_y"]
        
        for ball3_idx,ball3_val in enumerate(balls3):
            ball3_pos_x = ball3_val["pos_x"]
            ball3_pos_y = ball3_val["pos_y"]
            ball3_img_idx = ball3_val["img_idx"]

            ball3_size=ball3_images[ball3_img_idx].get_rect().size
            ball3_width=ball3_size[0]
            ball3_height=ball3_size[1]

            #벽에 부딪힐 때
            if ball3_pos_x <=0 or ball3_pos_x > screen_width - ball3_width:
                ball3_val["to_x"]=ball3_val["to_x"]*-1
                
            #스테이지에 부딪힐 때
            if ball3_pos_y>=screen_height-stage_height-ball3_height:
                ball3_val["to_y"]=ball3_val["init_spd_y"]

            else:#그 외 모든경우 속도 증가
                ball3_val["to_y"] +=0.5

            ball3_val["pos_x"] += ball3_val["to_x"]
            ball3_val["pos_y"] += ball3_val["to_y"]
    
        bullets=[[m[0],m[1]+bullet_speed] for m in bullets]
        bullets=[[m[0],m[1]] for m in bullets if m[1]>0]

        bullets2=[[m[0],m[1]+bullet2_speed] for m in bullets2]
        bullets2=[[m[0],m[1]] for m in bullets2 if m[1]>0]


        #캐릭터 rect정보 업데이트
        character_rect=character.get_rect()
        character_rect.left=character_x_pos
        character_rect.top=character_y_pos

        for ball_idx,ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_img_idx = ball_val["img_idx"]

            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left=ball_pos_x

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball_rect):
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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
                    if ball_img_idx==2:
                            score+=50
                    weapon_to_remove=weapon_idx
                    ball_to_remove=ball_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball_img_idx<2:
                        

                        ball_width=ball_rect.size[0]
                        ball_height=ball_rect.size[1]

                        small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                        small_ball_width=small_ball_rect.size[0]
                        small_ball_height=small_ball_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls.append({
                            "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                            "pos_y":20,
                            "img_idx":ball_img_idx+1,
                            "to_x":-3,
                            "init_spd_x":ball_speed_x[ball_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls.append({
                            "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                            "pos_y":20,
                            "img_idx":ball_img_idx+1,
                            "to_x":3,
                            "init_spd_x":ball_speed_x[ball_img_idx+1]})
                                                
                        if ball_img_idx==0:
                            score+=30
                        if ball_img_idx==1:
                            score+=40
                        
                        
                    break
            else:
                continue
            break
        
        
        for ball_idx,ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_img_idx = ball_val["img_idx"]

            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left=ball_pos_x

            num=randint(0,20)
            if num==5:
                if len(bullets)<1:
                    bullet_x_pos=ball_pos_x+(ball_width/2)-(bullet_width/2)
                    bullet_y_pos=ball_height
                    bullets.append([bullet_x_pos,bullet_y_pos])

            elif num==6:
                if len(bullets2)<1:
                    bullet2_x_pos=ball_pos_x+(ball_width/2)-(bullet2_width/2)
                    bullet2_y_pos=ball_height
                    bullets2.append([bullet2_x_pos,bullet2_y_pos])
            
            for bullet_idx, bullet_val in enumerate(bullets):
                bullet_x=bullet_val[0]
                bullet_y_pos=bullet_val[1]

                #무기 rect정보 업데이트
                bullet_rect = bullet.get_rect()
                bullet_rect.left=bullet_x_pos
                bullet_rect.bottom=bullet_y_pos+20
                if bullet_rect.bottom>480:
                    bullet_to_remove=bullet_idx

                character_rect=character.get_rect()
                character_rect.left=character_x_pos
                character_rect.top=character_y_pos

                if bullet_rect.bottom>character_y_pos and bullet_rect.bottom<430:
                    if bullet_x_pos>character_x_pos and bullet_x_pos<character_x_pos+character_width:
                        
                        bullet_to_remove=bullet_idx
                        if shield==1:
                            game_result="Try Again!"
                            msg=game_font.render(game_result,True,(255,255,0))
                            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                            screen.blit(msg,msg_rect)
                            pygame.display.update()
                            running =False
                            break
                        else:
                            level=1
                            screen.blit(msg,msg_rect)
                            pygame.display.update()
                            print("{} 점입니다.".format(score))
                            ranking.append(score)
                            ranking.append(input("이름을 입력하세요 : "))
                            score=0
                            n+=1
                            shot=1
                            running =False
                            break


                    break
                else:
                    continue
                break
            
            for bullet2_idx, bullet2_val in enumerate(bullets2):
                bullet2_x=bullet2_val[0]
                bullet2_y_pos=bullet2_val[1]

                #무기 rect정보 업데이트
                bullet2_rect = bullet2.get_rect()
                bullet2_rect.left=bullet2_x_pos
                bullet2_rect.bottom=bullet2_y_pos+20
                if bullet2_rect.bottom>480:
                    bullet2_to_remove=bullet2_idx

                character_rect=character.get_rect()
                character_rect.left=character_x_pos
                character_rect.top=character_y_pos

                if bullet2_rect.bottom>character_y_pos and bullet2_rect.bottom<430:
                    if bullet2_x_pos>character_x_pos and bullet2_x_pos<character_x_pos+character_width:
                        
                        bullet2_to_remove=bullet2_idx
                        if shield==1:
                            game_result="Try Again!"
                            msg=game_font.render(game_result,True,(255,255,0))
                            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                            screen.blit(msg,msg_rect)
                            pygame.display.update()
                            running =False
                            break
                        else:
                            level=1
                            screen.blit(msg,msg_rect)
                            pygame.display.update()
                            print("{} 점입니다.".format(score))
                            ranking.append(score)
                            ranking.append(input("이름을 입력하세요 : "))
                            score=0
                            n+=1
                            shot=1
                            running =False
                            break


                    break
                else:
                    continue
                break
            
        for ball2_1_idx,ball2_1_val in enumerate(balls2):
            ball2_1_pos_x = ball2_1_val["pos_x"]
            ball2_1_pos_y = ball2_1_val["pos_y"]
            ball2_1_img_idx = ball2_1_val["img_idx"]

            ball2_1_rect = ball2_images[ball2_1_img_idx].get_rect()
            ball2_1_rect.left=ball2_1_pos_x
            ball2_1_rect.top=ball2_1_pos_y
        

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball2_1_rect):
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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

                if weapon_rect.colliderect(ball2_1_rect):
                    if ball2_1_img_idx==3:
                            score+=45
                    weapon_to_remove=weapon_idx
                    ball2_1_to_remove=ball2_1_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball2_1_img_idx<3:
                        

                        ball2_1_width=ball2_1_rect.size[0]
                        ball2_1_height=ball2_1_rect.size[1]

                        small_ball2_1_rect=ball2_images[ball2_1_img_idx+1].get_rect()
                        small_ball2_1_width=small_ball2_1_rect.size[0]
                        small_ball2_1_height=small_ball2_1_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":-3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_x[ball2_1_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls2.append({
                            "pos_x":ball2_1_pos_x+(ball2_1_width/2)-(small_ball2_1_width/2),
                            "pos_y":ball2_1_pos_y+(ball2_1_height/2)-(small_ball2_1_height/2),
                            "img_idx":ball2_1_img_idx+1,
                            "to_x":3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_x[ball2_1_img_idx+1]})
                        
                        if ball2_1_img_idx==0:
                            score+=10
                        if ball2_1_img_idx==1:
                            score+=21
                        if ball2_1_img_idx==2:
                            score+=33
                    break
            else:
                continue
            break

        for ball3_idx,ball3_val in enumerate(balls3):
            ball3_pos_x = ball3_val["pos_x"]
            ball3_pos_y = ball3_val["pos_y"]
            ball3_img_idx = ball3_val["img_idx"]

            ball3_rect = ball3_images[ball3_img_idx].get_rect()
            ball3_rect.left=ball3_pos_x
            ball3_rect.top=ball3_pos_y

            #공과 캐릭터 충돌
            if character_rect.colliderect(ball3_rect):
                if shield==1:
                    game_result="Try Again!"
                    msg=game_font.render(game_result,True,(255,255,0))
                    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    running =False
                    break
                else:
                    level=1
                    screen.blit(msg,msg_rect)
                    pygame.display.update()
                    print("{} 점입니다.".format(score))
                    ranking.append(score)
                    ranking.append(input("이름을 입력하세요 : "))
                    score=0
                    n+=1
                    shot=1
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

                if weapon_rect.colliderect(ball3_rect):
                    if ball3_img_idx==3:
                            score+=40
                    weapon_to_remove=weapon_idx
                    ball3_to_remove=ball3_idx

                    #가장 작은 공이 아니라면 나눠주기
                    if ball3_img_idx<3:

                        ball3_width=ball3_rect.size[0]
                        ball3_height=ball3_rect.size[1]

                        small_ball3_rect=ball3_images[ball3_img_idx+1].get_rect()
                        small_ball3_width=small_ball3_rect.size[0]
                        small_ball3_height=small_ball3_rect.size[1]

                        #왼쪽으로 나가는 공
                        balls3.append({
                            "pos_x":ball3_pos_x+(ball3_width/2)-(small_ball3_width/2),
                            "pos_y":ball3_pos_y+(ball3_height/2)-(small_ball3_height/2),
                            "img_idx":ball3_img_idx+1,
                            "to_x":-3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_x[ball3_img_idx+1]})

                        #오른쪽으로 나가는 공
                        balls3.append({
                            "pos_x":ball3_pos_x+(ball3_width/2)-(small_ball3_width/2),
                            "pos_y":ball3_pos_y+(ball3_height/2)-(small_ball3_height/2),
                            "img_idx":ball3_img_idx+1,
                            "to_x":3,
                            "to_y":-6,
                            "init_spd_y":ball_speed_x[ball3_img_idx+1]})
                        
                        if ball3_img_idx==0:
                            score+=10
                        if ball3_img_idx==1:
                            score+=20
                        if ball3_img_idx==2:
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
        
        if bullet_to_remove>-1:
            del bullets[bullet_to_remove]
            bullet_to_remove=-1
        
        if bullet2_to_remove>-1:
            del bullets2[bullet2_to_remove]
            bullet2_to_remove=-1
        
        if ball2_1_to_remove>-1:
            del balls2[ball2_1_to_remove]
            ball2_1_to_remove=-1
        
        if ball3_to_remove>-1:
            del balls3[ball3_to_remove]
            ball3_to_remove=-1

        #모든 공을 없앤 경우
        if len(balls)==0 and len(balls2)==0 and len(balls3)==0:
            if level<5:
                game_result="Next Level"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level+=1
                shot=1
                score+=int(total_time-elapsed_time)
                running=False

            else:
                game_result="Mission Complete"
                msg=game_font.render(game_result,True,(255,255,0))
                msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
                screen.blit(msg,msg_rect)
                pygame.display.update()
                level=1
                print("{} 점입니다.".format(score))
                ranking.append("***"+str(score)+"***")
                ranking.append(input("이름을 입력하세요 : "))
                score=0
                n+=1
                running=False

        #r그리기
        screen.blit(background,(0,0))

        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

        for bullet_x_pos, bullet_y_pos in bullets:
            screen.blit(bullet,(bullet_x_pos,bullet_y_pos))
        for bullet2_x_pos, bullet2_y_pos in bullets2:
            screen.blit(bullet2,(bullet2_x_pos,bullet2_y_pos))

        for idx,val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_img_idx = val["img_idx"]
            screen.blit(ball_images[ball_img_idx],(ball_pos_x,20))

        for idx2,val2 in enumerate(balls2):
            ball2_1_pos_x = val2["pos_x"]
            ball2_1_pos_y = val2["pos_y"]
            ball2_1_img_idx = val2["img_idx"]
            screen.blit(ball2_images[ball2_1_img_idx],(ball2_1_pos_x,ball2_1_pos_y))

        for idx3,val3 in enumerate(balls3):
            ball3_pos_x = val3["pos_x"]
            ball3_pos_y = val3["pos_y"]
            ball3_img_idx = val3["img_idx"]
            screen.blit(ball3_images[ball3_img_idx],(ball3_pos_x,ball3_pos_y))

        screen.blit(stage,(0,screen_height-stage_height))
        screen.blit(character,(character_x_pos,character_y_pos))

        elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
        timer = game_font.render("Time : {}".format(int(total_time-elapsed_time)),True,(255,255,255))
        scoreout = game_font.render("Score : {}".format(int(score)),True,(255,255,255))
        levelout = game_font.render("Level : {}".format(int(level)),True,(255,255,255))
        screen.blit(timer,(10,10))
        screen.blit(levelout,(260,10))
        screen.blit(scoreout,(450,10))

        if total_time-elapsed_time <=0:
            game_result="Time Over"
            msg=game_font.render(game_result,True,(255,255,0))
            msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
            screen.blit(msg,msg_rect)
            pygame.display.update()
            level=1
            print("{} 점입니다.".format(score))
            ranking.append(score)
            ranking.append(input("이름을 입력하세요 : "))
            score=0
            n+=1
            shot=1
            running=False
        
        pygame.display.update()

    msg=game_font.render(game_result,True,(255,255,0))
    msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()

    #pygame.time.delay(2000)
    return game_result

def shop():
    global score
    global shot
    global shield
    shoprun=True
    while(shoprun):
        shopvisual=pygame.image.load(os.path.join(image_path,"shop.png"))
        screen.blit(shopvisual,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:

                if event.key == ord('2'):
                    if score>=500:
                        shot=2
                        score-=500
                        print("아이템 구매에 성공했습니다!")
                        shoprun=False
                    elif shot==2:
                        print("이미 소지중입니다.")
                        shoprun=False
                    else:
                        print("점수가 부족합니다.")
                        shoprun=False
                
                if event.key == ord('1'):
                    if score>=1000:
                        shield=1
                        score-=1000
                        print("아이템 구매에 성공했습니다!")
                        shoprun=False
                    elif shield==1:
                        print("이미 소지중입니다.")
                        shoprun=False
                    else:
                        print("점수가 부족합니다.")
                        shoprun=False
                
                if event.key == ord('p'):
                        shoprun=False

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
mainvisual=pygame.image.load(os.path.join(image_path,"main.png"))

running=True
while running:
    screen.blit(mainvisual,(0,0))
    pygame.display.update()

    for event in pygame.event.get():
        #이동 키보드 입력
        if event.type==pygame.KEYDOWN:
            if event.key == ord('s'):
                level=1
                score=0
                n+=1
                game_result=Gameplay()
                break
            if event.key == ord('d'):
                running=False
                break
            if game_result=="Next Level":
                if event.key == ord('n'):
                    if level==2:
                        game_result=Gameplay2()
                    elif level==3:
                        game_result=Gameplay3()
                    elif level==4:
                        game_result=Gameplay4()
                    else:
                        game_result=Gameplay5()
            if event.key == ord('2'):
                level=2
                game_result=Gameplay2()
            if event.key == ord('3'):
                level=3
                game_result=Gameplay3()
            if event.key == ord('4'):
                level=4
                game_result=Gameplay4()
            if event.key == ord('5'):
                level=5
                game_result=Gameplay5()
            if event.key == ord('r'):
                for i in range(int(len(ranking)/2)):
                    result=ranking[2*i]
                    name=ranking[(2*i)+1]

                    print("{}님의 점수는 {}점 입니다.".format(name,result))
            if event.key == ord('p'):
                shop()
            if shield==1:
                if event.key == ord('m'):
                    shield=0
                    if level==2:
                        game_result=Gameplay2()
                    elif level==3:
                        game_result=Gameplay3()
                    elif level==4:
                        game_result=Gameplay4()
                    else:
                        game_result=Gameplay5()


#ptgame 종료
pygame.quit()
