# -*- coding:utf-8 -*-

from pygame.locals import *
from PIL import Image
import pygame
import sys
import os
import time
import random
from win32com.shell import shell, shellcon

WIN_WIDTH = 800
WIN_HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 40  # 设置帧数40帧
VHNUMS = 3
CELLNUMS = VHNUMS * VHNUMS
MACRANDTIME = 100
ARR = []
DEBUG = False


def getimgs(file):
    for root, ds, fs in os.walk(file):
        for f in fs:
            if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'):
                fullname = os.path.join(root, f)
                yield fullname


def imglen(file):
    for i in getimgs(file):
        ARR.append(i)
    return len(ARR)


# 向左
def moveLeft(board, blackCell):
    if blackCell % VHNUMS == VHNUMS - 1:
        return blackCell
    board[blackCell + 1], board[blackCell] = board[blackCell], board[blackCell + 1]
    return blackCell + 1


# 向右
def moveRight(board, blackCell):
    if blackCell % VHNUMS == 0:
        return blackCell
    board[blackCell - 1], board[blackCell] = board[blackCell], board[blackCell - 1]
    return blackCell - 1


# 向上
def moveUp(board, blackCell):
    if blackCell >= VHNUMS:
        return blackCell
    board[blackCell + VHNUMS], board[blackCell] = board[blackCell], board[blackCell + VHNUMS]
    return blackCell + VHNUMS


# 向下
def moveDown(board, blackCell):
    if blackCell < VHNUMS:
        return blackCell
    board[blackCell - VHNUMS], board[blackCell] = board[blackCell], board[blackCell - VHNUMS]
    return blackCell - VHNUMS


# 是否完成
def isFinished(board, blackCell):
    for i in range(CELLNUMS - 1):
        if board[i] != i:
            return False
    return True


def newGameBoard():
    board = []
    for i in range(CELLNUMS):
        board.append(i)

    blackCell = CELLNUMS - 1
    board[blackCell] = -1
    for i in range(MACRANDTIME):
        direction = random.randint(0, 3)
        if (direction == 0):
            blackCell = moveLeft(board, blackCell)
        elif (direction == 1):
            blackCell = moveRight(board, blackCell)
        elif (direction == 2):
            blackCell = moveUp(board, blackCell)
        elif (direction == 3):
            blackCell = moveDown(board, blackCell)
    return board, blackCell


def quit():
    pygame.quit()
    sys.exit()


def begin(imgl):
    pygame.init()
    mainClock = pygame.time.Clock()

    rnum = random.randint(0, imgl)
    print("index is ", rnum, " addr is ", ARR[rnum])
    gameImage = pygame.image.load(ARR[rnum])
    # gameImage = pygame.image.load(ARR[268])
    print(ARR[rnum])
    # print("img size is ", gameImage.get_width(), gameImage.get_height())
    r = WIN_HEIGHT / gameImage.get_height()  # 比例

    # print(r)
    img2 = pygame.transform.rotozoom(gameImage, 0, r)  # 缩放旋转
    # print("new img size is ", img2.get_width(), img2.get_height())
    windowSurface = pygame.display.set_mode((img2.get_width(), WIN_HEIGHT + 80))  # 游戏窗口
    pygame.display.set_caption('拼图')
    windowSurface.fill(WHITE)  # 背景色
    windowSurface.blit(img2, (0, 0))

    # print(windowSurface.get_width(), windowSurface.get_height())

    cellWidth = int(img2.get_width() / VHNUMS)
    cellHeight = int(img2.get_height() / VHNUMS)
    finish = False
    gameBoard, blackCell = newGameBoard()
    pygame.display.flip()

    return img2, cellWidth, cellHeight, finish, gameBoard, blackCell, windowSurface, mainClock, rnum


