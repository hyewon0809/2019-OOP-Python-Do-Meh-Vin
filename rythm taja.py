#https://www.youtube.com/watch?v=bP6OyB-tC_c&t=9s로부터 게임 진행 아이디어 착안

import pygame, random, time

def initgame() : #게임기본설정
    global f, list, listlen, background, white, green, point, starttime, paper, font, wallpaper

    pygame.init()

    f = open('text.txt', 'r')
    list = f.readlines()
    listlen = len(list)

    background = (200, 200, 255)
    white = (255, 255, 255)
    green = (30, 150, 30)
    point = 0

    paper = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("리듬을 타자")
    font = pygame.font.SysFont("Agency FB", 50)
    wallpaper = pygame.image.load('background.png')


def gamestart(): #게임 시작화면
    global mainpaper, startpaper
    mainpaper = pygame.image.load('main.png')
    startpaper = pygame.image.load('start.png')

    check = True

    paper.fill(background)
    paper.blit(mainpaper, (0, 0))
    pygame.display.update()

    while check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 버튼 누르면 게임 종료
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == 13:  # 엔터키 누르면 화면 넘어가기
                    check = False

    paper.fill(background)
    paper.blit(startpaper, (0, 0))
    pygame.display.update()

    while not check:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 버튼 누르면 게임 종료
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == 13:  # 엔터키 누르면 화면 넘어가기
                    check = True

    return check

def maingame(): #메인게임 진행
    global inputline, point, starttime

    initgame()

    if gamestart():

        pygame.mixer.music.load('music.mp3') #노래 재생
        pygame.mixer.music.play()
        starttime = time.time() + 0.5 #노래 재생 지연 보정


        fileopen()
        changeline(True)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 종료 버튼 누르면 게임 종료
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == 32:  # 스페이스바 예외 처리
                        inputline += ' '
                    else:
                        inputline += pygame.key.name(event.key)  # 누른 키에 해당하는 알파펫 입력문장에 추가

                    if chosenline.startswith(inputline):  # 입력문장과 선택문장 일치시 점수 올리고 문장 교체
                        if chosenline == inputline:
                            point += len(inputline)
                            changeline(True)
                    else:
                        inputline = ''  # 입력 문장과 선택문장 일치하지 않으면 초기화
                        changeline(False)

            #점수와 입력 문장 띄우기
            pointCaption = font.render(str(point), True, green)
            paper.blit(pointCaption, (860, 135))

            input = font.render(str(inputline), True, green)
            paper.blit(input, (190, 570))

            pygame.display.update()

def fileopen(): # txt파일 열고 문장단위로 끊어 읽기
    for i in range(listlen):
        list[i] = list[i].split('=')
        list[i][1] = list[i][1].lower()
    for i in range(listlen - 1):
        list[i][1] = list[i][1][:-1]

    list.insert(0,[-9999999,'test'])
    list.append([999999999999,'last'])

def changeline(change): #문장 교체

    global chosenline, pressedWord, text, pointCaption, timesec, inputline, chosenwords,starttime

    # 화면 초기화
    paper.fill(background)
    paper.blit(wallpaper, (0, 0))

    inputline = '' #입력 글자 초기화

    timesec = time.time() - starttime
    chosenline = list[0][1]

    if(change) : # 문장 맞췄을 때 만 문장 교체 및 삭제

        print(timesec)

        if int(list[0][0]) <= timesec:
            if int(list[1][0]) <= timesec:  # 시간초과시 게임종료
                gameend()
            else:
                del list[0]  # 제 시간 안에 입력시 삭제

                if list[0][1] == 'last':  # 모두 입력하여 리스트가 비었으면 성공
                    gamesuccess()
                    return True
                chosenline = list[0][1]

    chosenwords = chosenline.split(' ') #해당가사 띄어쓰기 단위로 잘라서 랜덤으로 띄우기
    for i in range(len(chosenwords)):
        text = font.render(chosenwords[i], True, white)
        paper.blit(text, (random.randint(100, 600), random.randint(100, 400)))


def gameend(): #시간 초과시 게임 종료
    endpaper = pygame.image.load('end.png')

    paper.fill(background)
    paper.blit(endpaper, (0, 0))
    pygame.mixer.music.stop()

    pygame.display.update()

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 버튼 누르면 게임 종료
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == 13:  # 엔터누르면 다시시작
                    maingame()
                    return True

def gamesuccess(): #게임 성공시 점수 띄우고 게임종료

    successpaper = pygame.image.load('success.png')

    paper.fill(background)
    paper.blit(successpaper, (0, 0))
    pygame.mixer.music.stop()

    point_result = font.render(str(point), True, white)
    paper.blit(point_result, (490, 300))
    pygame.display.update()


    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 버튼 누르면 게임 종료
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == 13:  #enter 누르면 다시 시작
                    maingame()
                    return True

# 게임 시작
maingame()
