import pygame
import time
pygame.font.init()

# to check whether the grid has any empty locations or not?
def empty(arr):
    for i in range(9):
        for j in range(9):
            if(arr[i][j]==0):
                return (i,j)
    return None

# to check whether the number is used in that row
def used_row(arr,row,col,num):
    for i in range(9):
        if(arr[row][i]==num and i!=col):#here i!=col is written so that the scribbed text is not compared
            return True
            return True
    return False

# to check whether the number is used in that col
def used_col(arr,row,col,num):
    for i in range(9):
        if(arr[i][col]==num and i!=row):# here i!=row is written so that the scribbed text is not compared
            return True
    return False

# to check whether the number is used in that box
def used_box(arr,row,col,num,pr,pc):
    for i in range(3):
        for j in range(3):
            if(arr[row+i][col+j]==num and row+i!=pr and col+j!=pc):
                return True
    return False

# to check whether a number at the location is safe or not? 
def check_is_safe(arr,row,col,num):
    return not used_row(arr,row,col,num) and not used_col(arr,row,col,num) and not used_box(arr,row-(row%3),col-(col%3),num,row,col)

class Cube:
    #constructor
    def __init__(self,val,i,j,width,height):
        self.value=val
        self.rows=i
        self.cols=j
        self.width=width
        self.height=height
        self.temp=0
        self.selected=False
        
    #draws the number on the screen at given location
    def draw(self,screen):
        fnt=pygame.font.SysFont("comicsans", 40)
        gap=self.width/9 
        if self.temp!=0 and self.value == 0:#if the temp is not 0 and value is zero which means that we have scribbed somehing so we use grey color to display it
            text=fnt.render(str(self.temp),1,(128,128,128))
            screen.blit(text,((self.cols*gap)+5,(self.rows*gap)+5))
        if self.value != 0: # the value is not zero which means at given oacion the value has found/given so we use black color to write
            text=fnt.render(str(self.value),True,(0,0,0))
            screen.blit(text,(25+self.cols*gap,20+self.rows*gap))
        if self.selected:# the given location is selected so we color it with red(ony borders)
            pygame.draw.rect(screen, (255,0,0), (self.cols*gap,self.rows*gap,gap,gap),4)
            
    # to change the border color from green to red and vice-versa
    def draw_change(self,screen,greencol):
        gap=self.width/9
        pygame.draw.rect(screen, (255,255,255), (self.cols*gap,self.rows*gap,gap,gap))
        text=fnt.render(str(self.value), 1, (0,0,0))
        screen.blit(text,(25+self.cols*gap,20+self.rows*gap))
        if greencol:
            pygame.draw.rect(screen, (0,255,0), (self.cols*gap,self.rows*gap,gap,gap),4)
        else:
            pygame.draw.rect(screen, (255,0,0), (self.cols*gap,self.rows*gap,gap,gap),4)