def main():
    file = 'E:\\迅雷下载\\'
    # print(os.path.exists(file))
    if os.path.exists(file) == False:
        file = 'F:\\迅雷下载\\'

    imgl = imglen(file)

    img2, cellWidth, cellHeight, finish, gameBoard, blackCell, windowSurface, mainClock, rnum = begin(imgl)

    font = pygame.font.Font('C:\\Windows\\Fonts\\simhei.ttf', 30)

    # bx, by, bw, bh = 40, WIN_HEIGHT + 20, 100, 50
    # pygame.draw.rect(windowSurface, RED, (bx, by, bw, bh))
    # text = font.render('删除', True, WHITE)
    # tw, th = text.get_size()
    # windowSurface.blit(text, (bx + bw / 2 - tw / 2, by + bh / 2 - th / 2))
    #
    # bx, by, bw, bh = 140, WIN_HEIGHT + 20, 100, 50
    # pygame.draw.rect(windowSurface, RED, (bx, by, bw, bh))
    # text = font.render('刷新', True, WHITE)
    # tw, th = text.get_size()
    # windowSurface.blit(text, (bx + bw / 2 - tw / 2, by + bh / 2 - th / 2))
    #
    # bx1, by1, bw1, bh = 300, WIN_HEIGHT + 20, 150, 50
    # pygame.draw.rect(windowSurface, GREEN, (bx1, by1, bw1, bh))
    # text = font.render('开始游戏', True, WHITE)
    # tw1, th1 = text.get_size()
    # windowSurface.blit(text, (bx1 + bw1 / 2 - tw1 / 2, by1 + bh / 2 - th1 / 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                # if event.key == K_LEFT or event.key == ord('a'):
                #     blackCell = moveLeft(gameBoard, blackCell)
                # if event.key == K_RIGHT or event.key == ord('d'):
                #     blackCell = moveRight(gameBoard, blackCell)
                # if event.key == K_UP or event.key == ord('w'):
                #     blackCell = moveUp(gameBoard, blackCell)
                # if event.key == K_DOWN or event.key == ord('s'):
                #     blackCell = moveRight(gameBoard, blackCell)
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = int(x / cellWidth)
                row = int(y / cellHeight)
                index = col + row * VHNUMS
                # print("col ", col, " row ", row, " index ", index, " blackCell ", blackCell, " VHNUMS ", VHNUMS)
                if (
                        index == blackCell - 1 or index == blackCell + 1 or index == blackCell - VHNUMS or index == blackCell + VHNUMS):
                    gameBoard[blackCell], gameBoard[index] = gameBoard[index], gameBoard[blackCell]
                    blackCell = index

                if bx <= x <= bx + bw and by <= y <= by + bh:
                    print("删除")
                    finish = False
                    if os.path.isfile(ARR[rnum]):
                        # os.remove(ARR[rnum])
                        if not DEBUG:
                            res = shell.SHFileOperation((0, shellcon.FO_DELETE, ARR[rnum], None,
                                                         shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                                                         None, None))  # 删除文件到回收站
                            if not res[1]:
                                os.system('del ' + ARR[rnum])
                        print('del over; leave is ', len(ARR))
                        img2, cellWidth, cellHeight, finish, gameBoard, blackCell, windowSurface, mainClock, rnum = begin(
                            imgl)

                if bx1 <= x <= bx1 + bw1 and by1 <= y <= by1 + bh:
                    print("刷新")
                    finish = False
                    img2, cellWidth, cellHeight, finish, gameBoard, blackCell, windowSurface, mainClock, rnum = begin(
                        imgl)

                if bx2 <= x <= bx2 + bw and by2 <= y <= by2 + bh:
                    print("开始")
                    if finish == False:
                        gameBoard, blackCell = newGameBoard()
                        pygame.display.flip()

            if finish:
                continue

        if (isFinished(gameBoard, blackCell)):
            gameBoard[blackCell] = CELLNUMS - 1
            finish = True

        windowSurface.fill(BLACK)

        bx, by, bw, bh = 40, WIN_HEIGHT + 20, 100, 50
        pygame.draw.rect(windowSurface, RED, (bx, by, bw, bh))
        text = font.render('删除', True, WHITE)
        tw, th = text.get_size()
        windowSurface.blit(text, (bx + bw / 2 - tw / 2, by + bh / 2 - th / 2))

        bx2, by2, bw, bh = 160, WIN_HEIGHT + 20, 100, 50
        pygame.draw.rect(windowSurface, RED, (bx2, by2, bw, bh))
        text = font.render('刷新', True, WHITE)
        tw2, th2 = text.get_size()
        windowSurface.blit(text, (bx2 + bw / 2 - tw2 / 2, by2 + bh / 2 - th2 / 2))

        bx1, by1, bw1, bh = 300, WIN_HEIGHT + 20, 150, 50
        pygame.draw.rect(windowSurface, GREEN, (bx1, by1, bw1, bh))
        text = font.render('开始游戏', True, WHITE)
        tw1, th1 = text.get_size()
        windowSurface.blit(text, (bx1 + bw1 / 2 - tw1 / 2, by1 + bh / 2 - th1 / 2))

        for i in range(CELLNUMS):
            rowDst = int(i / VHNUMS)
            colDst = int(i % VHNUMS)
            rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)
            if gameBoard[i] == -1:
                continue
            rowArea = int(gameBoard[i] / VHNUMS)
            colArea = int(gameBoard[i] % VHNUMS)
            rectArea = pygame.Rect(colArea * cellWidth, rowArea * cellHeight, cellWidth, cellHeight)
            windowSurface.blit(img2, rectDst, rectArea)
        for i in range(VHNUMS + 1):
            pygame.draw.line(windowSurface, BLACK, (i * cellWidth, 0), (i * cellWidth, img2.get_height()))
        for i in range(VHNUMS + 1):
            pygame.draw.line(windowSurface, BLACK, (0, i * cellHeight), (img2.get_width(), i * cellHeight))

        pygame.display.update()
        mainClock.tick(FPS)


if __name__ == '__main__':
    main()
