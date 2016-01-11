import matplotlib.pyplot as plt

plt.style.use("bmh")


def printInFile(path, tist):
    f = open(path, 'w')
    f.write("[")
    for i in range(len(tist)-1):
        f.write("%s, " % tist[i])
    f.write(str(tist[-1]) + "]")
    f.close()


def evalFile(path):
    f = open(path, 'r')
    res = eval(f.read())
    f.close()
    return res

def handlePlot(xLabel, yLabel, title, data, legend, fOut):
    c= ['b','g','r','c','m','y', "orange","saddlebrown"]

    plt.title(title)
    for i in range(len(data)):
        plt.plot(data[i], label=legend[i])

    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
        
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 0),\
          ncol=2, fancybox=True, shadow=True)

    plt.savefig(fOut)
    plt.cla()
    plt.clf()

def readAndPlot(xLabel, yLabel, title, fOut, files):
    data = []
    legend = []
    for i in range(len(files)):
        tmp = files[i].split(".")[0]
        tmp = tmp.split("/")[-1]
        legend.append(tmp)
        tmpdata = evalFile(files[i])
        dataformated = []
        res = 0
        for j in range(len(tmpdata)):
            if j%100 == 0:
                dataformated.append(res/100)
                res = 0
            res += tmpdata[j]
        dataformated.append(res/100)
        data.append(dataformated)

    handlePlot(xLabel, yLabel, title, data, legend, fOut)



if __name__ == "__main__":

    readAndPlot("(#*100) Episodes", "Total discounted reward", "Initial results", "initial.png", ['txt/initial/no-shaping.txt', 'txt/initial/flag-based.txt', 'txt/initial/joint-plan-based.txt', 'txt/initial/individual-plan-based.txt', 'txt/initial/flag+joint-plan.txt', 'txt/initial/flag+individual-plan.txt'])
    readAndPlot("(#*100) Episodes", "Total discounted reward", "Knowledge Pessimistic results", "knowledgePessimistic.png", ['txt/knowledgePessimistic/no-shaping.txt', 'txt/knowledgePessimistic/joint-plan-based.txt', 'txt/knowledgePessimistic/individual-plan-based.txt', 'txt/knowledgePessimistic/plan-based-4.txt', 'txt/knowledgePessimistic/plan-based-5.txt', 'txt/knowledgePessimistic/plan-based-6.txt'])
    readAndPlot("(#*100) Episodes", "Total discounted reward", "Cooperation results", "coop.png", ['txt/coop/no-shaping.txt', 'txt/coop/flag-based.txt', 'txt/coop/joint-plan-based.txt', 'txt/coop/individual-plan-based.txt', 'txt/coop/flag+joint-plan.txt', 'txt/coop/flag+individual-plan.txt'])
    
