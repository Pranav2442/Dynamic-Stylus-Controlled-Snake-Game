import pygame as py,cv2 as cv,numpy as np, math,os,time,random

py.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue=(0,0,255)
orange=(0, 128,255)
cap=cv.VideoCapture(0)

l=[0,0,0]
m=[0,0,0]
n=0

# score=0
# highscore=0
while (cap.isOpened()):
    ret,frame=cap.read()
    frame=cv.flip(frame,1)
    frame=cv.putText(frame,"Allign your stylus on the Rectangle",(20,40),cv.FONT_HERSHEY_PLAIN,2,black,2)
    frame=cv.putText(frame,"Press C after Alligning the stylus ",(20,380),cv.FONT_HERSHEY_PLAIN,2,black,2)
    cv.rectangle(frame,(310,230),(330,250),(0,0,255),2)
    
    
    
    cv.imshow("Caputruing......",frame)

    if cv.waitKey(1)==99:
        break

# cv.waitKey(10000)
img=frame[230:250,310:330]
img=cv.cvtColor(img,cv.COLOR_BGR2HSV)

for i in range(0,20):
    for j in range (0,20):
        if img[i,j][0]!=0:
            l=l+img[i,j]
            n=n+1
m=l//n

cap.release
cv.destroyAllWindows()


screenw = 900
screenh = 600
gameWindow = py.display.set_mode((screenw, screenh))

py.display.set_caption("Dynamic Stylus Snake Game")
py.display.update()
clock = py.time.Clock()
font = py.font.SysFont(None, 55)


snakepiece = 10
snake_speed = 12


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def gameover(score,highscore):
    font1 = py.font.SysFont('times new roman', 90)
    gamesurface = font1.render('GAME OVER :)', True, red)
    # gamesurface1 = font1.render('Try again Later', True, red)
    gamerect = gamesurface.get_rect()
    # gamerect1 = gamesurface1.get_rect()
    gamerect.midtop = (screenw/2, screenh/2)
    # gamerect1.midtop = ((screenw-700),(screenh-200))
    gameWindow.fill(black)
    gameWindow.blit(gamesurface, gamerect)
    # gameWindow.blit(gamesurface1, gamerect1)
    
    text_screen("score: "+str(score),red,10,10)
    text_screen("High Score: "+str(highscore),red,(screenw-280),10)
    
    py.display.flip()
    time.sleep(5)
    
    py.quit()
    
    exit()


def welcome():
    quitgame = False
    while not quitgame:
        gameWindow.fill((233,210,229))
        text_screen("Welcome to Dynamic Stylus Snake Game", black, 70, 150)
        text_screen("Have a Great Time!!!!!", black, 280,500 )
        text_screen("Press F To Play", black, 320,(screenh/2))
        for event in py.event.get():
            if event.type == py.QUIT:
                quitgame = True
                # gameend()
            if event.type == py.KEYDOWN:
                if event.key == py.K_f:
                    
                    quitgame=True
                    gameLoop()

        py.display.update()
        clock.tick(120)

# l1 = sqrt((x1 - x2)**2 + (y1 - y2)**2)
# l2 = sqrt((x2 - x3)**2 + (y2 - y3)**2)
# l3 = sqrt((x3 - x1)**2 + (y3 - y1)**2)




def Area(a1, b1, a2, b2, a3, b3):
    return abs(((a1 * (b2 - b3) + a2 * (b3 - b1) + a3 * (b1 - b2)))*0.5)


def check_region(a1, b1, a2, b2, a3, b3, xcor, ycor):
    A = Area(a1, b1, a2, b2, a3, b3)
    Area1 = Area(xcor, ycor, a2, b2, a3, b3)
    Area2 = Area(a1, b1, xcor, ycor, a3, b3)
    Area3 = Area(a1, b1, a2, b2, xcor, ycor)
    if A == (Area1 + Area2 + Area3):
        return True
    else:
        return False

def snake(snakepiece, snakelist):
    for i in snakelist:
        py.draw.rect(gameWindow, (255,255,0), [i[0], i[1], snakepiece, snakepiece])

