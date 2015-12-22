from random import random, choice

class rsMARL:
    def __init__(self, filename):
        self.parse(filename)

        self.moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.goalReached = [False]*len(self.flags)
        '''

        self.canMove(0, 0)
        self.canMove(17, 12)

        self.canMove(5, 3)
        self.canMove(4, 3)
        self.canMove(4, 4)
        self.canMove(3, 4)

        self.canMove(5, 4)
        self.canMove(5, 5)'''
    
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

    def canMove(self, x, y):
        availablePoses = []
        availableMoves = []
        potentialPoses = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
        potentialMoves = range(4)
        for i in range(len(potentialPoses)):
            if potentialPoses[i][0] >= 0 and potentialPoses[i][1] >= 0 and potentialPoses[i][0] < self.size[0] and potentialPoses[i][1] < self.size[1]:
                if self.isInSameRoom([x, y], potentialPoses[i]):
                    availableMoves.append(potentialMoves[i])
                    availablePoses.append(potentialPoses[i])
                if self.hasDoor([x, y], potentialPoses[i]):
                    availableMoves.append(potentialMoves[i])
                    availablePoses.append(potentialPoses[i])
        return availablePoses, availableMoves

    def hasDoor(self, coord1, coord2):
        return (coord1+coord2) in self.doors or (coord2+coord1) in self.doors

    def isInSameRoom(self, coord1, coord2):
        return self.world[coord1[1]][coord1[0]] == self.world[coord2[1]][coord2[0]]


    def isDone(self):
        return self.agent1 == self.goal and self.agent2 == self.goal


    def run(self):
        self.Qas = [[0, 0, 0, 0] for i in range(self.size[0])] for j in range(self.size[1])]
        self.agent1 = self.start[0]
        self.agent2 = self.start[1]

        while not self.isDone() :
            action1 = self.chooseAction(self.agent1[0], self.agent1[1])
            nextPos1 = self.getNextPos(x, y, action1)
            reward1 = self.getReward(nextPos1)
            self.updateQ(reward1, nextPos1, self.agent1, action1)
            self.agent1 = nextPos1


    def probability(self, p):
        return random() < p

    def chooseAction(self, x, y):
        availablePoses, availableMoves = canMove(x, y)
        if probability(self.epsilon):
            return choice(availableMoves)
        else:
            maxValue, moves = computeMax(x, y, availableMoves)
            return choice(moves)

    def computeMax(self, pos):
        res = -9999999999999999999
        best = []
        for i in range(len(4)):
            current = self.Qas[pos[0]][pos[1]][i]
            if current > res:
                res = current
                best = [i]
            elif current == res:
                best.append(i)
        return res, best

    def getNextPos(self, x, y, move):
        return [pos[0] + self.moves[move][0], pos[1] + self.moves[move][1]]

    def getReward(self, nextPos):
        if nextPos == self.goal:
            return self.getFinalReward()
        else:
            return 0

    def getFinalReward(self):
        res = 0
        for value in self.goalReached:
            if value:
                res += 1
        return res*100
                
    def updateQ(self, reward, nextPos, currentPos, action):
        availablePoses, availableMoves = canMove(nextPos[0], nextPos[1])
        maxA, moves = computeMax(nextPos[0], nextPos[1], availableMoves)
        originalQ = self.Qas[currentPos[0]][currentPos[1]][action]
        self.Qas[currentPos[0]][currentPos[1]][action] =\
            originalQ + self.alpha*(reward + self.gamma*maxA-originalQ)






if __name__ == '__main__':
    marl = rsMARL("world.txt")
