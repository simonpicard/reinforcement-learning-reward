import Tkinter as tkinter
from Tkinter import *
from random import randint


class game(Tk):

    def __init__(self, world, openDoors, flags):
        Tk.__init__(self)
        self.world = world
        self.openDoors = openDoors
        self.flags = flags

        self.height = len(self.world)
        self.width = len(self.world[0])
        
        self.gridSize = 30
        self.pad = 20
        self.canvas = Canvas(self, width = self.width*self.gridSize+self.pad, height = self.height*self.gridSize+self.pad, bg = 'white')
        self.canvas.pack(padx = 5, pady = 5)

        self.drawWorld()

    def drawWorld(self):
        #Draw Grid
        for i in range(self.width+1):
             self.drawVerticalLine(0, self.height, i, 1)
        for i in range(self.height+1):
             self.drawHoriZontalLine(0, self.width, i, 1)

        #Draw Walls
        for i in range(self.height-1):
            for j in range(self.width-1):
                if self.world[i][j] != self.world[i+1][j]:
                    if (i, j, i+1, j) not in self.openDoors:
                        self.drawHoriZontalLine(j, j+1, i+1, 5)
                if self.world[i][j] != self.world[i][j+1]:
                    if (i, j, i, j+1) not in self.openDoors:
                        self.drawVerticalLine(i, i+1, j+1, 5)
            if self.world[i][self.width-1] != self.world[i+1][self.width-1]:
                    self.drawHoriZontalLine(self.width-1, self.width, i+1, 5)
        if self.world[self.height-1][self.width-2] != self.world[self.height-1][self.width-1]:
            if (i, self.width-2, i, self.width-1) not in self.openDoors:
                self.drawVerticalLine(self.height-1, self.height, self.width-1, 5)

        # for door in self.openDoors:
        #     x, y, x2, y2 = door[0], door[1], door[2], door[3]
        #     if x == x2:
        #         self.drawHoriZontalLine(x+0.03, x+1, max(y, y2), 5, 'white')
        #     else:
        #         self.drawVerticalLine(min(y, y2)+0.03, max(y, y2)+1, max(x, x2), 5, 'white')

        for flag in self.flags:
            self.drawFlag(flag[0], flag[1])

                
    def drawHoriZontalLine(self, x1, x2, y, lineWidth, color = 'black'):
        self.canvas.create_line(x1*self.gridSize+self.pad/2, y*self.gridSize+self.pad/2, x2*self.gridSize+self.pad/2, y*self.gridSize+self.pad/2, width = lineWidth, fill = color)

    def drawVerticalLine(self, y1, y2, x, lineWidth, color = 'black'):
        self.canvas.create_line(x*self.gridSize+self.pad/2, y1*self.gridSize+self.pad/2, x*self.gridSize+self.pad/2, y2*self.gridSize+self.pad/2, width = lineWidth, fill = color)


    def drawFlag(self,x,y):
        self.canvas.create_line(self.pad/2+y*self.gridSize+15,self.pad/2+x*self.gridSize+5,self.pad/2+y*self.gridSize+15,self.pad/2+x*self.gridSize+25,fill="black",width = 3)
        self.canvas.create_line(self.pad/2+y*self.gridSize+5,self.pad/2+x*self.gridSize+12,self.pad/2+y*self.gridSize+15,self.pad/2+x*self.gridSize+5,fill="black",width = 3)
        self.canvas.create_line(self.pad/2+y*self.gridSize+9,self.pad/2+x*self.gridSize+15,self.pad/2+y*self.gridSize+15,self.pad/2+x*self.gridSize+7,fill="black",width = 5)
        self.canvas.create_line(self.pad/2+y*self.gridSize+13,self.pad/2+x*self.gridSize+18,self.pad/2+y*self.gridSize+14,self.pad/2+x*self.gridSize+9,fill="black",width = 5)
        self.canvas.create_line(self.pad/2+y*self.gridSize+5,self.pad/2+x*self.gridSize+12,self.pad/2+y*self.gridSize+15,self.pad/2+x*self.gridSize+17,fill="black",width = 3)
        self.canvas.create_line(self.pad/2+y*self.gridSize+7,self.pad/2+x*self.gridSize+25,self.pad/2+y*self.gridSize+23,self.pad/2+x*self.gridSize+25,fill="black",width = 3)


world = [[1,1,3,3],
         [1,1,3,3],
         [3,3,3,3],
         [3,3,2,2],
         [3,3,3,3],
         [3,3,3,4]]
flags = [(2,3), (4, 0)]
openDoors = [(1, 1, 1, 2), (5, 3, 5, 2)]
root = game(world, openDoors, flags)
root.title('Reward Shaping')
root.mainloop()
