#-------------------------------------------------------------------------------
# Name:        Pygame
# Purpose:
#
# Author:      2202075
#
# Created:     09/05/2016
# Copyright:   (c) 2202075 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, sys, time, random
from pygame.locals import *

color =(0,0,255)
pygame.init()
clock = pygame.time.Clock()

#window
window = pygame.display.set_mode((800,800))
window.fill(color)
pygame.display.set_caption("Fish Feeding")
pygame.mouse.set_visible(False)
#Eat food
def fishHitFood(playerRect, foodList):#function to remove
    for foodStuff in foodList:
        if playerRect.colliderect(foodStuff['rect']):

            foodList.remove(foodStuff)
            return True
    return False
#Hurt by bubbles
def fishHitBubble(playerRect, bubbleList):
    for bub in bubbleList:
        if playerRect.colliderect(bub['rect']):
            return True
    return False

#Text
font = pygame.font.SysFont('comicsansms', 48)#sets up the font type and size
font2 = pygame.font.SysFont('comicsansms', 16)
textcolor =(255, 0, 0)
#function to draw text on the screen
def text(text, font, screen, x, y):
    textobj = font.render(text, 1, textcolor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)#position of top left corner
    screen.blit(textobj, textrect)#draws sentence
#Player
playerRect = pygame.Rect(400,400,100,100)
playerImage = pygame.image.load('PlayerR.png')#imports fish images
playerImage1 = pygame.image.load('PlayerL.png')
playerImage2 = pygame.image.load('PlayerF.png')

#food
food = pygame.image.load('Food.png')


#Bubbles
bubble1 = pygame.image.load('Bubbles1.png')#imports bubble images
bubble2 = pygame.image.load('Bubbles2.png')


#sounds
pygame.mixer.music.load('underwater.mp3')#background music

gulp1 = pygame.mixer.Sound('gulp1.wav')#eating sounds
gulp2 = pygame.mixer.Sound('gulp2.wav')
gulp3 = pygame.mixer.Sound('gulp3.wav')
drown = pygame.mixer.Sound('bubbless.wav')#bubble sound doesnt play instantly, as the bubbles do damage over time instead of instant damage and it disappearing

#pause
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return
#Start Screen
text('Welcome to Fish Feeding!', font, window, 150, 200)
text('To play you must move with WASD or arrow keys', font2, window, 175, 300)
text('You grow bigger when you eat the fish food,', font2, window, 175, 350)
text('and you grow smaller when touching a bubble!', font2, window, 175, 400)
text('Avoid the bubbles, and try to get as big as you can in 60 seconds!', font2, window, 175, 450)
text('As you grow, the screen will change to accommodate your size!', font2, window, 175, 500)
text('Press any key to start!', font, window, 150, 550)

pygame.display.update()
waitForPlayerToPressKey()




