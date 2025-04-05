import pygame
import random

# cols
COL_0=(103,97,105)
COL_1=(0,162,255)
COL_2=(255,93,0)
COL_3=(32,17,171)

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
my_font = pygame.font.SysFont('Ubuntu', 18)

lvl_font=pygame.font.SysFont('Times New Roman',10)

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:done=True
    
    screen.fill(COL_0)

    text_surface = my_font.render('PORTAL', False, COL_1)
    screen.blit(text_surface, (0,0))

    for i in range(4):
        text=f'Level {i+1}'
        col=COL_2
        if i==3:
            text='Quit'
            col=COL_3
        surf=lvl_font.render(text,False,col)
        screen.blit(surf,(20,20+i*11))

    # display everything
    pygame.display.flip()
    clock.tick(60)


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

        out+=char

        #print(col)
        cols.add(col)
    out+='\n'
print(cols)
print(out)
out=out[:-1]
with open('./screens/select.txt','w') as file:file.write(out)


pygame.quit()

# write the map

"""
with open('map.lvl','w') as file:
    for line in gamemap:
        file.write(''.join(line)+'\n')
"""