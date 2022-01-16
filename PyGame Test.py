# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 16:10:33 2019

@author: Jasper
"""

import pygame
import numpy as np
import random
import math
import time

pygame.init()

displayWidth = 800
displayHeight = 600
carWidth = 75
carHeight = 40

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
brightRed = (255,0,0)
green = (0,200,0)
brightGreen = (0,255,0)
blue = (0,0,255)

gameName = "Laser Dodges"
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption(gameName)
clock = pygame.time.Clock()

carImg = pygame.image.load('raceCar.png')
carImg = pygame.transform.scale(carImg,(carWidth,carHeight))


def buttonEvent(click):
    if click[0] == 1:
        return True
        
def rectDraw(colour, posX, posY, buttonL, buttonH):
    pygame.draw.rect(gameDisplay, colour, (posX, posY, buttonL, buttonH))

def buttonMain(colourBase, colourActive, posX, posY, buttonL, buttonH):
    pressed = False
    mouse = pygame.mouse.get_pos()
    if posX+buttonL > mouse[0] > posX and posY+buttonH > mouse[1] > posY:
        rectDraw(colourActive, posX, posY, buttonL, buttonH)
        pressed = buttonEvent(pygame.mouse.get_pressed())
    else:
        rectDraw(colourBase, posX, posY, buttonL, buttonH)
    return pressed

def car(x,y):
    gameDisplay.blit(carImg,(x,y))
    
def textObjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def textDisplay(write,size,textTime, centerL, centerH):
    text = pygame.font.Font("freesansbold.ttf",size)
    textSurf, textRect = textObjects(write, text)
    textRect.center = (centerL,centerH)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(textTime)
    
def crash():
    size = 115
    textTime = 1
    textDisplay("You Crashed", size, textTime, displayWidth/2, displayHeight/2)
    

def move(x,y,moveSpeed):
    xChange = 0
    yChange = 0
    angledMoveSpeed = math.sqrt(((moveSpeed**2)/2))
    pressedKeys = pygame.key.get_pressed()
    
        #Angle Movement
    if pressedKeys[pygame.K_UP] and pressedKeys[pygame.K_LEFT] and 0 < x and y > 0:
        yChange = -angledMoveSpeed
        xChange = -angledMoveSpeed
        
    elif pressedKeys[pygame.K_UP] and pressedKeys[pygame.K_RIGHT] and x < displayWidth - carWidth and y > 0:
        yChange = -angledMoveSpeed
        xChange = angledMoveSpeed
        
    elif pressedKeys[pygame.K_DOWN] and pressedKeys[pygame.K_LEFT] and 0 < x and y < displayHeight - carHeight:
        yChange = angledMoveSpeed
        xChange = -angledMoveSpeed
        
    elif pressedKeys[pygame.K_DOWN] and pressedKeys[pygame.K_RIGHT] and x < displayWidth - carWidth and y < displayHeight - carHeight:
        yChange = angledMoveSpeed
        xChange = angledMoveSpeed
        
        #Cartesian Movement
    elif pressedKeys[pygame.K_LEFT] and 0 < x:
        xChange = -moveSpeed
        
    elif pressedKeys[pygame.K_RIGHT] and x < displayWidth - carWidth:
        xChange = moveSpeed
        
    elif pressedKeys[pygame.K_DOWN] and y < displayHeight - carHeight:
        yChange = moveSpeed
        
    elif pressedKeys[pygame.K_UP] and y > 0:
        yChange = -moveSpeed
        
    x += xChange
    y += yChange
        
    return(x,y)
            
def gameIntro():
    intro = True
    
    gameDisplay.fill(white)
    
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        titleTextSize = 100
        textTime = 0
        buttonTextSize = 20
        menuButtonL = 100
        menuButtonH = 50
        #button[text, posX, posY]
        button1 = ["Start", 150, 450]
        button2 = ["Quit", 550, 450]
        
        #buttonMain(colourBase, colourActive, posX, posY, buttonL, buttonH):
        start = buttonMain(green, brightGreen, button1[1], button1[2], menuButtonL, menuButtonH)
        leave = buttonMain(red, brightRed, button2[1], button2[2], menuButtonL, menuButtonH)
        
        #textDisplay(write,size,textTime, centerL, centerH):
        textDisplay(button1[0], buttonTextSize, textTime, (button1[1] + menuButtonL/2), (button1[2] + menuButtonH/2))
        textDisplay(button2[0], buttonTextSize, textTime, (button2[1] + menuButtonL/2), (button2[2] + menuButtonH/2))
        textDisplay(gameName,titleTextSize,textTime,displayWidth/2,displayHeight/2)
        
        if start:
            main()
        if leave:
            intro = False
        
        pygame.display.update()
        clock.tick(15)
        
        
        
    
def main():
    difficulty = 1
    laserWidth = 10
    maxPos = 0 
    """List of tuples: (axis, pos)"""
    laserList = []
    axis = 0
    laserDuration = 0.75
    laserBreak = 0.25
    startTime = time.time()
    x = (displayWidth * 0.5 - (carWidth/2))
    y = (displayHeight * 0.55 - (carHeight/2))
    moveSpeed = 3
    
    gameExit = False
    while not gameExit:
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_c]:
            crash()
            gameExit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
                
                
        x,y = move(x,y,moveSpeed)
   
        gameDisplay.fill(white)
        car(x,y)
        
        elapsedTime = time.time() - startTime


        
        for laserNum in range(difficulty*3 + 3):
            if laserBreak <= elapsedTime <= laserBreak + 0.1 and len(laserList) < (difficulty*3 + 3):
                #If axis = 0, verticle laser. If axis = 1, horizontal laser.
                axis = random.randint(0,1)
                
                if axis == 0:
                    maxPos = displayWidth
                else:
                    maxPos = displayHeight
                    
                pos = random.randint(0, maxPos)
                
                laserList.append((axis, pos))
        for cycle,laserInfo in enumerate(laserList):
            axis = laserInfo[0]
            pos = laserInfo[1]
            if elapsedTime >= laserBreak + laserDuration and not gameExit:
                if axis == 0 and (x <= pos and pos <= x + carWidth or x <= pos + laserWidth and pos + laserWidth <= x + carWidth):
                    gameDisplay.fill(white)
                    car(x,y)
                    crash()
                    gameExit = True
                elif axis == 1 and (y <= pos and pos <= y + carHeight or y <= pos + laserWidth and pos +laserWidth <= y + carHeight):
                    gameDisplay.fill(white)
                    car(x,y)
                    crash()
                    gameExit = True
                if cycle == (difficulty*3 + 3) - 1 and not gameExit:
                    laserList = []
                    startTime = time.time()
            if laserInfo[0] == 0 and elapsedTime >= laserBreak and not gameExit:
                rectDraw(red, laserInfo[1], 0, laserWidth, displayHeight)
            elif laserInfo[0] == 1 and elapsedTime >= laserBreak and not gameExit:
                rectDraw(red, 0, laserInfo[1], displayWidth, laserWidth)
            
        pygame.display.update()
        clock.tick(100)
    gameDisplay.fill(white)

gameIntro()

pygame.quit()
quit()