from driver import *
import random


BG_COL=(255,255,255)
FINISH_COL=(239,242,27)
WALL_COL=(0,0,0)
NP_WALL_COL=(103,97,105)
DOOR_COL=(32,17,171)
PLAYER_COL=(0,255,255)
LOOK_COL=(255,0,0)
BOX_COL=(13,186,19)
BTN_DE_COL=(74,47,47)
BTN_AC_COL=(155,20,222)
BP_COL=(0,162,255)
OP_COL=(255,93,0)
PORTAL_COLS=(BP_COL,OP_COL)

done=False
clock=pygame.time.Clock()

for i in range(64):
    for j in range(64):
        pixel(i,j,*BG_COL)

gamemap=[['E' for _ in range(64)] for _ in range(64)]

# the first five rows will be ignored so we'll just black them out by default
for i in range(5):
    for j in range(64):
        pixel(i,j,*WALL_COL)

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:done=True
    
    # look out for mouse presses
    press=pygame.mouse.get_pressed()
    x,y=pygame.mouse.get_pos()
    x//=PIXEL_SIZE
    y//=PIXEL_SIZE
    r,c=y,x

    
    

    pygame.event.get()
    keys=pygame.key.get_pressed()
    
    # place walls
    if press[0]:
        if not keys[ord(',')]:
            pixel(r,c,*WALL_COL)
            gamemap[r][c]='W'
        else:
            pixel(r,c,*NP_WALL_COL)
            gamemap[r][c]='N'
    if press[2]:
        pixel(r,c,*BG_COL)
        gamemap[r][c]='E'

    # place ending
    if keys[ord('q')]:
        pixel(r,c,*FINISH_COL)
        gamemap[r][c]='F'
    
    # place box
    if keys[ord('x')]:
        # need enough room
        if r<=61 and c<=61:
            for i in range(3):
                for j in range(3):
                    pixel(r+i,c+j,*BOX_COL)
                    gamemap[r][c]='E'
            
            gamemap[r][c]='B'

    fnum=None
    snum=None
    if keys[ord('0')]:fnum=0
    if keys[ord('1')]:fnum=1
    if keys[ord('2')]:fnum=2
    if keys[ord('3')]:fnum=3
    if keys[ord('4')]:snum=4
    if keys[ord('5')]:snum=5
    if keys[ord('6')]:snum=6
    if keys[ord('7')]:snum=7

    # place door
    if fnum!=None:
        if r<=60:
            for i in range(4):
                pixel(r+i,c,*DOOR_COL)
                gamemap[r][c]='E'
            gamemap[r][c]=str(fnum)
    
    # place button
    if snum!=None:
        if c<=61:
            for j in range(3):
                pixel(r,c+j,*BTN_DE_COL)
                gamemap[r][c]='E'
            gamemap[r][c]=str(snum)


    # display everything
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# write the map

with open('map3.lvl','w') as file:
    for line in gamemap:
        file.write(''.join(line)+'\n')