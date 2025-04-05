import pygame

PIXEL_SIZE=8

WIDTH=64
HEIGHT=64

screen=pygame.display.set_mode((WIDTH*PIXEL_SIZE,HEIGHT*PIXEL_SIZE))

buf=[[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

def pixel(r,c,red,green,blue):
    if not inb(r,c):
        assert False
        return

    buf[r][c]=(red,green,blue)
    rect=pygame.Rect((c*PIXEL_SIZE,r*PIXEL_SIZE),(PIXEL_SIZE,PIXEL_SIZE))
    pygame.draw.rect(screen,(red,green,blue),rect)

def inb(r,c):
    return 0<=r<HEIGHT and 0<=c<WIDTH