while True: #runs starting setting for game
    #size
    size = 100
    totalSize = 100
    maxSize = 100
    sizeCounter = ["10x","8x",'6x','4x','2x','1x']
    magnification = 0
    playerRect = pygame.Rect(400,400,100,100)
    transform = pygame.transform.scale(playerImage, (size,size))#new image sizes for each sideview of fish
    transform1 = pygame.transform.scale(playerImage1, (size,size))
    transform2 = pygame.transform.scale(playerImage2, (size,size))
    #food
    foodSize = 30
    foodList = []
    foodCounter = 0
    needsFood = 50
    foodTransform = pygame.transform.scale(food,(foodSize,foodSize))
    #bubbles
    bubbleList = []
    bubbleX = 100
    bubbleY = 200
    bubbleCounter = 0
    bubbleRise = 100
    bubbleSideCounter = 0
    #sounds
    drownCounter = 0
    musicCounter = 0
    pygame.mixer.music.play(-1,0)#plays music on repeat starting from the start at 0:00

    #Movement
    moveLeft = moveRight = moveUp = moveDown = False
    side = 0
    window.blit(transform2, playerRect)

    t1 = time.time()
    pygame.display.update()
    while True: #runs game loop

        #Decreases the size of everything once the fish gets big enough, so it can grow further without filling up screen
        if size >=300:
            magnification +=1
            size -= 200
            bubbleX1 = bubbleX
            bubbleY1 = bubbleY
            bubbleX = int(bubbleX*.75)
            bubbleY = int(bubbleY*.75)
            dX = bubbleX1 - bubbleX
            dY = bubbleY1 - bubbleY
            foodSize -= 5
            playerRect.inflate_ip(-200,-200)
            #changes player and food size
            foodTransform = pygame.transform.scale(food,(foodSize,foodSize))
            transform = pygame.transform.scale(playerImage, (size,size))
            transform1 = pygame.transform.scale(playerImage1, (size,size))
            transform2 = pygame.transform.scale(playerImage2, (size,size))
            #changes bubble size
            for bub in bubbleList:
                bub['rect'].inflate_ip(-dX,-dY)
                bub['surface'] = pygame.transform.scale(bubble1,(bubbleX,bubbleY))
            pygame.display.update()

        # After the fish grows past a point, it may get smaller than that point, so we need to revert what we did above, making everything bigger
        if maxSize>300 and totalSize <300 or maxSize>500 and totalSize<500 or maxSize>700 and totalSize<700 or maxSize>900 and totalSize<900 or maxSize>1100 and totalSize<1100:
            magnification -= 1
            maxSize = totalSize
            size += 200
            bubbleX1 = bubbleX
            bubbleY1 = bubbleY
            bubbleX = int(bubbleX/.75)
            bubbleY = int(bubbleY/.75)
            dX = bubbleX1 - bubbleX
            dY = bubbleY1 - bubbleY
            foodSize += 5
            playerRect.inflate_ip(200,200)
            foodTransform = pygame.transform.scale(food,(foodSize,foodSize))
            transform = pygame.transform.scale(playerImage, (size,size))
            transform1 = pygame.transform.scale(playerImage1, (size,size))
            transform2 = pygame.transform.scale(playerImage2, (size,size))
            for bub in bubbleList:
                bub['rect'].inflate_ip(dX,dY)
                bub['surface'] = pygame.transform.scale(bubble1,(bubbleX,bubbleY))
            pygame.display.update()

        #Timer
        t2 = time.time()
        dT = t2-t1 #Change in time
        seconds=(60-(dT)) #calculate how many seconds
        if seconds<0: # if the timer is zero or less, end the game
            win ="Yes"
            break

        text(("%.2f" %(seconds)),font,window,300,50) #print how many seconds

        if totalSize <= 20:#if size is less than 20, end the game
            win = "No"
            break

        #Fish food adding & Moving
        addFood = random.randint(1,5)
        foodCounter += addFood
        for foodStuff in foodList:
            if foodStuff['rect'].bottom < 770:
                foodStuff['rect'].move_ip(0,1)
            else:
                foodList.remove(foodStuff)
                window.fill(color)
            window.blit(foodTransform, foodStuff['rect'])
        if foodCounter >= needsFood:
            newFood = {'rect': pygame.Rect(random.randint(0,750),0,foodSize,foodSize)}
            foodList.append(newFood)
            foodCounter = 0

        #Air Bubbles adding & Moving
        bubbleCounter += 1
        for bub in bubbleList:
            if bub['rect'].top >10:
                bub['rect'].move_ip(0,-5)
            else:
                bubbleList.remove(bub)
                window.fill(color)
            window.blit(bub['surface'],bub['rect'])
        if bubbleCounter == bubbleRise:
            randSide = random.randint(0,1)
            if randSide == 0:
                newBubble = {'rect':pygame.Rect(random.randint(0,750),800,bubbleX,bubbleY),'surface':pygame.transform.scale(bubble1,(bubbleX,bubbleY))}
            elif randSide == 1:
                newBubble = {'rect':pygame.Rect(random.randint(0,750),800,bubbleX,bubbleY),'surface':pygame.transform.scale(bubble2,(bubbleX,bubbleY))}
            bubbleList.append(newBubble)
            bubbleCounter = 0

        #Key presses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == ord('m'):#if user presses 'm', the music stops or starts depending if it is on or not
                    if musicCounter == 0:
                        pygame.mixer.music.pause()
                        musicCounter += 1
                    elif musicCounter == 1:
                        pygame.mixer.music.unpause()
                        musicCounter = 0


            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                #Changes fish facing forward if no movement keys are being pressed
                window.fill(color)
                window.blit(transform2, playerRect)
                side = 3

        window.fill(color)
        window.blit(transform2, playerRect)

        #Draws fish food and air bubbles
        for bub in bubbleList:
            window.blit(bub['surface'],bub['rect'])
        for foodStuff in foodList:
            window.blit(foodTransform, foodStuff['rect'])

        #Player movements and drawing in food and bubbles before fish, making the fish sprite always show above the others
        if moveLeft and playerRect.left >= 0:
            window.fill(color)
            for bub in bubbleList:
                window.blit(bub['surface'],bub['rect'])#prints all bubbles
            for foodStuff in foodList:
                window.blit(foodTransform, foodStuff['rect'])#prints all food
            window.blit(transform1, playerRect)
            playerRect.move_ip(-8, 0)
            side = 1
        if moveRight and playerRect.right <= 800:
            window.fill(color)
            for bub in bubbleList:
                window.blit(bub['surface'],bub['rect'])
            for foodStuff in foodList:
                window.blit(foodTransform, foodStuff['rect'])
            window.blit(transform, playerRect)
            playerRect.move_ip(8, 0)
            side = 2
        if moveUp and playerRect.top >= 0:
            if side == 1:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform1, playerRect)
            elif side == 2:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform, playerRect)
            elif side == 3:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform2, playerRect)
            playerRect.move_ip(0, -8)
        if moveDown and playerRect.bottom <= 800:
            if side == 1:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform1, playerRect)
            elif side == 2:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform, playerRect)
            elif side == 3:
                window.fill(color)
                for bub in bubbleList:
                    window.blit(bub['surface'],bub['rect'])
                for foodStuff in foodList:
                    window.blit(foodTransform, foodStuff['rect'])
                window.blit(transform2, playerRect)
            playerRect.move_ip(0, 8)


        #Check if fish collides with food
        if fishHitFood(playerRect, foodList):
            num = random.randint(1,3)
            if num == 1:
                gulp1.play()
            if num == 2:
                gulp2.play()
            if num == 3:
                gulp3.play()
            size += 5
            totalSize += 5
            if totalSize >= maxSize:
                maxSize += 5
            playerRect.inflate_ip(5,5)
            transform = pygame.transform.scale(playerImage, (size,size))
            transform1 = pygame.transform.scale(playerImage1, (size,size))
            transform2 = pygame.transform.scale(playerImage2, (size,size))

        #check if fish collides with bubbles
        if fishHitBubble(playerRect, bubbleList):
            size -= 2
            totalSize -=2
            playerRect.inflate_ip(-2,-2)
            drownCounter += 1
            if drownCounter == 1:
                drown.play()
            transform = pygame.transform.scale(playerImage, (size,size))
            transform1 = pygame.transform.scale(playerImage1, (size,size))
            transform2 = pygame.transform.scale(playerImage2, (size,size))
        elif fishHitBubble(playerRect, bubbleList) == False:
            drown.stop()
            drownCounter = 0


        clock.tick(60)
        #Draws the information at the top
        text("Size: %s"%(totalSize),font2,window,10,10)
        text(("Time left: %.2f" %(seconds)),font2,window,150,10)
        text(("Magnification Multiplier: %s" %(sizeCounter[magnification])),font2,window,500,10)
        pygame.display.update()
        window.fill(color)
        window.blit(transform2, playerRect)


    #This occurs after the time runs out or the user loses
    if win =="Yes": #if  user successfully survives until the timer stops
        color1 = (24, 20, 108)
        font1 = pygame.font.SysFont("Gothic",32)
        window.fill(color1)
        pygame.mixer.music.pause()
        f = open("Score.txt",'a')#adding to the Score notepad list
        name = ""
        x = True
        while x is True:#getting key presses for username
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        name += event.unicode
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == K_RETURN:
                        x = False
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)
            #draws the end screen
            text(("Username: %s"%(name)),font1,window,150,500)
            text(("Congratulations you survived for a minute!"),font1,window,150,300)
            text(("Your final size was %s."%(totalSize)),font1,window,150,350)
            text("Please type your username to enter your score,",font1,window,150,400)
            text("press enter when ready.",font1,window,150,450)
            pygame.display.update()
            window.fill(color1)
        #restarts
        window.fill(color1)
        text("Press any key to start!",font,window,150,300)
        pygame.display.update()
        f.write(str(name) + " " + str(totalSize)+'\n')
        f.close()
        waitForPlayerToPressKey()

    elif win == "No": #User gets below a size of 20 during the game, they lose
        color1 = (106, 22, 39)
        font1 = pygame.font.SysFont("Gothic",32)
        window.fill(color1)
        pygame.mixer.music.pause()#paues music


        text(("Sorry but your fish became too small for it's organs to function"),font1,window,50,300)

        text('Press a key to play again.', font1,window, 50, 400)
        pygame.display.update()
        waitForPlayerToPressKey()







