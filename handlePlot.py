import matplotlib.pyplot as plt

plt.style.use("bmh")


def printInFile(path, tist):
    f = open(path, 'w')
    f.write(str(tist))
    f.close()


def evalFile(path):
    f = open(path, 'r')
    res = eval(f.read())
    f.close()
    return res

def handlePlot(xAxis, yAxis, xLabel, yLabel, title, data, legend, fOut):
    c= ['b','g','r','c','m','y', "orange","saddlebrown"]
    plt.axis([xAxis[0], xAxis[1], yAxis[0], yAxis[1]])
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.title(title)
    for i in range(len(data)):
        plt.plot(data[i], label=legend[i])
        
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1),\
          ncol=3, fancybox=True, shadow=True)
    plt.savefig(fOut)
    plt.cla()
    plt.clf()

def readAndPlot(xAxis, yAxis, xLabel, yLabel, title, fOut, files):
    data = []
    legend = []
    for i in range(len(files)):
        tmp = files[i].split(".")[0]
        tmp = tmp.split("/")[-1]
        legend.append(tmp)
        data.append(evalFile(files[i]))
    handlePlot(xAxis, yAxis, xLabel, yLabel, title, data, legend, fOut)



if __name__ == "__main__":

    t = [1,3,5,4,6,3,2,5,9,14]

    printInFile("test.txt", t)
    print(evalFile("test.txt")[3])