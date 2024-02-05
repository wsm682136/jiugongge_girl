# -*- coding:utf-8 -*-


import pygame


class Button:

    def __init__(self, x, y, w, h, txt, bc, font, fontSize):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = txt
        self.bc = bc
        self.font = font
        self.fontSize = fontSize
        self.clicked = False

    def draw(self, surface):
        if self.clicked:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(surface, self.bc, self.rect)
        pygame.draw.rect(surface, self.bc, self.rect)
        font = pygame.font.Font(self.font, self.fontSize)
        text_surface = font.render(self.txt, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
