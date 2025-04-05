from driver import *
import random

# cols
BG_COL=(255,255,255)
FINISH_COL=(239,242,27)
SCORE_COL=(7,232,240)
WALL_COL=(0,0,0)
NP_WALL_COL=(103,97,105)
DOOR_COL=(32,17,171)
PLAYER_COL=(0,255,255)
LOOK_COL=(255,0,0)
BOX_COL=(13,186,19)
BOX_CONSUME_COL=(13,187,19)
BTN_DE_COL=(74,47,47)
BTN_AC_COL=(155,20,222)
BP_COL=(0,162,255)
OP_COL=(255,93,0)
PORTAL_COLS=(BP_COL,OP_COL)

def check_on_floor():
    global on_floor
    on_floor=False

    if player_row+player_height==HEIGHT:
        on_floor=True
        return

    # check pixels below us
    row=player_row+player_height
    for j in range(player_col,player_col+player_width):
        col_below=buf[row][j]
        if col_below in (WALL_COL,NP_WALL_COL,DOOR_COL,BTN_AC_COL,BTN_DE_COL,*PORTAL_COLS):
            on_floor=True

def check_portals():
    global where_portal,where_portal_type
    where_portal=-1
    where_portal_type=0

    # check left
    if player_col>0:
        col=buf[player_row][player_col-1]
        if col==BP_COL:
            where_portal=0
            where_portal_type=0
        elif col==OP_COL:
            where_portal=0
            where_portal_type=1
    
    # check right
    if player_col+player_width<64:
        col=buf[player_row][player_col+player_width]
        if col==BP_COL:
            where_portal=1
            where_portal_type=0
        elif col==OP_COL:
            where_portal=1
            where_portal_type=1
            

def check_wall_left():
    global wall_left
    wall_left=False

    if player_col==0:
        wall_left=True
        return
    
    # check to the left of us
    col=player_col-1
    for r in range(player_row,player_row+player_height):
        col_below=buf[r][col]
        if col_below in (WALL_COL,NP_WALL_COL,DOOR_COL,BTN_AC_COL,BTN_DE_COL,*PORTAL_COLS):
            wall_left=True

def check_wall_right():
    global wall_right
    wall_right=False

    if player_col+player_width==WIDTH:
        wall_right=True
        return
    
    # check to the right of us
    col=player_col+player_width
    for r in range(player_row,player_row+player_height):
        col_below=buf[r][col]
        if col_below in (WALL_COL,NP_WALL_COL,DOOR_COL,BTN_AC_COL,BTN_DE_COL,*PORTAL_COLS):
            wall_right=True

# are we on a button?
def check_button():
    global player_button,button_pixels
    player_button=0
    button_pixels=0

    r=player_row+player_height
    if r>=64:return

    for j in range(player_col,player_col+player_width):
        t=objbuf[r][j]
        if 4<=t<8:
            player_button=t
            button_pixels+=1

def draw_door(col):
    r,c=objloc[player_button-4]
    for i in range(4):
        pixel(r+i,c,*col)

def draw_btn(col):
    r,c=objloc[player_button]
    for j in range(3):
        pixel(r,c+j,*col)

def interact_button():
    global keys_work,player_boxes
    if player_button==0:return
    # we can either take the cube from the button, or put the cube on the button (box i mean lmao)
    ac=objstate[player_button-4]
    if not ac:
        if player_boxes<=0:return

        objstate[player_button-4]=1 # activate it
        draw_door(BG_COL) # delete the wall
        draw_btn(BTN_AC_COL) # draw the btn

        # take away the cube
        player_boxes-=1

        keys_work=False
    
    if ac:
        objstate[player_button-4]=0 # deactivate it
        draw_door(DOOR_COL) # draw the wall
        draw_btn(BTN_DE_COL) # draw the btn

        # give the cube
        player_boxes+=1
        keys_work=False

def eat_box(y,x):
    global player_boxes,cur_score
    
    while y>=0:
        if buf[y][x]!=BOX_COL:break
        y-=1
    
    y+=1
    
    while x>=0:
        if buf[y][x]!=BOX_COL:break
        x-=1
    
    x+=1
    
    for i in range(3):
        for j in range(3):
            pixel(y+i,x+j,*BG_COL)
    
    player_boxes+=1
    for i in range(10):increase_score()

def decrease_score():
    global cur_score
    if cur_score<=0:return

    for i in range(1,4):
        pixel(i,cur_score-1,*WALL_COL)
    
    cur_score-=1

def increase_score():
    global cur_score
    if cur_score>=64:return

    for i in range(1,4):
        pixel(i,cur_score,*SCORE_COL)
    
    cur_score+=1

