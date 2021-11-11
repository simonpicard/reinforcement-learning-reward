from random import random, choice
import copy
from world import World
from worldParser import parse
import numpy as np
from handlePlot import *

shapeDic = {"None":0, "Flag":1, "Solo":2, "Join":3, "Flag+Solo":4, "Flag+Join":5}

class rsMARL:
    def __init__(self, w, epsilon, gamma, alpha, lambd, start, flagShape, initialQ, runs, coop):
        
        self.world = w

        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.lambd = lambd

        self.moves = [[0, -1], [1, 0], [0, 1], [-1, 0]] #x y N E S O
        self.totalReward = 0

        self.start = start

        self.flagShape = flagShape

        self.initialQ = initialQ

        self.runs = runs

        self.rewards = [0.0]*runs

        self.competitive = False

        self.coop = coop

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
        for i in range(len(flags)):
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
        self.lel1 = []
        self.lel2 = []
        self.lastStep1 = 0
        self.lastStep2 = 0
        self.firstDone = None

    def run(self):
        Qas1 = [[[[self.initialQ]*4 for k in range(2**6)] for i in range(self.world.size[0])] for j in range(self.world.size[1])]
        Qas2 = [[[[self.initialQ]*4 for k in range(2**6)] for i in range(self.world.size[0])] for j in range(self.world.size[1])]
        z = False
        
        for run in range(self.runs):
            self.reset()
            step = 0
            done1 = False
            done2 = False
            self.done1 = done1
            self.done2 = done2
            action1 = choice(self.world.canMove(self.agent1))
            action2 = choice(self.world.canMove(self.agent2))
            self.action2 = action2
            self.action1 = action1
            path1 = []
            path2 = []
            done1 = False
            done2 = False
            flagIndex1 = 0
            flagIndex2 = 0
            quitted = False
            while not self.isDone() :
                step += 1

                if not self.world.isOnGoal(self.agent1) and not done1:
                    self.agent1, Qas1, action1, p1, done1, flagIndex1 = self.runAgent(self.agent1, Qas1, path1, action1, 1, flagIndex1)
                    self.action1 = action1
                    self.done1 = done1

                if not self.world.isOnGoal(self.agent2) and not done2:
                    self.agent2, Qas2, action2, p2, done2, flagIndex2 = self.runAgent(self.agent2, Qas2, path2, action2, 2, flagIndex2)
                    self.action2 = action2
                    self.done2 = done2

                if done1 and done2:
                    if self.firstDone == 1:
                        self.agent1, Qas1, action1, p1, done1, flagIndex1 = self.finishEpisode(self.agent1, Qas1, path1, action1, 1, flagIndex1)
                    else:
                        self.agent2, Qas2, action2, p2, done2, flagIndex2 = self.finishEpisode(self.agent2, Qas2, path2, action2, 2, flagIndex2)
                
                if step > 20000:
                    print("Quitted")
                    quitted = True
                    break

            if False:
                self.rewards[run] = self.rewards[run-1]
            else:
                self.rewards[run] = self.getTotalReward()*(self.gamma**step)
            #print (run, step, self.getTotalReward(), self.getTotalReward()*(self.gamma**step), self.world.flagsIndexToName(self.flagsGot1), self.world.flagsIndexToName(self.flagsGot2), int(self.phi(path1[-1][0], 1)), int(self.phi(path2[-1][0], 2)))
        #print(path2)
        #print(path1)
        #print(self.world.flagsIndexToName(self.flagsGot1))
        #print(self.world.flagsIndexToName(self.flagsGot2))

    def printShit(self, pos, agent):
        return (self.getStepPlan(agent, pos, "Join"), self.world.roomsIndexToName(self.world.getCurrentRoom(pos)), self.world.flagsIndexToName(self.getFlagsGot(agent, pos)))


    def runAgent(self, pos, Qas, path, action, agent, flagIndex):
        #action = self.chooseAction(pos[0], pos[1], Qas)
        path.append((pos, action, flagIndex))
        done = False
        nextPos = self.getNextPos(pos[0], pos[1], action)

        if self.world.isOnGoal(nextPos):
            if self.firstDone == None:
                self.firstDone = agent
                return pos, Qas, action, "", True, flagIndex
            else:
                done = True

        reward = self.getReward(nextPos, agent)

        sigma, nextAction, p, nextFlagIndex = self.getSigma(reward, nextPos, pos, action, Qas, agent, flagIndex)
        Qas = self.updateEligibilityTrace(path, sigma, Qas)

        self.checkFlags(nextPos, agent)
        return nextPos, Qas, nextAction, p, done, nextFlagIndex

    def finishEpisode(self, pos, Qas, path, action, agent, flagIndex):
        path.append((pos, action, flagIndex))
        nextPos = self.getNextPos(pos[0], pos[1], action)
        reward = self.getReward(nextPos, agent)

        sigma, nextAction, p, nextFlagIndex = self.getSigma(reward, nextPos, pos, action, Qas, agent, flagIndex)
        Qas = self.updateEligibilityTrace(path, sigma, Qas)

        self.checkFlags(nextPos, agent)
        return nextPos, Qas, nextAction, p, True, nextFlagIndex


    def probability(self, p):
        return random() < p

    def chooseAction(self, pos, Qas, agent, flagsIndex):
        posToAvoid = []
        if agent == 1 and not self.done2:
            posToAvoid.append(self.getNextPos(self.agent2[0], self.agent2[1], self.action2))
        elif agent == 2 and not self.done1:
            posToAvoid.append(self.getNextPos(self.agent1[0], self.agent1[1], self.action1))
        availableMoves = self.world.canMoveAvoid(pos, posToAvoid)
        if self.probability(self.epsilon):
            return choice(availableMoves), "random"
        else:
            maxValue, moves = self.computeMax(pos, availableMoves, Qas, flagsIndex)
            ret = choice(moves)
            return ret, "greedy"

    def computeMax(self, pos, moves, Qas, flagsIndex):
        x = pos[0]
        y = pos[1]
        res = -9999999999999999999
        best = []
        for i in range(len(moves)):
            current = Qas[y][x][flagsIndex][moves[i]]
            if current > res:
                res = current
                best = [moves[i]]
            elif current == res:
                best.append(moves[i])
        return res, best

    def getNextPos(self, x, y, move):
        return [x + self.moves[move][0], y + self.moves[move][1]]

    def getReward(self, pos, agent):
        if self.world.isOnGoal(pos):
            if self.competitive:
                return self.getCompetitiveReward(agent)
            else:
                return self.getTotalReward()
        else:
            return 0

    def getCompetitiveReward(self, agent):
        if agent == 1:
            return 100*self.goalReached1.count(True)
        else:
            return 100*self.goalReached2.count(True)

    def getTotalReward(self):
        return 100*self.goalReached.count(True)

    def updateEligibilityTrace(self, path, sigma, Qas):
        #size = min (len(path), 56)
        cells = min(len(path), 56)
        #(0.99*0.4)**805 = 0.0
        size = len(path)
        for i in range (size-1, size-cells-1, -1):
            pos, a, flagsIndex = path[i]
            x, y = pos
            Qas[y][x][flagsIndex][a] += self.alpha*sigma*(self.gamma * self.lambd)**(size -1 - i)

        return Qas
        
                
    def getSigma(self, reward, nextPos, currentPos, action, Qas, agent, flagIndex):
        originalQ = Qas[currentPos[1]][currentPos[0]][flagIndex][action]

        nextFlagIndex = self.testFlagsIndex(nextPos, agent)

        nextAction, p = self.chooseAction(nextPos, Qas, agent, nextFlagIndex)
        nextQ = Qas[nextPos[1]][nextPos[0]][nextFlagIndex][nextAction]
        sigma = \
            reward + (self.gamma*nextQ) - originalQ + self.rewardShaping(currentPos, nextPos, agent)

        return sigma, nextAction, p, nextFlagIndex


    def checkFlags(self, pos, agent):
        if self.coop == False:
            flag = None
            if pos in self.world.flags:
                flag = self.world.flags.index(pos)
            else:
                return
            if not self.goalReached[flag]:
                self.goalReached[flag] = True
                if agent == 1 :
                    self.flagsGot1.append(flag)
                    self.goalReached1[flag] = True
                else:
                    self.flagsGot2.append(flag)
                    self.goalReached2[flag] = True
        else:
            flag = None
            if pos in self.world.flags:
                flag = self.world.flags.index(pos)
            else:
                return
            if not self.goalReached[flag]:
                self.goalReached[flag] = True
                if agent == 1 :
                    self.lel1.append(flag)
                    self.flagsGot1.append(flag)
                    self.flagsGot2.append(flag)
                    self.goalReached1[flag] = True
                    self.goalReached2[flag] = True
                else:
                    self.lel2.append(flag)
                    self.flagsGot2.append(flag)
                    self.flagsGot1.append(flag)
                    self.goalReached2[flag] = True
                    self.goalReached1[flag] = True

    def testFlags(self, pos, agent):
        if agent == 1:
            tmp = list(self.goalReached1)
        if agent == 2:
            tmp = list(self.goalReached2)
        if pos in self.world.flags:
            f = self.world.flags.index(pos)
            if not self.goalReached[f]:
                tmp[f] = True
        return tmp.count(True)


    def testFlagsIndex(self, pos, agent):
        if agent == 1:
            tmp = list(self.goalReached1)
        if agent == 2:
            tmp = list(self.goalReached2)
        if pos in self.world.flags:
            f = self.world.flags.index(pos)
            if not self.goalReached[f]:
                tmp[f] = True
        return self.flagsIndex(tmp)

    def rewardShaping(self, currentPos, nextPos, agent):
        currentPhi = self.phi(currentPos, agent)
        nextPhi = self.phi(nextPos, agent) #that order
        a = self.gamma*nextPhi-currentPhi
        return a

    def phi(self, pos, agent):
        maxReward = 600.0
        
        if self.world.isOnGoal(pos):
            return 0
        elif not self.flagShape:
            return 0
        else:
            #omega = len(self.flags)*100.0/len(self.flags)
            omega = 100
            return omega*self.testFlags(pos, agent)


def runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, flagShape, initialQ, runs, fOut, competitive):
    print(fOut)
    rewards = [0.0]*runs

    for i in range(nbSimulation):
        print(i)
        marl = rsMARL(w, epsilon, gamma, alpha, lambd, start, flagShape, initialQ, runs, competitive)
        marl.run()
        tmp = [0.0]*runs
        for i in range(runs):
            tmp[i] += marl.rewards[i]
        rewards = np.add(rewards, tmp)

    for i in range(runs):
        rewards[i] /= (nbSimulation)
        #print(rewards[i])

    printInFile(fOut, rewards)

if __name__ == '__main__':

    size, goal, start, doors, flags, world, flagsNames, roomsNames, plan1Join, plan2Join, plan1Solo, plan2Solo, plan1Solo6, plan2Solo6, plan1Solo5, plan2Solo5, plan1Solo4, plan2Solo4 =\
        parse("world.txt")

    w = World(size, goal, doors, flags, world, flagsNames, roomsNames)

    epsilon = 0.1
    gamma = 0.99
    alpha = 0.1
    lambd = 0.4


    nbSimulation = 30

    initialQ = 0.0
    runs = 2000

    for i in range(1):
        print(i)
        marl = rsMARL(w, epsilon, gamma, alpha, lambd, start, False, 600.0, runs, False)
        marl.run()