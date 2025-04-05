import pygame
import pygame.gfxdraw
import random
import math

# cols
COL_0=(103,97,105)
COL_1=(0,162,255)
COL_2=(255,93,0)
COL_3=(32,17,171)
COL_4=(5,141,245)
COL_5=(255,255,255)

"""
BG_COL=(255,255,255)
FINISH_COL=(239,242,27)
WALL_COL=(0,0,0)
NP_WALL_COL=
DOOR_COL=(32,17,171)
PLAYER_COL=(0,255,255)
LOOK_COL=(255,0,0)
BOX_COL=(13,186,19)
BTN_DE_COL=(74,47,47)
BTN_AC_COL=(155,20,222)
BP_COL=
OP_COL=
PORTAL_COLS=(BP_COL,OP_COL)
"""

done=False
clock=pygame.time.Clock()

PIXEL_SIZE=1

WIDTH=64
HEIGHT=64
screen=pygame.display.set_mode((WIDTH*PIXEL_SIZE,HEIGHT*PIXEL_SIZE))

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
#my_font = pygame.font.SysFont('Times New Roman', 16)
my_font = pygame.font.SysFont('Ubuntu', 15)

lvl_font=pygame.font.SysFont('Times New Roman',10)

screen.fill(COL_4)

text_surface = my_font.render('Nice!!', False, COL_5)
screen.blit(text_surface, (13,0))

pygame.draw.line(screen,COL_5,(20,20),(20,30))
pygame.draw.line(screen,COL_5,(63-20,20),(63-20,30))

intersect=(20+(63-20))//2
width=(63-20)-20
height=20

#pygame.draw.line(screen,COL_5,(20,35),(intersect,50))
#pygame.draw.line(screen,COL_5,(63-20,35),(intersect,50))

smilerect=pygame.Rect(20,30,width,height)
pygame.draw.arc(screen,COL_5,smilerect,-math.pi,0)

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:done=True
    
    press=pygame.mouse.get_pressed()
    x,y=pygame.mouse.get_pos()
    #r,c=y,x

    pygame.event.get()
    keys=pygame.key.get_pressed()

    if press[0]:
        pygame.gfxdraw.pixel(screen,x,y,COL_5)
    if press[2]:
        pygame.gfxdraw.pixel(screen,x,y,COL_4)


    """

    for i in range(4):
        text=f'Level {i+1}'
        col=COL_2
        if i==3:
            text='Quit'
            col=COL_3
        surf=lvl_font.render(text,False,col)
        screen.blit(surf,(20,20+i*11))
    """

    # display everything
    pygame.display.flip()
    clock.tick(120)


# display the result
out=""

cols=set()
for i in range(64):
    for j in range(64):
        col=screen.get_at((j,i))
        col=(col.r,col.g,col.b)

        char='?'
        if col==COL_0:char='0'
        if col==COL_1:char='1'
        if col==COL_2:char='2'
        if col==COL_3:char='3'
        if col==COL_4:char='4'
        if col==COL_5:char='5'

        out+=char

        #print(col)
        cols.add(col)
    out+='\n'
print(cols)
print(out)
out=out[:-1]
with open('./screens/win.txt','w') as file:file.write(out)


pygame.quit()

# write the map

"""
with open('map.lvl','w') as file:
    for line in gamemap:
        file.write(''.join(line)+'\n')
"""