def draw_player(colour):
    # see if there's a cube in our midst
    for i in range(player_row,player_row+player_height):
        for j in range(player_col,player_col+player_width):
            if buf[i][j]==BOX_COL:
                eat_box(i,j)
            if buf[i][j]==FINISH_COL:
                levels_beat[curlevel]=1
                return


    for i in range(player_row,player_row+player_height):
        for j in range(player_col,player_col+player_width):
            pixel(i,j,*colour)
    
    # draw where we are looking
    if colour==BG_COL:return
    if player_dir==0:
        pixel(player_row,player_col,*LOOK_COL)
    elif player_dir==1:
        pixel(player_row,player_col+player_width-1,*LOOK_COL)
    elif player_dir==2:
        pixel(player_row,player_col+1,*LOOK_COL)
    
    # box?
    if player_boxes>0:
        pass
        pixel(player_row+1,player_col+1,*BOX_CONSUME_COL)
        pixel(player_row+2,player_col+1,*BOX_CONSUME_COL)
        

def good_portal_loc(loc,ptype):
    for i in range(4):
        pos=(loc[0]+i,loc[1])
        if buf[pos[0]][pos[1]] not in (WALL_COL,PORTAL_COLS[ptype]):return False
    return True


def pass_through_portal():
    global player_row,player_col,keys_work
    #print('going!')

    # TODO: check if we have room maybe? (optional)
    pthrough=1-where_portal_type
    if portal_locs[pthrough]==None:return

    #print('pthrough portal',pthrough)

    # if the portal was shot from the left...
    if portal_dir[pthrough]==0:
        #print('dir 0')
        new_pos=portal_locs[pthrough]
        new_pos=(new_pos[0],new_pos[1]+1)
    elif portal_dir[pthrough]==1:
        #print('dir 1')
        #print('heres the loc',pthrough,portal_locs[pthrough])
        new_pos=portal_locs[pthrough]
        new_pos=(new_pos[0],new_pos[1]-player_width)
    else:
        new_pos=portal_locs[pthrough]
        new_pos=(new_pos[0]+1,new_pos[1])
    
    if portal_dir[pthrough]==portal_dir[1-pthrough]:
        keys_work=False
    
    # is this a safe location?
    for i in range(4):
        for j in range(3):
            cl=buf[new_pos[0]+i][new_pos[1]+j]
            if cl not in (BOX_COL,BG_COL):return
    
    player_row=new_pos[0]
    player_col=new_pos[1]

    decrease_score()

def portal_shot(ptype):
    if player_dir==2:portal_shot_up(ptype)
    else:portal_shot_lr(ptype)

def remove_old_portal(ptype):
    if portal_locs[ptype]==None:return
    if portal_dir[ptype]<2:
        for i in range(4):
            pixel(portal_locs[ptype][0]+i,portal_locs[ptype][1],*WALL_COL)
    else:
        for i in range(4):
            pixel(portal_locs[ptype][0],portal_locs[ptype][1]+i,*WALL_COL)

# call this when we want to shoot a portal
def portal_shot_lr(ptype):
    # direction (in which to raycast): 0 left, 1 right, 2 upward
    # ptype (portal type): 0 blue, 1 orange

    # determine the starting pos to raycast
    cur_pos=(player_row,player_col-1)
    delta=-1
    if player_dir==1:
        cur_pos=(player_row,player_col+player_width)
        delta=1
    
    # raycast!
    good=False
    while inb(*cur_pos):
        # are we on a wall or a portal?
        cur_col=buf[cur_pos[0]][cur_pos[1]]
        if cur_col in(WALL_COL,PORTAL_COLS[ptype]):
            good=True
            break
        elif cur_col==BOX_COL or cur_col==BG_COL:
            pass
        else:
            return

        cur_pos=(cur_pos[0],cur_pos[1]+delta)

    good=good and good_portal_loc(cur_pos,ptype)
    if not good:return

    # remove the old portal if it exists (TODO)
    remove_old_portal(ptype)

    # OPERATION: construct a portal at cur_pos
    for i in range(4):
        pixel(cur_pos[0]+i,cur_pos[1],*PORTAL_COLS[ptype])
    
    # make changes
    portal_locs[ptype]=cur_pos
    portal_dir[ptype]=player_dir

