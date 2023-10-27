# -*- coding:utf-8 -*-


import pygame
import os
import random
import sys
import math
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


def quit():
    pygame.quit()
    sys.exit()


def begin(imgl, rnum=0):
    if rnum == 0:
        rnum = random.randint(0, imgl)
    # rnum = 6749
    print("index is ", rnum, " addr is ", ARR[rnum])
    image = pygame.image.load(ARR[rnum])

    # print(image.get_height(), WIN_HEIGHT)
    # print(image.get_width(), WIN_WIDTH)
    # tmp = r = r1 = 1
    # if image.get_height() > WIN_HEIGHT:
    #     r = WIN_HEIGHT / image.get_height()
    #
    # if image.get_width() > WIN_WIDTH:
    #     r1 = WIN_WIDTH / image.get_width()

    r = WIN_HEIGHT / image.get_height()
    r1 = WIN_WIDTH / image.get_width()

    # print(r)
    # print(r1)
    tmp = min(r, r1)

    newimg = pygame.transform.rotozoom(image, 0, tmp)

    win = pygame.display.set_mode((newimg.get_width(), newimg.get_height() + 80), pygame.RESIZABLE)
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption('图片浏览')
    win.blit(newimg, (0, 0))

    font = pygame.font.Font('C:\Windows\Fonts\simhei.ttf', 26)

    return win, newimg, font, rnum, image


def main():
    pygame.init()

    file = 'E:\\迅雷下载\\'
    if os.path.exists(file) == False:
        file = 'F:\\迅雷下载\\'
    index = 0
    imgl = imglen(file)

    win, newimg, font, rnum, image = begin(imgl)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

            if event.type == pygame.VIDEORESIZE:
                w = event.w
                h = event.h

                r = h / image.get_height()
                r1 = w / image.get_width()

                tmp = min(r, r1)

                newimg = pygame.transform.rotozoom(image, 0, tmp)

                win = pygame.display.set_mode((newimg.get_width(), newimg.get_height() + 80), pygame.RESIZABLE)
                win.blit(newimg, (0, 0))
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if bx2 <= x <= bx2 + bw and by2 <= y <= by2 + bh:
                    win, newimg, font, rnum, image = begin(imgl)

                if bx3 <= x <= bx3 + bw and by3 <= y <= by3 + bh:
                    if not DEBUG:
                        res = shell.SHFileOperation((0, shellcon.FO_DELETE, ARR[rnum], None,
                                                     shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                                                     None, None))  # 删除文件到回收站
                        if not res[1]:
                            os.system('del ' + ARR[rnum])
                            ARR.pop(rnum)
                    print('del over; leave is ', len(ARR))
                    win, newimg, font, rnum, image = begin(imgl, rnum)

                if bx1 <= x <= bx1 + bw and by1 <= y <= by1 + bh:
                    win, newimg, font, rnum, image = begin(imgl, rnum - 1)

                if bx4 <= x <= bx4 + bw and by4 <= y <= by4 + bh:
                    win, newimg, font, rnum, image = begin(imgl, rnum + 1)

            bx1, by1, bw, bh = 30, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx1, by1, bw, bh))
            text = font.render('上一页', True, WHITE)
            tw1, th1 = text.get_size()
            win.blit(text, (bx1 + bw / 2 - tw1 / 2, by1 + bh / 2 - th1 / 2))

            bx2, by2, bw, bh = 290, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx2, by2, bw, bh))
            text = font.render('刷新', True, WHITE)
            tw2, th2 = text.get_size()
            win.blit(text, (bx2 + bw / 2 - tw2 / 2, by2 + bh / 2 - th2 / 2))

            bx3, by3, bw, bh = 400, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, RED, (bx3, by3, bw, bh))
            text = font.render('删除', True, WHITE)
            tw3, th3 = text.get_size()
            win.blit(text, (bx3 + bw / 2 - tw3 / 2, by3 + bh / 2 - th3 / 2))

            bx4, by4, bw, bh = 140, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx4, by4, bw, bh))
            text = font.render('下一页', True, WHITE)
            tw4, th4 = text.get_size()
            win.blit(text, (bx4 + bw / 2 - tw4 / 2, by4 + bh / 2 - th4 / 2))

            pygame.display.update()


if __name__ == '__main__':
    main()
