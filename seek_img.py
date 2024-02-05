# -*- coding:utf-8 -*-


import pygame
import os
import random
import sys
import math
from win32com.shell import shell, shellcon
from Button import Button
import time
import signal
from inputimeout import inputimeout, TimeoutOccurred
import tkinter as tk
from tkinter import filedialog

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
FONT = 'C:\Windows\Fonts\simhei.ttf'
DEC = r'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\回收站.lnk'


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


def winWH():
    root = tk.Tk()
    root.withdraw()
    winX, winY = root.winfo_screenwidth(), root.winfo_screenheight()
    return winX, winY


def quit():
    pygame.quit()
    sys.exit()


def begin(imgl, rnum=0, num=0, wm=0, hm=0):
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

    # info = pygame.display.Info()
    # wm, hm = info.current_w, info.current_h
    print(num)
    if int(num) == 1:
        print("num is 1 ", wm, hm, image.get_width(), image.get_height())
        win = pygame.display.set_mode((wm, hm), pygame.RESIZABLE)
        r = (hm - 120) / image.get_height()
        r1 = wm / image.get_width()
        tmp = min(r, r1)
        newimg = pygame.transform.rotozoom(image, 0, tmp)
        win.blit(newimg, ((wm - newimg.get_width()) / 2, 0))
    else:
        print("num is 2 ", WIN_WIDTH, WIN_HEIGHT, image.get_width(), image.get_height())
        r = WIN_HEIGHT / image.get_height()
        r1 = WIN_WIDTH / image.get_width()
        tmp = min(r, r1)
        newimg = pygame.transform.rotozoom(image, 0, tmp)
        win = pygame.display.set_mode((newimg.get_width(), newimg.get_height() + 80), pygame.RESIZABLE)
        win.blit(newimg, (0, 0))

    # print(r, r1)
    # tmp = min(r, r1)
    #
    # newimg = pygame.transform.rotozoom(image, 0, tmp)

    # win = pygame.display.set_mode((newimg.get_width(), newimg.get_height() + 80), pygame.RESIZABLE)
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption('图片浏览')
    font = pygame.font.Font(FONT, 26)

    return win, newimg, font, rnum, image


