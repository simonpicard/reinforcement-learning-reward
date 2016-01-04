
def parse(filename):
        file = open(filename)
        content = file.readlines()
        size = list(map(int, content[0].strip().replace("\n", "").split(" ")))
        del content[0]
        #print(size)

        tmp = content[0].strip().strip("\n").split(", ")
        for i in range(len(tmp)):
            tmp[i] = tmp[i].split(" ")
        goal = list(map(int, tmp[0]))
        start = tmp[1:]
        for i in range(len(start)):
            start[i] = list(map(int, start[i]))
        nbAgent = len(start)
        #print(start)
        del content[0]
        #print(goal)

        # Doors
        tmp = content[0].strip().replace("\n", "").split(", ")

        doors = [[] for i in range(len(tmp))]
        for i in range(len(tmp)):
            doors[i] = list(map(int, tmp[i].split(" "))) #Convert list str into list int
        del content[0]
        #print(doors)

        # Flags
        tmp = content[0].strip().replace("\n", "").split(", ")
        flags = [[0, 0] for i in range(len(tmp))]
        for i in range(len(tmp)):
            flags[i] = list(map(int, tmp[i].split(" "))) #Convert list str into list int
        del content[0]
        #print(flags)

        world = [[0 for i in range(int(size[0]))] for j in range(int(size[1]))]
        for y in range(int(size[1])):
            content[y] = content[y].replace("\n", "")
            for x in range(int(size[0])):
                world[y][x] = int(content[y][x])
        #print(world)
        del content[:13]
        #print(content)
        
        sizet = int(content[0].strip("\n"))
        del content[0]
        flagsNames = []
        for i in range(sizet):
            flagsNames.append(content[0].strip("\n"))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        roomsNames = []
        for i in range(sizet):
            roomsNames.append(content[0].strip("\n"))
            del content[0]
        #print(flagsNames, roomsNames)
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan1Join = []
        for i in range(sizet):
            plan1Join.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan2Join = []
        for i in range(sizet):
            plan2Join.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan1Solo = []
        for i in range(sizet):
            plan1Solo.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan2Solo = []
        for i in range(sizet):
            plan2Solo.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan1Solo6 = []
        for i in range(sizet):
            plan1Solo6.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan2Solo6 = []
        for i in range(sizet):
            plan2Solo6.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan1Solo5 = []
        for i in range(sizet):
            plan1Solo5.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan2Solo5 = []
        for i in range(sizet):
            plan2Solo5.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan1Solo4 = []
        for i in range(sizet):
            plan1Solo4.append(content[0].strip("\n").split(" "))
            del content[0]
            
        sizet = int(content[0].strip("\n"))
        del content[0]
        plan2Solo4 = []
        for i in range(sizet):
            plan2Solo4.append(content[0].strip("\n").split(" "))
            del content[0]
            
        plan1Join = handlePlan(plan1Join, roomsNames, flagsNames)
        plan2Join = handlePlan(plan2Join, roomsNames, flagsNames)
        plan1Solo = handlePlan(plan1Solo, roomsNames, flagsNames)
        plan2Solo = handlePlan(plan2Solo, roomsNames, flagsNames)
        plan1Solo6 = handlePlan(plan1Solo6, roomsNames, flagsNames)
        plan2Solo6 = handlePlan(plan2Solo6, roomsNames, flagsNames)
        plan1Solo5 = handlePlan(plan1Solo5, roomsNames, flagsNames)
        plan2Solo5 = handlePlan(plan2Solo5, roomsNames, flagsNames)
        plan1Solo4 = handlePlan(plan1Solo4, roomsNames, flagsNames)
        plan2Solo4 = handlePlan(plan2Solo4, roomsNames, flagsNames)

        return size, goal, start, doors, flags, world, flagsNames, roomsNames, plan1Join, plan2Join, plan1Solo, plan2Solo, plan1Solo6, plan2Solo6, plan1Solo5, plan2Solo5, plan1Solo4, plan2Solo4


def handlePlan(plan, roomsNames, flagsNames):
    for i in range(len(plan)):
        flags = []
        room = plan[i][0]
        room = roomsNames.index(room)
        if len(plan[i]) > 1:
            flags = plan[i][1:]
            for j in range(len(flags)):
                flags[j] = flagsNames.index(flags[j])
        plan[i] = [room] + flags
    return plan