def portal_shot_up(ptype):
    cur_pos=(player_row-1,player_col+1)
    good=False
    while inb(*cur_pos):
        # are we on a wall or a portal?
        cur_col=buf[cur_pos[0]][cur_pos[1]]
        if cur_col==NP_WALL_COL:return
        elif cur_col in(WALL_COL,PORTAL_COLS[ptype]):
            good=True
            break
        elif cur_col==BOX_COL or cur_col==BG_COL:
            pass
        else:
            return
        
        cur_pos=(cur_pos[0]-1,cur_pos[1])
    
    if not good:return

    for i in range(4):
        c=buf[cur_pos[0]][cur_pos[1]+i]
        if c!=WALL_COL and c!=PORTAL_COLS[ptype]:return
    
    # remove the old portal if it exists (TODO)
    remove_old_portal(ptype)

    # OPERATION: construct a portal at cur_pos
    for i in range(4):
        pixel(cur_pos[0],cur_pos[1]+i,*PORTAL_COLS[ptype])
    
    # make changes
    portal_locs[ptype]=cur_pos
    portal_dir[ptype]=2

def init_level():
    global player_row,player_col,player_button,player_boxes,player_width,player_height,on_floor,wall_left,wall_right,keys_work
    global where_portal,where_portal_type
    global objloc,objstate
    global objbuf
    global portal_locs,portal_dir
    global player_dir
    global cur_score
    global partial_frames,button_pixels

    player_row=56
    player_col=2

    player_button=0

    player_boxes=0 # how many cubes the player has

    player_width=3
    player_height=4

    on_floor=False
    wall_left=False
    wall_right=False

    keys_work=False

    where_portal=-1 # -1 if there is no portal to our left/right, 0 if there is a portal to our left, 1 if there is one to our right
    where_portal_type=0 # 0 for blue, 1 for orange

    objloc=[
    (-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)
    ]
    objstate=[0,0,0,0] # 0 deactivated, 1 activated

    objbuf=[[-2 for _ in range(64)] for _ in range(64)]

    # idx 0 is blue, idx 1 is orange
    portal_locs=[
        None,
        None
    ]

    # which direction we shot the portal in
    # 0 is left
    # 1 is right
    # 2 is upward
    portal_dir=[
        None,
        None
    ]

    player_dir=1 # 0 - left, 1 - right, 2 - up

    # initial graphics
    gamemap=gamemaps[curlevel-1]

    for i in range(64):
        if i<5:continue

        for j in range(64):
            if gamemap[i][j]=='E':
                pixel(i,j,*BG_COL)
            elif gamemap[i][j]=='W':
                pixel(i,j,*WALL_COL)
            elif gamemap[i][j]=='N':
                pixel(i,j,*NP_WALL_COL)
            elif gamemap[i][j]=='F':
                pixel(i,j,*FINISH_COL)
            elif gamemap[i][j]=='B':
                for y in range(3):
                    for x in range(3):
                        objbuf[i+y][j+x]=-1
            
            else:
                num=eval(gamemap[i][j])
                objloc[num]=(i,j)

                if num<4:
                    for y in range(4):
                        objbuf[i+y][j]=num

                elif num>=4:
                    for x in range(3):
                        objbuf[i][j+x]=num


    # go through the object buffer
    for i in range(64):
        for j in range(64):
            t=objbuf[i][j]
            if t==-2:continue

            if t==-1:
                pixel(i,j,*BOX_COL)
            elif t<4:
                pixel(i,j,*DOOR_COL)
            elif t>=4:
                pixel(i,j,*BTN_DE_COL)

    # make banner
    cur_score=64
    partial_frames=0

    for j in range(64):
        pixel(0,j,*NP_WALL_COL)
        
        for i in range(1,4):
            pixel(i,j,*SCORE_COL)
        
        pixel(4,j,*NP_WALL_COL)

def play_level():
    global keys_work,player_row,player_col,player_dir,where_portal,partial_frames,cur_score,restarted

    init_level()
    #print('level inited')
    levels_beat[curlevel]=0

    while True:


        #print(where_portal,where_portal_type)

        # keyboard
        pygame.event.get()
        keys=pygame.key.get_pressed()
        no_keys=sum(keys)==0
        if keys[ord('q')]:quit()
        if keys[ord('r')]:
            game_restart()
            restarted=True
            #print('setting restarted to true')
            return
        if keys[ord('m')]:init_level()

        #print('game loop')
        partial_frames+=1
        # draw new stuff
        draw_player(BG_COL)

        # make updates to the internal state
        check_wall_left()
        check_wall_right()
        check_portals()
        check_button()

        if keys_work:
            if keys[ord('o')]:
                # want to move left
                player_dir=0
                # do we have a portal to our left?
                if where_portal==0:
                    # portal to our left!
                    pass_through_portal()

                elif not wall_left:
                    player_col-=1


            elif keys[ord('u')]:
                # want to move right
                player_dir=1

                # do we have a portal to our right?
                if where_portal==1:
                    # portal to our right!
                    pass_through_portal()
                
                elif not wall_right:
                    player_col+=1
                
            elif keys[ord('.')]:
                player_dir=2
                
            
            # portal!
            if keys[ord('h')]:
                portal_shot(0)
            elif keys[ord('n')]:
                portal_shot(1)

            # button!
            if keys[ord('t')]:
                interact_button()

        if no_keys:
            keys_work=True

        check_on_floor()

        if player_row==60:return

        if not on_floor:
            player_row+=1


        # make updates to the graphics
        draw_player(PLAYER_COL)
        if levels_beat[curlevel]:break

        # update the score
        if partial_frames>=25:
            partial_frames=0
            if cur_score==0:return
            decrease_score()

        # are we fully on a button?
        if player_button!=0:
            if button_pixels==3:
                draw_door(BG_COL)
            elif not objstate[player_button-4]:
                draw_door(DOOR_COL)


        # display everything
        pygame.display.flip()
        clock.tick(15)
    
    levels_beat[curlevel]=1

