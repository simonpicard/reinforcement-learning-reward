from random import random, choice
import copy
from world import World
from worldParser import parse

shapeDic = {"None":0, "Flag":1, "Solo":2, "Join":3, "Flag+Solo":4, "Flag+Join":5}

class rsMARL:
    def __init__(self, w, epsilon, gamma, alpha, shape, lambd, plans, start):
        
        self.world = w

        self.shape = shape
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.lambd = lambd

        self.moves = [[0, -1], [1, 0], [0, 1], [-1, 0]] #x y N E S O
        self.totalReward = 0

        self.plan1Join = plans[0]
        self.plan2Join = plans[1]
        self.plan1Solo = plans[2]
        self.plan2Solo = plans[3]

        self.start = start

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

    def flagsIndex(self, flags):
        res = 0
        for i in rangel(len(flags)):
            if flags[i]:
                res += 2**i 
        return res


    def isDone(self):
        return self.world.isOnGoal(self.agent1) and self.world.isOnGoal(self.agent2)


    def reset(self):
        self.agent1 = self.start[0]
        self.agent2 = self.start[1]
        self.goalReached = [False]*len(self.world.flags)
        self.goalReached1 = [False]*len(self.world.flags)
        self.goalReached2 = [False]*len(self.world.flags)
        self.flagsGot1 = []
        self.flagsGot2 = []
        self.lastStep1 = 0
        self.lastStep2 = 0
        self.firstDone = None

    def run(self):
        Qas1 = [[[[0.0, 0.0, 0.0, 0.0] for i in range(self.world.size[0])] for j in range(self.world.size[1])] for k in range(2**6)]
        Qas2 = [[[[0.0, 0.0, 0.0, 0.0] for i in range(self.world.size[0])] for j in range(self.world.size[1])] for k in range(2**6)]
        z = False
        

        for run in range(1000):
            self.reset()
            step = 0
            sigma1 = None
            sigma2 = None
            action1 = choice(self.world.canMove(self.agent1))
            action2 = choice(self.world.canMove(self.agent2))
            path1 = []
            path2 = []
            done1 = False
            done2 = False
            while not self.isDone() :
                step += 1

                if not self.world.isOnGoal(self.agent1) and not done1:
                    path1.append(self.agent1)
                    flagIndex1 = self.flagsIndex(self.goalReached1)
                    self.agent1, Qas1, eTrace1, action1, p1, done1 = self.runAgent(self.agent1, Qas1, path1, action1, 1, flagIndex1)

                if not self.world.isOnGoal(self.agent2) and not done2:
                    path2.append(self.agent2)
                    flagIndex2 = self.flagsIndex(self.goalReached1)
                    self.agent2, Qas2, eTrace2, action2, p2, done2 = self.runAgent(self.agent2, Qas2, eTrace2, action2, 2, flagIndex1)

                if done1 and done2:
                    #print("okFinis")
                    if self.firstDone == 1:
                        self.agent1, Qas1, eTrace1, action1, p1, done1 = self.finishEpisode(self.agent1, Qas1, eTrace1, action1, 1)
                    else:
                        self.agent2, Qas2, eTrace2, action2, p2, done2 = self.finishEpisode(self.agent2, Qas2, eTrace2, action2, 2)


                if step%100 == 0:
                    if self.shape == "Solo" or self.shape == "Join":
                        print(step, self.world.isOnGoal(self.agent1), self.world.isOnGoal(self.agent2), self.getStepPlan(1, self.agent1, self.shape), self.getStepPlan(2, self.agent2, self.shape))
                    else:
                        print(step, done1, done2)
                #print (self.agent2)
                if step > 10000 and not z:
                    a = input("What to do")
                    if a == "e":
                        z = True
                        pass
                    else:
                        print("ok")
                        if not self.world.isOnGoal(self.agent1):
                            print(self.agent1, self.world.canMove(self.agent1), Qas1[self.agent1[1]][self.agent1[0]], action1, p1, self.testFlags([0,0],1))
                            for i in range(len(Qas1)):
                                for j in range(len(Qas1[i])):
                                    print(list(map(int, Qas1[i][j])), end= " ")
                                print("")
                        if not self.world.isOnGoal(self.agent2):
                            print(self.agent2, self.world.canMove(self.agent2), Qas2[self.agent2[1]][self.agent2[0]], action2, p2, self.testFlags([0,0],2))
                            for i in range(len(Qas2)):
                                for j in range(len(Qas2[i])):
                                    print(list(map(int, Qas2[i][j])), end= " ")
                                print("")

            self.totalReward += self.getFinalReward()
            print (run, step, self.goalReached.count(True), int(self.totalReward/(run+1)))
        print(path2)
        print(path1)

    def runAgent(self, pos, Qas, path, action, agent, flagIndex):
        #action = self.chooseAction(pos[0], pos[1], Qas)
        done = False
        nextPos = self.getNextPos(pos[0], pos[1], action)
        if self.world.isOnGoal(nextPos):
            if self.firstDone == None:
                self.firstDone = agent
                return pos, Qas, eTrace, action, "", True
            else:
                done = True
        reward = self.getReward(nextPos)
        #reward = self.testFlags(pos, agent)*100
        #if not self.world.isOnGoal(pos):
        #    reward = 0

        sigma, nextAction, p = self.getSigma(reward, nextPos, pos, action, Qas[flagIndex], agent)
        path.append((pos, action, flagIndex))
        eTrace, Qas = self.updateEligibilityTrace(path, sigma, Qas)

        self.checkFlags(nextPos, agent)
        return nextPos, Qas, eTrace, nextAction, p, done

    def finishEpisode(self, pos, Qas, eTrace, action, agent):
        #action = self.chooseAction(pos[0], pos[1], Qas)
        nextPos = self.getNextPos(pos[0], pos[1], action)
        reward = self.getReward(nextPos)
        #reward = self.testFlags(pos, agent)*100
        #if not self.world.isOnGoal(pos):
        #    reward = 0

        sigma, nextAction, p = self.getSigma(reward, nextPos, pos, action, Qas, agent)
        eTrace[pos[1]][pos[0]][action] = 1
        eTrace, Qas = self.updateEligibilityTrace(eTrace, sigma, Qas)

        self.checkFlags(nextPos, agent)
        return nextPos, Qas, eTrace, nextAction, p, True


    def probability(self, p):
        return random() < p

    def chooseAction(self, pos, Qas, agent):
        availableMoves = self.world.canMove(pos)
        if self.probability(self.epsilon):
            return choice(availableMoves), "random"
        else:
            maxValue, moves = self.computeMax(pos, availableMoves, Qas)
            return choice(moves), "greedy"

    def computeMax(self, pos, moves, Qas):
        x = pos[0]
        y = pos[1]
        res = -9999999999999999999
        best = []
        for i in range(len(moves)):
            current = Qas[y][x][moves[i]]
            if current > res:
                res = current
                best = [moves[i]]
            elif current == res:
                best.append(moves[i])
        return res, best

    def getNextPos(self, x, y, move):
        return [x + self.moves[move][0], y + self.moves[move][1]]

    def getReward(self, pos):
        if self.world.isOnGoal(pos):
            return self.getFinalReward()
        else:
            return -1

    def getFinalReward(self):
        return 100*self.goalReached.count(True)

    def updateEligibilityTrace(self, path, sigma, Qas):
        for f in range(len(Qas)):
            for y in range(len(Qas[f])):
                for x in range(len(Qas[f][y])):
                    for a in range(len(Qas[y][x])):
                        Qas[y][x][a] += self.alpha * sigma * eTrace[y][x][a]
                        eTrace[y][x][a] *= self.gamma * self.lambd
                        if eTrace[y][x][a] < 0.0000000001:
                            eTrace[y][x][a] = 0
        return eTrace, Qas
        
                
    def getSigma(self, reward, nextPos, currentPos, action, Qas, agent):
        nextAction, p = self.chooseAction(nextPos, Qas, agent)
        originalQ = Qas[currentPos[1]][currentPos[0]][action]
        nextQ = Qas[nextPos[1]][nextPos[0]][nextAction]
        sigma = \
            reward + (self.gamma*nextQ) - originalQ + self.rewardShaping(currentPos, nextPos, agent)

        return sigma, nextAction, p


    def checkFlags(self, pos, agent):
        if pos in self.world.flags:
            self.goalReached[self.world.flags.index(pos)] = True
            if agent == 1 :
                self.goalReached1[self.world.flags.index(pos)] = True
                if not self.world.flags.index(pos) in self.flagsGot1:
                    self.flagsGot1.append(self.world.flags.index(pos))
            else:
                self.goalReached2[self.world.flags.index(pos)] = True
                if not self.world.flags.index(pos) in self.flagsGot2:
                    self.flagsGot2.append(self.world.flags.index(pos))


    def testFlags(self, pos, agent):
        if agent == 1:
            tmp = list(self.goalReached1)
        if agent == 2:
            tmp = list(self.goalReached2)
        if pos in self.world.flags:
            tmp[self.world.flags.index(pos)] = True
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
        roomIn = self.world.getCurrentRoom(pos)
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

    size, goal, start, doors, flags, world, flagsNames, roomsNames, plan1Join, plan2Join, plan1Solo, plan2Solo =\
        parse("world.txt")

    w = World(size, goal, doors, flags, world, flagsNames, roomsNames)

    print(len(w.flags), w.flags)


    epsilon = 0.1
    gamma = 0.99
    alpha = 0.1
    lambd = 0.4
    plans = (plan1Join, plan2Join, plan1Solo, plan2Solo)
    marl = rsMARL(w, epsilon, gamma, alpha, "Flags", lambd, plans, start)
    marl.run()
