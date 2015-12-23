import tkinter
from tkinter import *
from random import randint


class game(Tk):

    def __init__(self, world, openDoors):
        Tk.__init__(self)
        self.world = world
        self.openDoors = openDoors

        self.height = len(self.world)
        self.width = len(self.world[0])
        
        self.gridSize = 30
        self.canvas = Canvas(self, width = self.width*self.gridSize, height = self.height*self.gridSize, bg = 'white')
        self.canvas.pack(padx = 5, pady = 5)

        self.drawWorld()

    def drawWorld(self):
        for i in range(self.width+1):
             self.canvas.create_line(i*self.gridSize, 0, i*self.gridSize, self.height*self.gridSize, width = 1)
        for i in range(self.height+1):
             self.canvas.create_line(0, i*self.gridSize, self.width*self.gridSize, i*self.gridSize, width = 1)

        for door in openDoors:
            x = door[0]
            y = door[1]
            self.canvas.create_rectangle(y*self.gridSize,x*self.gridSize,y*self.gridSize+self.gridSize,x*self.gridSize+self.gridSize, fill='white')
                    

    def drawFlag(self,x,y):
        self.canvas.create_line(y*self.gridSize+15,x*self.gridSize+5,y*self.gridSize+15,x*self.gridSize+25,fill="black",width = 3)
        self.canvas.create_line(y*self.gridSize+5,x*self.gridSize+12,y*self.gridSize+15,x*self.gridSize+5,fill="black",width = 3)
        self.canvas.create_line(y*self.gridSize+9,x*self.gridSize+15,y*self.gridSize+15,x*self.gridSize+7,fill="black",width = 5)
        self.canvas.create_line(y*self.gridSize+13,x*self.gridSize+18,y*self.gridSize+14,x*self.gridSize+9,fill="black",width = 5)
        self.canvas.create_line(y*self.gridSize+5,x*self.gridSize+12,y*self.gridSize+15,x*self.gridSize+17,fill="black",width = 3)
        self.canvas.create_line(y*self.gridSize+7,x*self.gridSize+25,y*self.gridSize+23,x*self.gridSize+25,fill="black",width = 3)


world = [[1,1,1,1],[3,3,3,3],[3,3,3,3],[3,3,3,3],[3,3,3,3],[3,3,3,3]]
openDoors = [(1, 3), (1, 4)]
root = game(world, openDoors)
root.title('Reward Shaping')
root.mainloop()
