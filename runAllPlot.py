import rsMARL
import rsMARLPlan
from worldParser import parse
from world import *




size, goal, start, doors, flags, world, flagsNames, roomsNames, plan1Join, plan2Join, plan1Solo, plan2Solo, plan1Solo6, plan2Solo6, plan1Solo5, plan2Solo5, plan1Solo4, plan2Solo4 =\
    parse("world.txt")

w = World(size, goal, doors, flags, world, flagsNames, roomsNames)


epsilon = 0.1
gamma = 0.99
alpha = 0.1
lambd = 0.4
planJoin = (plan1Join, plan2Join)
planSolo = (plan1Solo, plan2Solo)
planSolo6 = (plan1Solo6, plan2Solo6)
planSolo5 = (plan1Solo5, plan2Solo5)
planSolo4 = (plan1Solo4, plan2Solo4)

nbSimulation = 5

#initial result

initialQ = 0.0
runs = 2000
competitive = False

#rsMARL.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, False, initialQ, runs, "txt/initial/no-shaping.txt", competitive)
#rsMARL.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, True, initialQ, runs, "txt/initial/flag-based.txt", competitive)

rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planJoin, False, initialQ, runs, "txt/initial/joint-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo, False, initialQ, runs, "txt/initial/individual-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planJoin, True, initialQ, runs, "txt/initial/flag+joint-plan.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo, True, initialQ, runs, "txt/initial/flag+individual-plan.txt", competitive)
"""
#competitive reward

initialQ = 0.0
runs = 2000
competitive = True

rsMARL.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, False, initialQ, runs, "txt/competitive/no-shaping.txt", competitive)
rsMARL.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, True, initialQ, runs, "txt/competitive/flag-based.txt", competitive)

rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planJoin, False, initialQ, runs, "txt/competitive/joint-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo, False, initialQ, runs, "txt/competitive/individual-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planJoin, True, initialQ, runs, "txt/competitive/flag+joint-plan.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo, True, initialQ, runs, "txt/competitive/flag+individual-plan.txt", competitive)



#improve knowledge pessimistic

initialQ = 0.0
runs = 2000
competitive = False

rsMARL.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, False, initialQ, runs, "txt/knowledgePessimistic/no-shaping.txt", competitive)

rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planJoin, False, initialQ, runs, "txt/knowledgePessimistic/joint-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo, False, initialQ, runs, "txt/knowledgePessimistic/individual-plan-based.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo4, False, initialQ, runs, "txt/knowledgePessimistic/plan-based-4.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo5, False, initialQ, runs, "txt/knowledgePessimistic/plan-based-5.txt", competitive)
rsMARLPlan.runFor(nbSimulation, w, epsilon, gamma, alpha, lambd, start, planSolo6, False, initialQ, runs, "txt/knowledgePessimistic/plan-based-6.txt", competitive)
"""
