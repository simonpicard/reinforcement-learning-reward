class rsMARL:
    def __init__(self, filename):
        self.parse(filename)
        self.goalReached = [False]*len(self.flags)
        pass
    
    def parse(self, filename):
        file = open(filename)
        content = file.readlines()
        self.size = content[0].strip().replace("\n", "").split(" ")
        del content[0]
        print(self.size)

        tmp = content[0].strip().replace("\n", "").split(",")
        for i in range(len(tmp)):
            tmp[i] = tmp[i].split(" ")
        self.goal = tmp[0]
        self.start = tmp[1:]
        self.nbAgent = len(self.start)
        del content[0]

        print(self.goal)

        # Doors
        tmp = content[0].strip().replace("\n", "").split(", ")

        self.doors = [[0, 0, 0, 0] for i in range(len(tmp))]
        for i in range(len(tmp)):
            self.doors[i] = tmp[i].split(" ")
        del content[0]

        print(self.doors)

        # Flags
        tmp = content[0].strip().replace("\n", "").split(", ")
        self.flags = [[0, 0] for i in range(len(tmp))]
        for i in range(len(tmp)):
            self.flags[i] = tmp[i].split(" ")
        del content[0]

        print(self.flags)

        self.world = [[0 for i in range(int(self.size[0]))] for j in range(int(self.size[1]))]
        for y in range(int(self.size[1])):
            content[y] = content[y].replace("\n", "")
            for x in range(int(self.size[0])):
                self.world[y][x] = content[y][x]

        print(self.world)


if __name__ == '__main__':
    marl = rsMARL("world")