def main():
    pygame.init()

    # root = tk.Tk()
    # root.withdraw()

    winX, winY = winWH()

    file = filedialog.askdirectory()
    print(file)

    if file == "":
        quit()

    # file = 'E:\\迅雷下载\\'
    # if os.path.exists(file) == False:
    #     file = 'F:\\迅雷下载\\'

    print("请选择窗口的大小：1：全屏，2：正常比例")
    num = input("请选择：")
    # try:
    #     num = inputimeout(prompt='请选择：(5秒后将随机选择)', timeout=5)
    # except TimeoutOccurred:
    #     num = random.randint(1, 2)
    #     print('已随机选择！', num)

    if num == "":
        num = 1
    if int(num) == 1:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(0, 30)
        fontSize = 26
    else:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(500, 30)
        fontSize = 20

    info = pygame.display.Info()
    wm, hm = info.current_w, info.current_h - 30

    imgl = imglen(file)
    print("len ", imgl)
    win, newimg, font, rnum, image = begin(imgl, 0, num, wm, hm)
    pygame.display.flip()

    font1 = pygame.font.Font(FONT, 18)

    # bx1, by1, bw, bh = 30, 100 + 20, 100, 50
    # button = Button(bx1, by1, bw, bh, '上一页', GREEN, FONT)
    # button.draw(win)
    # pygame.display.update()

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

                if btn1.rect.collidepoint(event.pos):
                    win, newimg, font, rnum, image = begin(imgl, rnum - 1, num, wm, hm)
                if btn2.rect.collidepoint(event.pos):
                    if rnum + 1 == len(ARR):
                        rnum = -1
                    win, newimg, font, rnum, image = begin(imgl, rnum + 1, num, wm, hm)
                if btn3.rect.collidepoint(event.pos):
                    win, newimg, font, rnum, image = begin(imgl, 0, num, wm, hm)
                if btn4.rect.collidepoint(event.pos):
                    if not DEBUG:
                        res = shell.SHFileOperation((0, shellcon.FO_DELETE, ARR[rnum], None,
                                                     shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                                                     None, None))  # 删除文件到回收站
                        if not res[1]:
                            os.system('del ' + ARR[rnum])
                            ARR.pop(rnum)
                    print('del over; leave is ', len(ARR))
                    if rnum + 1 == len(ARR):
                        rnum = 0
                    win, newimg, font, rnum, image = begin(imgl, rnum, num, wm, hm)

                if num == 1:
                    if btn5.rect.collidepoint(event.pos):
                        os.system("explorer.exe %s" % DEC)

                # x, y = event.pos

                # if bx2 <= x <= bx2 + bw and by2 <= y <= by2 + bh:
                #     win, newimg, font, rnum, image = begin(imgl)
                #
                # if bx3 <= x <= bx3 + bw and by3 <= y <= by3 + bh:
                #     if not DEBUG:
                #         res = shell.SHFileOperation((0, shellcon.FO_DELETE, ARR[rnum], None,
                #                                      shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                #                                      None, None))  # 删除文件到回收站
                #         if not res[1]:
                #             os.system('del ' + ARR[rnum])
                #             ARR.pop(rnum)
                #     print('del over; leave is ', len(ARR))
                #     win, newimg, font, rnum, image = begin(imgl, rnum)
                #
                # if bx1 <= x <= bx1 + bw and by1 <= y <= by1 + bh:
                #     win, newimg, font, rnum, image = begin(imgl, rnum - 1)
                #
                # if bx4 <= x <= bx4 + bw and by4 <= y <= by4 + bh:
                #     win, newimg, font, rnum, image = begin(imgl, rnum + 1)

            y, w, h = newimg.get_height() + 20, 80, 40

            x1, x2, x3, x4, x5 = 30, 140, 290, 400, 550

            btnY = y
            if int(num) == 1:
                w, h = 100, 50
                x1, x2, x3, x4, x5 = 600, 710, 1000, 1110, 1310
                btnY = winY - 130
            btn1 = Button(x1, btnY, w, h, '上一页', GREEN, FONT, fontSize)
            btn1.draw(win)

            btn2 = Button(x2, btnY, w, h, '下一页', GREEN, FONT, fontSize)
            btn2.draw(win)

            btn3 = Button(x3, btnY, w, h, '刷新', GREEN, FONT, fontSize)
            btn3.draw(win)

            btn4 = Button(x4, btnY, w, h, '删除', RED, FONT, fontSize)
            btn4.draw(win)

            if num == 1:
                btn5 = Button(x5, btnY, w, h, 'REC', RED, FONT, fontSize)
                btn5.draw(win)

                tx = x2 + 130
                t = "index is " + str(rnum)
                t1 = "sum len is " + str(len(ARR))
                txt = font1.render(t, True, RED)
                win.blit(txt, (tx, btnY + 5))
                txt = font1.render(t1, True, RED)
                win.blit(txt, (tx, btnY + 30))
                pygame.display.update()

            # bx1, by1, bw, bh = 30, newimg.get_height() + 20, 100, 50
            # pygame.draw.rect(win, GREEN, (bx1, by1, bw, bh))
            # text = font.render('上一页', True, WHITE)
            # tw1, th1 = text.get_size()
            # win.blit(text, (bx1 + bw / 2 - tw1 / 2, by1 + bh / 2 - th1 / 2))

            # bx2, by2, bw, bh = 290, newimg.get_height() + 20, 100, 50
            # pygame.draw.rect(win, GREEN, (bx2, by2, bw, bh))
            # text = font.render('刷新', True, WHITE)
            # tw2, th2 = text.get_size()
            # win.blit(text, (bx2 + bw / 2 - tw2 / 2, by2 + bh / 2 - th2 / 2))
            #
            # bx3, by3, bw, bh = 400, newimg.get_height() + 20, 100, 50
            # pygame.draw.rect(win, RED, (bx3, by3, bw, bh))
            # text = font.render('删除', True, WHITE)
            # tw3, th3 = text.get_size()
            # win.blit(text, (bx3 + bw / 2 - tw3 / 2, by3 + bh / 2 - th3 / 2))
            #
            # bx4, by4, bw, bh = 140, newimg.get_height() + 20, 100, 50
            # pygame.draw.rect(win, GREEN, (bx4, by4, bw, bh))
            # text = font.render('下一页', True, WHITE)
            # tw4, th4 = text.get_size()
            # win.blit(text, (bx4 + bw / 2 - tw4 / 2, by4 + bh / 2 - th4 / 2))

            pygame.display.update()


if __name__ == '__main__':
    main()
