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

    #readAndPlot("(#*100) Episodes", "Total discounted reward", "Initial results", "initial.png", \
    #    ['txt/initial/no-shaping.txt','txt/initial/flag-based.txt','txt/initial/joint-plan-based.txt', 'txt/initial/individual-plan-based.txt',\
    #    'txt/initial/joint-plan.txt', 'txt/initial/individual-plan-based.txt'])
    #readAndPlot("(#*100) Episodes", "Total discounted reward", "Improve knowledge", "knwoledge.png", ['txt/initial/joint-plan-based.txt', 'txt/initial/individual-plan-based.txt'])
    #readAndPlot("(#*100) Episodes", "Total discounted reward", "Improve cooperation", "coop.png", ['txt/initial/joint-plan-based.txt', 'txt/initial/individual-plan-based.txt'])



    readAndPlot("(#*100) Episodes", "Total discounted reward", "Initial results", "initialtweek.png", ['txt/tweeked/initial/no-shaping.txt', 'txt/tweeked/initial/flag-based.txt', 'txt/tweeked/initial/joint-plan-based.txt', 'txt/tweeked/initial/individual-plan-based.txt', 'txt/tweeked/initial/flag+joint-plan.txt', 'txt/tweeked/initial/flag+individual-plan.txt'])
    readAndPlot("(#*100) Episodes", "Total discounted reward", "Improved knowledge", "knowledgetweek.png", ['txt/tweeked/knowledge/no-shaping.txt', 'txt/tweeked/knowledge/joint-plan-based.txt', 'txt/tweeked/knowledge/individual-plan-based.txt', 'txt/tweeked/knowledge/plan-based-4.txt', 'txt/tweeked/knowledge/plan-based-5.txt', 'txt/tweeked/knowledge/plan-based-6.txt'])
    readAndPlot("(#*100) Episodes", "Total discounted reward", "Cooperation", "cooptweek.png", ['txt/tweeked/coop/no-shaping.txt', 'txt/tweeked/coop/joint-plan-no-coop.txt', 'txt/tweeked/coop/individual-plan-no-coop.txt', 'txt/tweeked/coop/individual-plan-coop.txt'])