class Grid:
    grid=[
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    #constructor
    def __init__(self,rows,cols,width,height,screen):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen=screen
        self.gap=self.width/9
        self.model = None
        self.cubes=[[Cube(self.grid[i][j],i,j,width,height) for j in range(cols)]for i in range(rows)]
        self.selected=None
        self.update_model()
        self.drawGridLines()
             
    #copying the cubes arr to model arr
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    #to draw the gridlines on the screen
    def drawGridLines(self):
        self.screen.fill((255,255,255))
        for i in range(self.rows+1):
            if i%3 == 0 and i!=0:
                thick=4
            else:
                thick=1
            pygame.draw.line(self.screen, (0,0,0),(0,i*self.gap),(self.width,i*self.gap),thick)
            pygame.draw.line(self.screen,(0,0,0),(i*self.gap,0),(i*self.gap,self.width),thick)
        # for writting the values on to the screen
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.screen)
    
    #to check whether the grid is finished or not?
    def finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.cubes[i][j].value==0):
                    return False
        return True
    
    #solves the grid using backtracking
    def solve(self):
        find = empty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if check_is_safe(self.model,row, col,i):
                self.model[row][col] = i
                if self.solve():
                    return True
                self.model[row][col] = 0
        return False
    
    # to check whether the number can be placed at the given location 
    def correct_place(self,val):
        r,c=self.selected[0],self.selected[1]
        if self.cubes[r][c].value==0:
            self.cubes[r][c].value=val
            self.update_model()
            if check_is_safe(self.model, r,c,val) and self.solve():
                return True
            else:
                self.cubes[r][c].value=0
                self.cubes[r][c].temp=0
                self.update_model()
                return False
            
    # assigning the temp of cubes to value
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].temp=val
        
    # to select the given row and col
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected=False
        self.cubes[row][col].selected=True
        self.selected=(row,col)
    
    #to clear the value
    def clear(self):
        row,col=self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].temp=0
            
    # solves the grid using backtracking
    def solve_gui(self):
        self.update_model()
        find = empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if check_is_safe(self.model,row, col,i):
                self.model[row][col] = i
                self.cubes[row][col].value=i
                self.cubes[row][col].draw_change(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                
                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].value=0
                self.update_model()
                self.cubes[row][col].draw_change(self.screen, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
    
# formatting the time 
def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60
    mat = str(hour)+":" + str(minute) + ":" + str(sec)
    return mat
    
#to redraw the window 
def redraw_win(screen,board,time,wrong):
    screen.fill((255,255,255))
    board.drawGridLines()
    text=fnt.render("Time:"+format_time(time),1,(0,0,0))
    screen.blit(text, (360,560))
    text=fnt.render("X "*wrong,1,(255,0,0))
    screen.blit(text, (0,560))
    
# main()
screen=pygame.display.set_mode((540,600))
pygame.display.set_caption("SUDOKO")
done=True
done2=True
board=Grid(9, 9, 540, 600, screen)
#fonts
fnt=pygame.font.SysFont("comicsans", 40)
game=pygame.font.SysFont("cosmicsans", 130)
x,y=(0,0)
pos=(0,0)
key=0
gap=540/9
wrong=0 
start=time.time()

#loop
while done:
    play_time=round(time.time()-start)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            done=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                key=1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                key=2
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                key=3
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                key=4
            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                key=5
            elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                key=6
            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                key=7
            elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                key=8
            elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                key=9
            elif event.key == pygame.K_SPACE:
                #if the given board has solution 
                if board.solve_gui():
                    pygame.time.delay(2000)
                    screen2=pygame.display.set_mode((540,600))
                    pygame.display.set_caption("RESULT")
                    text=game.render(str("GAME OVER"),True,(255,0,0))
                    screen2.blit(text,(0,230))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                #the given board has no solution
                else:
                    screen2=pygame.display.set_mode((540,600))
                    pygame.display.set_caption("RESULT")
                    text=game.render(str("NO"),True,(255,0,0))
                    screen2.blit(text,(200,160))
                    text=game.render(str("SOLUTION"),True,(255,0,0))
                    screen2.blit(text,(40,250))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                done=False
                pygame.quit()
                done2=False
                break
            elif board.finished():
                text=game.render(str("GAME OVER"),True,(255,0,0))
                screen.blit(text,(0,230))
            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                board.clear()
                key=None
            elif event.key == pygame.K_RETURN:
                i,j=board.selected[0],board.selected[1]
                if board.cubes[i][j].temp!=0 :
                    if board.correct_place(board.cubes[i][j].temp):
                        print("Sucess")
                    else:
                        wrong=wrong+1
                        print("Wrong")
                    key=None
                    if board.finished():
                        text=game.render(str("GAME OVER"),True,(255,0,0))
                        screen.blit(text,(0,230))
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            x,y=(pos[0],pos[1])
            if(540>x and 540>y):
                board.select(int(pos[1]//gap), int(pos[0]//gap))
                key=None
    
    if(done2):
        if board.selected and key!=None:
            board.cubes[board.selected[0]][board.selected[1]].temp=key
        redraw_win(screen,board,play_time,wrong) 
        pygame.display.update()
pygame.quit() # to quit