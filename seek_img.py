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


def begin(imgl):
    rnum = random.randint(0, imgl)

    print(ARR[rnum])
    image = pygame.image.load(ARR[rnum])

    tmp = r = r1 = 1
    if image.get_height() > WIN_HEIGHT:
        r = WIN_HEIGHT / image.get_height()
    if image.get_width() > WIN_WIDTH:
        r1 = WIN_WIDTH / image.get_width()

    tmp = min(r, r1)

    newimg = pygame.transform.rotozoom(image, 0, tmp)

    win = pygame.display.set_mode((newimg.get_width(), newimg.get_height() + 80))
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption('图片浏览')
    win.blit(newimg, (0, 0))

    font = pygame.font.Font('C:\Windows\Fonts\simhei.ttf', 26)

    return win, newimg, font, rnum

    pass


def main():
    pygame.init()

    file = 'E:\\迅雷下载\\'
    if os.path.exists(file) == False:
        file = 'F:\\迅雷下载\\'

    imgl = imglen(file)
    win, newimg, font, rnum = begin(imgl)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if bx <= x <= bx + bw and by <= y <= by + bh:
                    print("上一张")
                    win, newimg, font, rnum = begin(imgl)
                    pass
                if bx2 <= x <= bx2 + bw and by2 <= y <= by2 + bh:
                    print("刷新")
                    win, newimg, font, rnum = begin(imgl)
                    pass
                if bx3 <= x <= bx3 + bw and by3 <= y <= by3 + bh:
                    print("删除")
                    if not DEBUG:
                        res = shell.SHFileOperation((0, shellcon.FO_DELETE, ARR[rnum], None,
                                                     shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                                                     None, None))  # 删除文件到回收站
                        if not res[1]:
                            os.system('del ' + ARR[rnum])
                    print('del over')
                    win, newimg, font, rnum = begin(imgl)
                    pass
                if bx1 <= x <= bx1 + bw and by1 <= y <= by1 + bh:
                    print("下一张")
                    win, newimg, font, rnum = begin(imgl)
                    pass

            bx, by, bw, bh = 40, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx, by, bw, bh))
            text = font.render('上一张', True, WHITE)
            tw, th = text.get_size()
            win.blit(text, (bx + bw / 2 - tw / 2, by + bh / 2 - th / 2))

            bx2, by2, bw, bh = 160, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx2, by2, bw, bh))
            text = font.render('刷新', True, WHITE)
            tw2, th2 = text.get_size()
            win.blit(text, (bx2 + bw / 2 - tw2 / 2, by2 + bh / 2 - th2 / 2))

            bx3, by3, bw, bh = 280, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, RED, (bx3, by3, bw, bh))
            text = font.render('删除', True, WHITE)
            tw3, th3 = text.get_size()
            win.blit(text, (bx3 + bw / 2 - tw3 / 2, by3 + bh / 2 - th3 / 2))

            bx1, by1, bw1, bh = 400, newimg.get_height() + 20, 100, 50
            pygame.draw.rect(win, GREEN, (bx1, by1, bw1, bh))
            text = font.render('下一张', True, WHITE)
            tw1, th1 = text.get_size()
            win.blit(text, (bx1 + bw1 / 2 - tw1 / 2, by1 + bh / 2 - th1 / 2))

            pygame.display.update()

    pass


if __name__ == '__main__':
    main()