highscores=[]

def gameLoop():
    gameend = False
    quitgame = False

    dir = 'r'
    change_of_dir = dir

    
    
    score=0
    highscore=0
    
    corx = 0
    cory = 0
    
    

    
    X1 = screenw / 2
    Y1 = screenh / 2

    x1_vel = 0
    y1_vel = 0

    snakelist = []
    snakelength = 1
    score=0
    if(not os.path.exists("highscore.txt")):
       with open("highscore.txt", "w") as f:
           f.write("0")
    with open("highscore.txt", "r") as f:
            highscore = f.read()

    foodxcor = round(random.randint(100, screenw-100)) 
    foodycor = round(random.randint(100, screenh-100))



    
    def block1():
        
        py.draw.rect(gameWindow, blue, [40,30,80,80])
        py.draw.rect(gameWindow, blue, [40, 480, 80, 50])
        py.draw.rect(gameWindow, blue, [810, 20, 60, 100])
        py.draw.rect(gameWindow, blue, [810, 480, 80, 50])
        
    def block2():
        
        py.draw.rect(gameWindow, blue, [300, 20, 400, 20])
        py.draw.rect(gameWindow, blue, [300, 570, 400, 20])
        py.draw.rect(gameWindow, blue, [40, 40, 20, 520])
        py.draw.rect(gameWindow, blue, [850,40,20,530])

    def block3():
        
        py.draw.rect(gameWindow, blue,[40,30,80,80] )
        py.draw.rect(gameWindow, blue, [300, 570, 400, 20])
        py.draw.rect(gameWindow, blue, [425, 325, 50, 50])
        py.draw.rect(gameWindow, blue, [850,40,20,530])


    blocks = [block1,block2,block3]
    br = random.choice([0, 1,2])

    if br == 0 or 1 or 2 :
        dir = 'r'
    

    while not gameend:
        
        
        

        
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)
        frame = cv.resize(frame,(630,480))
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        
        lower = np.array([m[0] - 30, m[1] - 30, m[2] - 30])
        uper = np.array([m[0] + 30, m[1] + 30, m[2] + 30])

        
        mask = cv.inRange(hsv, lower, uper)

        k = np.ones((5, 5), np.uint8)

        
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, k)
        opening = cv.morphologyEx(closing, cv.MORPH_OPEN, k)
        blur = cv.GaussianBlur(opening, (5, 5), 0)

        
        __, thresh = cv.threshold(blur, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, 1, 2)

        
        frame = cv.line(frame, (0, 0), (630, 480), (0, 0, 0), 5)
        frame = cv.line(frame, (0, 480), (630, 0), (0, 0, 0), 5)

        
        frame = cv.putText(frame, 'left', (100, 240), cv.FONT_HERSHEY_DUPLEX, 1, orange, 2, cv.LINE_AA)
        frame = cv.putText(frame, 'Right', (450, 240), cv.FONT_HERSHEY_DUPLEX, 1, orange, 2, cv.LINE_AA)
        frame = cv.putText(frame, 'Up', (305, 170), cv.FONT_HERSHEY_DUPLEX, 1, orange, 2, cv.LINE_AA)
        frame = cv.putText(frame, 'Down', (280, 340), cv.FONT_HERSHEY_DUPLEX, 1, orange, 2, cv.LINE_AA)

        cv.imshow('Controller', frame)
        
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break


        if len(contours) > 0:
            cnt = contours[0]
            M = cv.moments(cnt)
            corx = int(M['m10']/M['m00'])
            cory = int(M['m01']/M['m00'])
            

        l = check_region(0,0,240,240,0,480,corx,cory)
        r = check_region(480,0,480,480,240,240,corx,cory)
        u = check_region(0,0,480,0,240,240,corx,cory)
        d = check_region(0,480,240,240,480,480,corx,cory)
        
        
            
                # with open("highscore.txt","w") as f:
                #     f.write(str(highscore))


        while  quitgame == True:
            with open("highscore.txt", "w") as f:
               f.write(str(highscore))
            gameWindow.fill((0, 0, 0))
            text_screen("You Lost!!!! Press F: Play Again ", (213, 50, 80),100,100)
            text_screen("or", red,430,180)
            text_screen("Press Q: Quit ;)",(205, 50, 80) ,320,250)
            text = font.render("Gamers Don't Die They Respawn", True,orange)
            textRect = text.get_rect()
            textRect.center = (450,550)
            gameWindow.blit(text, textRect)
 
            # text_screen("Gamer's Dont't Die They Respawn", (213, 50, 80),300,500)
            # text_screen("High score: "+str(highscore),red,200,200)
            text_screen("score: "+str(score),red,395,400)
            
            py.display.update()

            
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        # text_screen("High score : "+str(highscore),red,100,100)
                        # text_screen("score : "+str(score),red,100,100)
                        gameover(score,highscore)
                        # gameend = True
                        # quitgame = False
                    if event.key == py.K_f:
                        gameLoop()



        if u:
            change_of_dir='u'
        if d:
            change_of_dir='d'
        if l:
            change_of_dir='l'
        if r:
            change_of_dir='r'


        if change_of_dir=='u':
            dir='u'
        if change_of_dir=='d' :
            dir='d'
        if change_of_dir=='l':
            dir='l'
        if change_of_dir=='r':
            dir='r'

        if dir=='u':
            y1_vel=-snakepiece
            x1_vel=0
        if dir=='d':
            y1_vel=snakepiece
            x1_vel=0
        if dir=='l':
            x1_vel=-snakepiece
            y1_vel=0
        if dir=='r':
            x1_vel=snakepiece
            y1_vel=0

        if X1>=screenw or X1<0 or Y1>=screenh or Y1<0:
            quitgame = True


        X1=X1+x1_vel
        Y1=Y1+y1_vel
        gameWindow.fill((0, 0, 0))
        py.draw.rect(gameWindow, (234,165,70), [foodxcor, foodycor, snakepiece, snakepiece])
        Head=[]
        Head.append(X1)
        Head.append(Y1)
        snakelist.append(Head)
        
        if len(snakelist)>snakelength:
            del snakelist[0]

        for h in snakelist[:-1]:
            if h == Head:
                quitgame = True

        
        blocks[br]()

        
        if (br == 0):
            if (20 < X1 < 130 and 10 < Y1 < 120) or (
                    20 < X1 < 130 and 460< Y1 < 540) or (790 < X1 < 880 and 0< Y1 < 130 ) or (790 < X1 < 880 and 460< Y1 < 540):
                quitgame = True
        elif (br == 1):
            if (280 < X1 < 710 and 0 < Y1 < 50) or (
                    280 < X1 < 710 and 550< Y1 < 600) or (20 < X1 < 70 and 20< Y1 < 570 ) or ( 830< X1 < 880 and 20< Y1 < 580):
                quitgame = True
        elif (br == 2):
            if (20 < X1 < 130 and 10 < Y1 < 120) or (
                    280 < X1 < 710 and 550< Y1 < 600) or (405 < X1 < 485 and 305< Y1 < 385 ) or ( 830< X1 < 880 and 20< Y1 < 580):
                quitgame = True
        
        
        if(len(snakelist)>snakelength):
            del snakelist[0]
        snake(snakepiece,snakelist)
        

        # py.display.update()
        # X1 = X1 + snakepiece
        # Y1 = Y1 + snakepiece

        
        if abs(X1-foodxcor)<5 and (Y1-foodycor)<5:
            score=score+10
            foodxcor=round(random.randint(10, screenw-20))
            foodycor=round(random.randint(10, screenh-20))
            snakelength+=1
            if score>int(highscore):
                   highscore = score
                #    highscores.append(highscore)
        text_screen("Score: "+str(score),red,10,7)
        text_screen("High Score"+str(highscore),(255,255,255),(screenw-280),10)
            # score=score+10

        
        # highscores.sort()
        # highscore=highscores[-1]

        py.display.update()
        clock.tick(snake_speed)
    
welcome()



