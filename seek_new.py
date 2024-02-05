# -*- coding: utf-8 -*-
# @Time : 2023-10-30 15:29:34
# @Author : Jack
# @File : seek_new.py
# @Software: PyCharm
# @contact: 937587312@qq.com
# -*- 功能说明 -*-
#
# -*- 功能说明 -*-

import os, sys, time
import pygame
import tkinter as tk
from tkinter import filedialog

MW = 500
MH = 400
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FONT = 'C:\Windows\Fonts\simhei.ttf'


class Button:

    def __init__(self, x, y, w, h, txt, bc, font, fs=24):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = txt
        self.bc = bc
        self.font = font
        self.fs = fs
        self.clicked = False

    def draw(self, surface):
        if self.clicked:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(surface, self.bc, self.rect)
        pygame.draw.rect(surface, self.bc, self.rect)
        font = pygame.font.Font(self.font, self.fs)
        text_surface = font.render(self.txt, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


def main():
    pygame.init()

    root = tk.Tk()
    root.withdraw()

    win = pygame.display.set_mode((MW, MH))
    win.fill(WHITE)

    btn1 = Button(100, 100, 250, 30, '选择要查看的文件夹', BLACK, FONT, 20)
    btn1.draw(win)

    btn2 = Button(100, 200, 100, 30, '全屏浏览', BLACK, FONT)
    btn2.draw(win)

    btn3 = Button(300, 200, 100, 30, '开始浏览', BLACK, FONT)
    btn3.draw(win)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            sx, sy = 0, 0
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("down ", event.pos)
                sx, sy = event.pos
                os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(sx, sy)

                if btn1.rect.collidepoint(event.pos):
                    print("选择")
                    file = filedialog.askdirectory()
                    print(file)

                if btn2.rect.collidepoint(event.pos):
                    print("1")

                if btn3.rect.collidepoint(event.pos):
                    print("2")

            # if event.type == pygame.MOUSEBUTTONUP:
            #     print("up ", event.pos)
            #     sx, sy = event.pos
            #     os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(sx, sy)
            #     print(sx, sy)
            # if event.type == pygame.MOUSEMOTION:
            #     print(event.pos)


if __name__ == '__main__':
    main()
