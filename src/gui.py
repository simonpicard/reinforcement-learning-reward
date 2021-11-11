import Tkinter as tkinter
from Tkinter import *
from random import randint
from worldParser import parse


class game(Tk):

    def __init__(self, world, openDoors, flags, start1, start2, goal):
        Tk.__init__(self)
        self.world = world
        self.openDoors = openDoors
        self.flags = flags
        self.start1 = start1
        self.start2 = start2
        self.goal = goal

        self.height = len(self.world)
        self.width = len(self.world[0])
        
        self.gridSize = 30
        self.pad = 20
        self.canvas = Canvas(self, width = self.width*self.gridSize+self.pad, height = self.height*self.gridSize+self.pad, bg = 'white')
        self.canvas.pack(padx = 5, pady = 5)

        self.drawWorld()

        """DRAW PATH"""
        self.drawPath([[0,0], [0, 1] , [1, 1], [2,1], [3,1], [3,2], [3,3]], "blue")


    def drawPath(self, path, color):
        for pos in path:
            self.colorMiniSquare(pos[0], pos[1], color)


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
                    if [j, i, j, i+1] not in self.openDoors:
                        self.drawHoriZontalLine(j, j+1, i+1, 5)
                if self.world[i][j] != self.world[i][j+1]:
                    if [j, i, j+1, i] not in self.openDoors:
                        self.drawVerticalLine(i, i+1, j+1, 5)
            if self.world[i][self.width-1] != self.world[i+1][self.width-1]:
                    self.drawHoriZontalLine(self.width-1, self.width, i+1, 5)
        for j in range(self.width-1):
            if self.world[self.height-1][j] != self.world[self.height-1][j+1]:
                if [i, j, i+1, j] not in self.openDoors:
                    self.drawVerticalLine(self.height-1, self.height, j+1, 5)

        #flags
        for flag in self.flags:
            self.drawFlag(flag[1], flag[0])

        #starts et goals
        self.colorSquare(self.goal[0], self.goal[1], 'red')
        self.colorSquare(self.start1[0], self.start1[1], 'magenta')
        self.colorSquare(self.start2[0], self.start2[1], 'green')
        self.canvas.create_text(self.goal[0]*self.gridSize+self.pad+5, self.goal[1]*self.gridSize+self.pad+5,  text="G", font="Arial 16")

    def colorSquare(self, x, y, color):
        self.canvas.create_rectangle(x*self.gridSize+self.pad/2,y*self.gridSize+self.pad/2,x*self.gridSize+self.pad/2+self.gridSize,y*self.gridSize+self.pad/2+self.gridSize, fill=color)

    def colorMiniSquare(self, x, y, color):
        self.canvas.create_rectangle(x*self.gridSize+self.pad/2+10,y*self.gridSize+self.pad/2+10,x*self.gridSize+self.pad/2+self.gridSize-10,y*self.gridSize+self.pad/2+self.gridSize-10, fill=color)


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


# world = [[1,1,3,3],
#          [1,1,3,3],
#          [3,3,3,3],
#          [3,3,2,2],
#          [3,3,3,3],
#          [3,2,3,4]]
# flags = [(2,3), (4, 0)]
# openDoors = [(1, 1, 1, 2), (5, 3, 5, 2)]

"""
size = width, height
start = x, y
goal = x, y
doors = x, y
flags = x, y
world[y][x]
agents = x, y
Qas[y][x]
eTrace[y][x]
"""

size, goal, start, openDoors, flags, world, flagsNames, roomsNames, plan1Join, plan2Join, plan1Solo, plan2Solo = parse("world.txt")
root = game(world, openDoors, flags, start[0], start[1], goal)
root.title('Reward Shaping')
root.mainloop()
