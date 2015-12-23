from random import random, choice

shapeDic = {"None":0, "Flag":1, "Solo":2, "Join":3, "Flag+Solo":4, "Flag+Join":5}

class rsMARL:
    def __init__(self, filename, epsilon, gamma, alpha, shape, lambd):
        self.parse(filename)

        self.shape=shape
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.lambd = lambd

        self.moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.totalReward = 0
        
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
            eTrace1 = [[[0, 0, 0, 0] for i in range(self.size[1])] for j in range(self.size[0])]
            eTrace2 = [[[0, 0, 0, 0] for i in range(self.size[1])] for j in range(self.size[0])]
            sigma1 = None
            sigma2 = None
            while not self.isDone() :
                step += 1
                if self.agent1 != self.goal:
                    self.agent1, Qas1, eTrace1 = self.runAgent(self.agent1, Qas1, eTrace1)

                if self.agent2 != self.goal:
                    self.agent2, Qas2, eTrace2 = self.runAgent(self.agent2, Qas2, eTrace2)

                if step%100 == 0:
                    print(step, self.agent1!= self.goal, self.agent2 != self.goal)
            self.totalReward += self.getFinalReward()
            print (run, step, self.goalReached.count(True), int(self.totalReward/(run+1)))

    def runAgent(self, pos, Qas, eTrace):
        action = self.chooseAction(pos[0], pos[1], Qas)
        nextPos = self.getNextPos(pos[0], pos[1], action)
        reward = self.getReward(nextPos)

        sigma = self.updateSigma(reward, nextPos, pos, action, Qas)
        eTrace[pos[0]][pos[1]][action] += 1
        eTrace, Qas = self.updateEligibilityTrace(eTrace, sigma, Qas)

        self.checkFlags(nextPos)

        return nextPos, Qas, eTrace


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

    def getReward(self, pos):
        if pos == self.goal:
            return self.getFinalReward()
        else:
            return 0

    def getFinalReward(self):
        return 100*self.goalReached.count(True)

    def updateEligibilityTrace(self, eTrace, sigma, Qas):
        for x in range(len(Qas)):
            for y in range(len(Qas[x])):
                for a in range(len(Qas[x][y])):
                    Qas[x][y][a] += self.alpha*sigma*eTrace[x][y][a]
                    eTrace[x][y][a] *= self.gamma * self.lambd
        return eTrace, Qas
        
                
    def updateSigma(self, reward, nextPos, currentPos, action, Qas):
        availablePoses, availableMoves = self.canMove(nextPos[0], nextPos[1])
        maxA, moves = self.computeMax(nextPos[0], nextPos[1], availableMoves, Qas)
        originalQ = Qas[currentPos[0]][currentPos[1]][action]
        sigma = \
            reward + self.gamma*maxA-originalQ + self.rewardShaping(currentPos, nextPos)

        return sigma


    def checkFlags(self, pos):
        if pos in self.flags:
            self.goalReached[self.flags.index(pos)] = True


    def testFlags(self, pos):
        tmp = list(self.goalReached)
        if pos in self.flags:
            tmp[self.flags.index(pos)] = True
        return tmp.count(True)

    def rewardShaping(self, currentPos, nextPos):
        return self.gamma*self.phi(nextPos)-self.phi(currentPos)

    def phi(self, pos):
        if self.shape == "None":
            return 0
        elif self.shape == "Flags":
            #omega = len(self.flags)*100.0/len(self.flags)
            omega = 100
            return omega*self.testFlags(pos)
        #elif self.shape = "Solo":
            
            
            



if __name__ == '__main__':
    epsilon = 0.1
    gamma = 0.99
    alpha = 0.1
    lambd = 0.4
    marl = rsMARL("world.txt", epsilon, gamma, alpha, "None", lambd)
    marl.run()
