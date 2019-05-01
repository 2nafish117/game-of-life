import pygame as pg
import random
import time
import copy
import pprint
from board import board

scale = 16
height = len(board)
width = len(board[0])
#board = [[0] * width] * height

displayHeight = scale * height
displayWidth = scale * width
greenTex = None
whiteTex = None
orangeTex = None
TextFont = None
FPS = 20
score = 0
frames = 0
isHeld = False

def neighbours(b, x, y):
    nbs = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            xpos = (x + i) % width
            ypos = (y + j) % height
            if b[ypos][xpos] == 1:
                if i != 0 or j != 0:
                    nbs += 1
    return nbs

def gameInput():
    global isHeld
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                isHeld = True
                print("in")
        if event.type == pg.MOUSEBUTTONUP:
            if not pg.mouse.get_pressed()[0]:
                isHeld = False
                print("out")
    #print(isHeld)
    if isHeld:
        xpos, ypos = pg.mouse.get_pos()
        xpos = int(xpos / scale)
        ypos = int(ypos / scale)
        print(xpos)
        print(ypos)
        board[ypos][xpos] = 1
        board[(ypos + 1) % height][(xpos + 1) % width] = 1
        board[(ypos - 1) % height][(xpos + 1) % width] = 1
        board[(ypos + 1) % height][(xpos - 1) % width] = 1
        board[(ypos - 1) % height][(xpos - 1) % width] = 1
    return

def gameUpdate():
    boardCopy = copy.deepcopy(board)
    for x in range(width):
        for y in range(height):
            nbs = neighbours(boardCopy, x, y)
            if boardCopy[y][x] == 1:
                if nbs < 2:
                    board[y][x] = 0
                if nbs > 3:
                    board[y][x] = 0
                if nbs in [2, 3]:
                    board[y][x] = 1
            if boardCopy[y][x] == 0:
                if nbs == 3:
                    board[y][x] = 1
    #pprint.pprint(board)
    return

def gameRender():
    #render board
    for y in range(0, height):
        for x in range(0, width):
            if board[y][x] == 1:
                gameDisplay.blit(greenTex, (scale * x, scale * y))
            if board[y][x] == 0:
                gameDisplay.blit(whiteTex, (scale * x, scale * y))

    renderText('frames:' + str(frames), 2, 1)
    return

def renderText(text, x:int, y:int):
    gameText = TextFont.render(str(text), True, (255, 255, 255))
    gameRect = gameText.get_rect()
    gameRect.centerx = x * scale
    gameRect.centery = y * scale
    gameDisplay.blit(gameText, gameRect)


if __name__ == '__main__':
    pg.init()
    gameDisplay = pg.display.set_mode((displayWidth, displayHeight))
    pg.display.set_caption('Game Of Life!')
    clock = pg.time.Clock()

    greenTex = pg.image.load('textures/green.png').convert()
    whiteTex = pg.image.load('textures/white.png').convert()
    orangeTex = pg.image.load('textures/orange.png').convert()
    TextFont = pg.font.Font('fonts/Digital_tech.otf', scale)
    
    gameIsRunning = True

    while gameIsRunning:

            
        frames += 1
        gameInput()
        gameUpdate()
        gameRender()
        
        pg.display.update()
        clock.tick(FPS)

    pg.quit()
    quit()