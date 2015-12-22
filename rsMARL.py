class rsMARL:
    def __init__(self, filename):
        self.parse(filename)

        '''
        self.goalReached = [False]*len(self.flags)


        self.canMove(0, 0)
        self.canMove(17, 12)

        self.canMove(5, 3)
        self.canMove(4, 3)
        self.canMove(4, 4)
        self.canMove(3, 4)

        self.canMove(5, 4)
        self.canMove(5, 5)'''

    def canMove(self, x, y):
        availableMoves = []
        move = [-1, 1]
        for shift in move:
            for shiftType in [0, 1]:

                if shiftType == 0: # shift on y
                    tmp = [x, y+shift]
                else: # shift on x
                    tmp = [x+shift, y]

                if (0 <= tmp[0] and tmp[0] < self.size[0]) and (0 <= tmp[1] and tmp[1] < self.size[1]): #Is in World
                    if self.isInSameRoom([x, y], tmp):
                        availableMoves.append(tmp)
                    elif self.hasDoor([x, y], tmp):
                        availableMoves.append(tmp)

        print(x, y, availableMoves)
        return availableMoves

    def hasDoor(self, coord1, coord2):
        return (coord1+coord2) in self.doors or (coord2+coord1) in self.doors

    def isInSameRoom(self, coord1, coord2):
        return self.world[coord1[1]][coord1[0]] == self.world[coord2[1]][coord2[0]]
    
    def parse(self, filename):
        file = open(filename)
        content = file.readlines()
        self.size = list(map(int, content[0].strip().replace("\n", "").split(" ")))
        del content[0]
        #print(self.size)

        tmp = content[0].strip().strip("\n").split(", ")
        for i in range(len(tmp)):
            tmp[i] = tmp[i].split(" ")
        self.goal = list(map(int, tmp[0]))
        self.start = tmp[1:]
        for i in range(len(self.start)):
            self.start[i] = list(map(int, self.start[i]))
        self.nbAgent = len(self.start)
        #print(self.start)
        del content[0]
        #print(self.goal)

        # Doors
        tmp = content[0].strip().replace("\n", "").split(", ")

        self.doors = [[0, 0, 0, 0] for i in range(len(tmp))]
        for i in range(len(tmp)):
            self.doors[i] = list(map(int, tmp[i].split(" "))) #Convert list str into list int
        del content[0]
        #print(self.doors)

        # Flags
        tmp = content[0].strip().replace("\n", "").split(", ")
        self.flags = [[0, 0] for i in range(len(tmp))]
        for i in range(len(tmp)):
            self.flags[i] = list(map(int, tmp[i].split(" "))) #Convert list str into list int
        del content[0]
        #print(self.flags)

        self.world = [[0 for i in range(int(self.size[0]))] for j in range(int(self.size[1]))]
        for y in range(int(self.size[1])):
            content[y] = content[y].replace("\n", "")
            for x in range(int(self.size[0])):
                self.world[y][x] = content[y][x]
        #print(self.world)
        del content[:13]
        print(content)
        
        size = int(content[0].strip("\n"))
        del content[0]
        self.flagsNames = []
        for i in range(size):
            self.flagsNames.append(content[0].strip("\n"))
            del content[0]
            
        size = int(content[0].strip("\n"))
        del content[0]
        self.roomsNames = []
        for i in range(size):
            self.roomsNames.append(content[0].strip("\n"))
            del content[0]
        print(self.flagsNames, self.roomsNames)
            
        size = int(content[0].strip("\n"))
        del content[0]
        self.plan1Join = []
        for i in range(size):
            self.plan1Join.append(content[0].strip("\n").split(" "))
            del content[0]
            
        size = int(content[0].strip("\n"))
        del content[0]
        self.plan2Join = []
        for i in range(size):
            self.plan2Join.append(content[0].strip("\n").split(" "))
            del content[0]
            
        size = int(content[0].strip("\n"))
        del content[0]
        self.plan1Solo = []
        for i in range(size):
            self.plan1Solo.append(content[0].strip("\n").split(" "))
            del content[0]
            
        size = int(content[0].strip("\n"))
        del content[0]
        self.plan2Solo = []
        for i in range(size):
            self.plan2Solo.append(content[0].strip("\n").split(" "))
            del content[0]
            
        self.plan1Join = self.handlePlan(self.plan1Join)
        self.plan2Join = self.handlePlan(self.plan2Join)
        self.plan1Solo = self.handlePlan(self.plan1Solo)
        self.plan2Solo = self.handlePlan(self.plan2Solo)

    def handlePlan(self, plan):
        for i in range(len(plan)):
            flags = []
            room = plan[i][0]
            room = self.roomsNames.index(room)
            if len(plan[i]) > 1:
                flags = plan[i][1:]
                for j in range(len(flags)):
                    flags[j] = self.flagsNames.index(flags[j])
            plan[i] = [room] + flags
        return plan


if __name__ == '__main__':
    marl = rsMARL("world")