clock=pygame.time.Clock()

# load in all of the screens
select_screen=open('./screens/select.txt','r').read().splitlines()
win_screen=open('./screens/win.txt','r').read().splitlines()
fail_screen=open('./screens/fail.txt','r').read().splitlines()
congrats_screen=open('./screens/congrats.txt','r').read().splitlines()

gamemaps=[
    open('./levels/map1.lvl','r').read().splitlines(),
    open('./levels/map2.lvl','r').read().splitlines(),
    open('./levels/map3.lvl','r').read().splitlines()
]

COL_0=(103,97,105)
COL_1=(0,162,255)
COL_2=(255,93,0)
COL_3=(32,17,171)
COL_4=(5,141,245)
COL_5=(255,255,255)
COL_6=(13,186,19)
COL_7=(191,15,15)

def draw_cursor(colour):
    col=18
    row=24+cursor_loc*11

    while col>14:
        up=row-(18-col+1)
        down=row+(18-col+1)

        for i in range(up,down+1):
            pixel(i,col,*colour)
        
        #print(col)
        
        col-=1

def game_restart():
    # restart the entire game
    global levels_beat,curlevel,curscreen,screendrawn,keys_work,cursor_loc,partial_frames
    global restarted
    restarted=False
    #print('setting restarted to false')

    # window state
    levels_beat=[0,0,0,0]

    curlevel=0
    curscreen=0
    screendrawn=0
    keys_work=False
    cursor_loc=0
    partial_frames=0

def get_next_level():
    for i in range(1,4):
        if levels_beat[i]==0:return i
    return 4

game_restart()

while True:
    if curscreen==-1:
        #print('lets play')
        play_level()
        if restarted:
            restarted=False
            continue

        screendrawn=0
        partial_frames=0

        # did we win
        if levels_beat[curlevel]:
            curscreen=1
        else:
            curscreen=2

        continue

    # do screen logic
    if not screendrawn:
        if curscreen==0:sc=select_screen
        if curscreen==1:sc=win_screen
        if curscreen==2:sc=fail_screen
        if curscreen==3:sc=congrats_screen

        for i in range(64):
            for j in range(64):
                char=sc[i][j]
                if char=='0':col=COL_0
                if char=='1':col=COL_1
                if char=='2':col=COL_2
                if char=='3':col=COL_3
                if char=='4':col=COL_4
                if char=='5':col=COL_5
                if char=='6':col=COL_6
                if char=='7':col=COL_7

                pixel(i,j,*col)
        
        screendrawn=1
    
    pygame.event.get()
    keys=pygame.key.get_pressed()

    # handle keys
    if keys[ord('q')]:quit()
    if keys[ord('r')]:game_restart()

    # updates
    if curscreen==0:
        draw_cursor(COL_0)
        no_keys=sum(keys)==0
        if keys_work:
            if keys[ord('.')]:
                # up
                cursor_loc-=1
                if cursor_loc<0:
                    cursor_loc=0
                keys_work=False

            elif keys[ord('e')]:
                # down
                cursor_loc+=1
                if cursor_loc>3:
                    cursor_loc=3
                keys_work=False

            elif keys[ord('u')]:
                # go right
                if cursor_loc==3:
                    quit()
                else:
                    curlevel=cursor_loc+1
                    curscreen=-1

                keys_work=False

        if no_keys:keys_work=True

        draw_cursor(BTN_AC_COL)
    
    # go to the next screen
    if curscreen==1:
        partial_frames+=1
        if partial_frames>=20:
            curscreen=-1

            # find next level
            curlevel=get_next_level()
            #print('switching to',curlevel)
            if curlevel==4:
                curscreen=3
                screendrawn=0
    
    if curscreen==2:
        partial_frames+=1
        if partial_frames>=20:
            curscreen=-1
    
    # updates
    pygame.display.flip()
    clock.tick(15)

pygame.quit()