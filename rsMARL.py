from random import random, choice
import copy

shapeDic = {"None":0, "Flag":1, "Solo":2, "Join":3, "Flag+Solo":4, "Flag+Join":5}

class rsMARL:
    def __init__(self, filename, epsilon, gamma, alpha, shape, lambd):
        self.parse(filename)

        self.shape=shape
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.lambd = lambd

        self.moves = [[0, -1], [1, 0], [0, 1], [-1, 0]] #x y N E S O
        self.totalReward = 0

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

        self.doors = [[] for i in range(len(tmp))]
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
                self.world[y][x] = int(content[y][x])
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

    def canMove(self, x, y, agent):
        availablePoses = []
        availableMoves = []
        potentialPoses = [[x+self.moves[i][0], y+self.moves[i][1]] for i in range(4)]
        potentialMoves = range(4)

        for i in range(len(potentialPoses)):
            if potentialPoses[i][0] >= 0 and potentialPoses[i][1] >= 0 and potentialPoses[i][0] < self.size[0] and potentialPoses[i][1] < self.size[1]:

                if self.isInSameRoom([x, y], potentialPoses[i]):
                    availableMoves.append(potentialMoves[i])
                    availablePoses.append(potentialPoses[i])

                elif self.hasDoor([x, y], potentialPoses[i]):
                    availableMoves.append(potentialMoves[i])
                    availablePoses.append(potentialPoses[i])

        """
        if agent == 2 and self.agent1 in availablePoses and self.agent1!=self.goal:
            availableMoves.pop(availablePoses.index(self.agent1))
            availablePoses.pop(availablePoses.index(self.agent1))
        elif agent == 1 and self.agent2 in availablePoses and self.agent2!=self.goal:
            availableMoves.pop(availablePoses.index(self.agent2))
            availablePoses.pop(availablePoses.index(self.agent2))
        """

        return availableMoves

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
        self.goalReached1 = [False]*len(self.flags)
        self.goalReached2 = [False]*len(self.flags)
        self.flagsGot1 = []
        self.flagsGot2 = []
        self.lastStep1 = 0
        self.lastStep2 = 0

    def run(self):
        Qas1 = [[[0, 0, 0, 0] for i in range(self.size[0])] for j in range(self.size[1])]
        Qas2 = [[[0, 0, 0, 0] for i in range(self.size[0])] for j in range(self.size[1])]
        z = False
        

        for run in range(1000):
            self.reset()
            step = 0
            eTrace1 = [[[0, 0, 0, 0] for i in range(self.size[0])] for j in range(self.size[1])]
            eTrace2 = [[[0, 0, 0, 0] for i in range(self.size[0])] for j in range(self.size[1])]
            sigma1 = None
            sigma2 = None
            action1 = choice(self.canMove(self.agent1[0], self.agent1[1], 1))
            action2 = choice(self.canMove(self.agent2[0], self.agent2[1], 2))
            while not self.isDone() :
                step += 1

                if self.agent1 != self.goal:
                    self.agent1, Qas1, eTrace1, action1, p1 = self.runAgent(self.agent1, Qas1, eTrace1, action1, 1)

                if self.agent2 != self.goal:
                    self.agent2, Qas2, eTrace2, action2, p2 = self.runAgent(self.agent2, Qas2, eTrace2, action2, 2)

                if step%100 == 0:
                    if self.shape == "Solo" or self.shape == "Join":
                        print(step, self.agent1!= self.goal, self.agent2 != self.goal, self.getStepPlan(1, self.agent1, self.shape), self.getStepPlan(2, self.agent2, self.shape))
                    else:
                        print(step, self.agent1!= self.goal, self.agent2 != self.goal)
                #print (self.agent2)
                if step > 10000 and not z:
                    a = input("What to do")
                    if a == "e":
                        z = True
                        pass
                    else:
                        print("ok")
                        if self.agent1 != self.goal:
                            print(self.agent1, self.canMove(self.agent1[0], self.agent1[1], 1), Qas1[self.agent1[1]][self.agent1[0]], action1, p1, self.testFlags([0,0],1))
                            for i in range(len(Qas1)):
                                for j in range(len(Qas1[i])):
                                    print(list(map(int, Qas1[i][j])), end= " ")
                                print("")
                        if self.agent2 != self.goal:
                            print(self.agent2, self.canMove(self.agent2[0], self.agent2[1], 2), Qas2[self.agent2[1]][self.agent2[0]], action2, p2, self.testFlags([0,0],2))
                            for i in range(len(Qas2)):
                                for j in range(len(Qas2[i])):
                                    print(list(map(int, Qas2[i][j])), end= " ")
                                print("")

            self.totalReward += self.getFinalReward()
            print (run, step, self.goalReached.count(True), int(self.totalReward/(run+1)))

    def runAgent(self, pos, Qas, eTrace, action, agent):
        #action = self.chooseAction(pos[0], pos[1], Qas)
        nextPos = self.getNextPos(pos[0], pos[1], action)
        reward = self.getReward(nextPos)

        sigma, nextAction, p = self.getSigma(reward, nextPos, pos, action, Qas, agent)
        eTrace[pos[1]][pos[0]][action] = 1
        eTrace, Qas = self.updateEligibilityTrace(eTrace, sigma, Qas)

        self.checkFlags(nextPos, agent)
        return nextPos, Qas, eTrace, nextAction, p


    def probability(self, p):
        return random() < p

    def chooseAction(self, x, y, Qas, agent):
        availableMoves = self.canMove(x, y, agent)
        if self.probability(self.epsilon):
            return choice(availableMoves), "random"
        else:
            maxValue, moves = self.computeMax(x, y, availableMoves, Qas)
            return choice(moves), "greedy"

    def computeMax(self, x, y, pos, Qas):
        res = -9999999999999999999
        best = []
        for i in range(len(pos)):
            current = Qas[y][x][pos[i]]
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
        for y in range(len(Qas)):
            for x in range(len(Qas[y])):
                for a in range(len(Qas[y][x])):
                    Qas[y][x][a] += self.alpha * sigma * eTrace[y][x][a]
                    eTrace[y][x][a] *= self.gamma * self.lambd
        return eTrace, Qas
        
                
    def getSigma(self, reward, nextPos, currentPos, action, Qas, agent):
        nextAction, p = self.chooseAction(nextPos[0], nextPos[1], Qas, agent)
        originalQ = Qas[currentPos[1]][currentPos[0]][action]
        nextQ = Qas[nextPos[1]][nextPos[0]][nextAction]
        sigma = \
            reward + (self.gamma*nextQ) - originalQ + self.rewardShaping(currentPos, nextPos, agent)

        return sigma, nextAction, p


    def checkFlags(self, pos, agent):
        if pos in self.flags:
            self.goalReached[self.flags.index(pos)] = True
            if agent == 1 :
                self.goalReached1[self.flags.index(pos)] = True
                if not self.flags.index(pos) in self.flagsGot1:
                    self.flagsGot1.append(self.flags.index(pos))
            else:
                self.goalReached2[self.flags.index(pos)] = True
                if not self.flags.index(pos) in self.flagsGot2:
                    self.flagsGot2.append(self.flags.index(pos))


    def testFlags(self, pos, agent):
        if agent == 1:
            tmp = list(self.goalReached1)
        if agent == 2:
            tmp = list(self.goalReached2)
        #if pos in self.flags:
        #    tmp[self.flags.index(pos)] = True
        return tmp.count(True)

    def rewardShaping(self, currentPos, nextPos, agent):
        return self.gamma*self.phi(nextPos, agent)-self.phi(currentPos, agent)

    def phi(self, pos, agent):
        maxReward = 600.0
        if self.shape == "None":
            return 0
        elif self.shape == "Flags":
            #omega = len(self.flags)*100.0/len(self.flags)
            omega = 100
            return omega*self.testFlags(pos, agent)
        elif self.shape == "Solo":
            if agent == 1:
                omega = maxReward/(len(self.plan1Solo)-1)
            else:
                omega = maxReward/(len(self.plan2Solo)-1)
            return omega*self.getStepPlan(agent, pos, "Solo")
        elif self.shape == "Join":
            if agent == 1:
                omega = maxReward/(len(self.plan1Join)-1)
            else:
                omega = maxReward/(len(self.plan2Join)-1)
            return omega*self.getStepPlan(agent, pos, "Join")
            
            
    def getStepPlan(self, agent, pos, strat):
        if agent == 1:
            if strat == "Solo":
                plan = self.plan1Solo
            else:
                plan = self.plan1Join
            lastStep = self.lastStep1
        else:
            if strat == "Solo":
                plan = self.plan2Solo
            else:
                plan = self.plan2Join
            lastStep = self.lastStep2
        roomIn = self.getCurrentRoom(pos)
        flagsGot = self.getFlagsGot(agent)
        step = None
        for i in range(len(plan)):
            if plan[i][0] == roomIn:
                flagsRequired = plan[i][1:]
                if flagsRequired == flagsGot:
                    step = i
        #print (roomIn, flagsGot, plan[0][0], step)
        if step == None:
            step = lastStep
        if step > lastStep:
            if agent == 1:
                self.lastStep1 = step
            else:
                self.lastStep2 = step
        return step
                

    def getCurrentRoom(self, pos):
        return self.world[pos[1]][pos[0]]

    def getFlagsGot(self, agent):
        """
        if agent == 1:
            flags = self.goalReached1
        else:
            flags = self.goalReached2
        res = []
        for i in range(len(flags)):
            if flags[i]:
                res.append(i)
        """
        if agent == 1:
            res = self.flagsGot1
        else:
            res = self.flagsGot2
        return res



if __name__ == '__main__':
    epsilon = 0.1
    gamma = 0.99
    alpha = 0.1
    lambd = 0.4
    marl = rsMARL("world.txt", epsilon, gamma, alpha, "Join", lambd)
    marl.run()
