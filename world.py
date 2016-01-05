class World:
    def __init__(self, size, goal, doors, flags, world, flagsNames, roomsNames):
        self.size = size
        self.goal = goal
        self.doors = doors
        self.flags = flags
        self.world = world
        self.flagsNames = flagsNames
        self.roomsNames = roomsNames

        self.moves = [[0, -1], [1, 0], [0, 1], [-1, 0]] #x y N E S O

    def canMoveAvoid(self, pos, posToAvoid):
        x = pos[0]
        y = pos[1]
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

        for p in posToAvoid:
            if p in availablePoses:
                i = availablePoses.index(p)
                availableMoves.pop(i)
                availablePoses.pop(i)

        return availableMoves

    def canMove(self, pos):
        x = pos[0]
        y = pos[1]
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

    def isOnGoal(self, pos):
        return pos == self.goal

    def getNextPos(self, pos, move):
        return [pos[0] + self.moves[move][0], pos[1] + self.moves[move][1]]

    def isOnFlag(self, pos):
        if pos in self.flags:
            return True
        else:
            return False

    def getFlag(self, pos):
        return self.flags.index(pos)

    def getCurrentRoom(self, pos):
        return self.world[pos[1]][pos[0]]

    def flagsIndexToName(self, flags):
        res = []
        for f in flags:
            res.append(self.flagsNames[f])
        return res

    def roomsIndexToName(self, room):
        return self.roomsNames[room]