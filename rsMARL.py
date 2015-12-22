from random import random, choice

class rsMARL:
    def __init__(self, filename, epsilon, gamma, alpha):
        self.parse(filename)

        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha

        self.moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
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
        #print(content)
        
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
        #print(self.flagsNames, self.roomsNames)
            
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
                elif self.hasDoor([x, y], potentialPoses[i]):
                    availableMoves.append(potentialMoves[i])
                    availablePoses.append(potentialPoses[i])

        if self.agent1 in availablePoses and self.agent1!=self.goal:
            availableMoves.pop(availablePoses.index(self.agent1))
            availablePoses.remove(self.agent1)
        if self.agent2 in availablePoses and self.agent2!=self.goal:
            availableMoves.pop(availablePoses.index(self.agent2))
            availablePoses.remove(self.agent2)
        return availablePoses, availableMoves

    def hasDoor(self, coord1, coord2):
        return (coord1+coord2) in self.doors or (coord2+coord1) in self.doors

    def isInSameRoom(self, coord1, coord2):
        return self.world[coord1[1]][coord1[0]] == self.world[coord2[1]][coord2[0]]


    def isDone(self):
        return self.agent1 == self.goal and self.agent2 == self.goal


    def reset(self):
        self.agent1 = self.start[0]
        self.agent2 = self.start[1]
        self.goalReached = [False]*len(self.flags)

    def run(self):
        Qas1 = [[[0, 0, 0, 0] for i in range(self.size[1])] for j in range(self.size[0])]
        Qas2 = [[[0, 0, 0, 0] for i in range(self.size[1])] for j in range(self.size[0])]

        for run in range(1000):
            self.reset()
            step = 0
            while not self.isDone() :
                step += 1
                if self.agent1 != self.goal:
                    action1 = self.chooseAction(self.agent1[0], self.agent1[1], Qas1)
                    nextPos1 = self.getNextPos(self.agent1[0], self.agent1[1], action1)
                    reward1 = self.getReward(nextPos1)
                    Qas1 = self.updateQ(reward1, nextPos1, self.agent1, action1, Qas1)
                    self.agent1 = nextPos1
                    self.checkFlags(self.agent1)

                if self.agent2 != self.goal:
                    action2 = self.chooseAction(self.agent2[0], self.agent2[1], Qas2)
                    nextPos2 = self.getNextPos(self.agent2[0], self.agent2[1], action2)
                    reward2 = self.getReward(nextPos2)
                    Qas2 = self.updateQ(reward2, nextPos2, self.agent2, action2, Qas2)
                    self.agent2 = nextPos2
                    self.checkFlags(self.agent2)
            print (step, self.goalReached.count(True))


    def probability(self, p):
        return random() < p

    def chooseAction(self, x, y, Qas):
        availablePoses, availableMoves = self.canMove(x, y)
        if self.probability(self.epsilon):
            return choice(availableMoves)
        else:
            maxValue, moves = self.computeMax(x, y, availableMoves, Qas)
            return choice(moves)

    def computeMax(self, x, y, pos, Qas):
        res = -9999999999999999999
        best = []
        for i in range(len(pos)):
            current = Qas[x][y][pos[i]]
            if current > res:
                res = current
                best = [pos[i]]
            elif current == res:
                best.append(pos[i])
        return res, best

    def getNextPos(self, x, y, move):
        return [x + self.moves[move][0], y + self.moves[move][1]]

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
                
    def updateQ(self, reward, nextPos, currentPos, action, Qas):
        availablePoses, availableMoves = self.canMove(nextPos[0], nextPos[1])
        maxA, moves = self.computeMax(nextPos[0], nextPos[1], availableMoves, Qas)
        originalQ = Qas[currentPos[0]][currentPos[1]][action]
        Qas[currentPos[0]][currentPos[1]][action] =\
            originalQ + self.alpha*(reward + self.gamma*maxA-originalQ)

        return Qas


    def checkFlags(self, pos):
        if pos in self.flags:
            self.goalReached[self.flags.index(pos)] = True            



if __name__ == '__main__':
    epsilon = 0.1
    gamma = 1
    alpha = 0.5
    marl = rsMARL("world.txt", epsilon, gamma, alpha)
    marl.run()
