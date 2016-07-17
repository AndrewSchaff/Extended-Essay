import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

target = 1.0
trainingEpochs = 10

def trainingGraph(runNumber, iterationNumber, networkNumber):
    path = "./Data/Run " + str(runNumber) + "/Iteration " + str(iterationNumber) + "/Network " + str(networkNumber)

    trainingData = pickle.load(open(path + "/network.pkl")).trainingPerformance

    if len(trainingData) == 0:
        trainingData = [0]*trainingEpochs
        
    elif len(trainingData) < trainingEpochs:
        trainingData += trainingData[-1]*(trainingEpochs-len(trainingData))

    #Add a title
    #fig = plt.figure()
    plt.suptitle('Network Training Performance', fontsize=20)
    plt.title('Run: ' + str(runNumber) + " | Iteration: " + str(iterationNumber) + " | Network: " + str(networkNumber), fontsize = 15)
    
    #Set up y axis limits
    if max(trainingData) <= 5:
        ymax = 5

    else:
        ymax = max(trainingData) + 1

    #Add in axes
    axes = plt.gca()
    plt.xlim([1, trainingEpochs])
    plt.ylim([0, ymax])

    #Set up axis ticks
    y_tick_size = 0.5
    plt.xticks(np.arange(1, trainingEpochs + 1, 1))
    plt.yticks(np.arange(0, ymax + y_tick_size, y_tick_size))

    #Plot the graphs and set up a legend
    plt.plot(range(1,11), trainingData[:trainingEpochs], 'r-', marker = "o", label = "Training Performance")
    plt.plot(range(1,11), [target]*trainingEpochs, 'b-', label="Training Target")
    plt.legend()
    
    #Set up axis labels
    plt.xlabel('Training Epoch', fontsize=16)
    plt.ylabel('Network Mean Squared Error (MSE)', fontsize=16)
    
    #plt.show()
    plt.savefig(path + "/Training Performance.png")
    plt.clf() #Clear the graph, so it's ready for another network
    
"""
def generateGraphs(runNumber):
    path = "./Data/Run " + str(runNumber)
    runs = 
"""

def graphAllNetworks():
    for iterationNumber in range(1, 26):
        for networkNumber in range(25):
            print "Producing Graph -    Run: 22 | Iteration: " + str(iterationNumber) + " | Network: " + str(networkNumber)
            trainingGraph(22, iterationNumber, networkNumber)
            #trainingData = pickle.load(open("./Data/Run 22/Iteration " + str(iterationNumber) + "/Network " + str(networkNumber) + "/network.pkl")).trainingPerformance

            #print trainingData

#trainingGraph(22,1,11)

def graphGrades(runNumber, grades=[]):
    #If no existing grades have been passed, get them from the training datas
    if not grades:
        files = os.listdir("./Data/Run " + str(runNumber) + "/") #Get a list of all iterations

        #Remove evolution_parameters.pkl from the list (interferes with sorting)
        if 'evolution_parameters.pkl' in files:
            del files[files.index('evolution_parameters.pkl')]

        #Remove .DS_Store if it exists (also interferes with sorting)
        if '.DS_Store' in files:
            del files[files.index('.DS_Store')]

        #Sort iterations by iteration number (not the ASCII value of the number)
        files = sorted(files, key = lambda x: int(x.split(" ")[-1]))

        #Store grades in this list
        grades = []

        #Loop over every iteration, calculating grades
        for iterationNumber in range(int(files[-1].split(" ")[-1])):
            networks = os.listdir("./Data/Run " + str(runNumber) + "/Iteration " + str(iterationNumber) + "/") #Get a list of all networks

            #Remove .DS_Store if it's there
            if '.DS_Store' in networks:
                del networks[networks.index('.DS_Store')]

            #Sort networks exactly the same as we did earlier
            networks = sorted(networks, key = lambda x: int(x.split(" ")[-1]))

            #Figure out how many networks we have
            NumberOfNetworks = int(networks[-1].split(" ")[-1])
            
            trainingPerformances = [] #Store all training performances here

            #For each network, open its file and look at its trainingPerformance
            for networkNumber in range(NumberOfNetworks):
                network = pickle.load(open("./Data/Run " + str(runNumber) + "/Iteration " + str(iterationNumber) + "/Network " + str(networkNumber) + "/network.pkl"))

                #Only append the minimum value if the network has been trained at all
                if len(network.trainingPerformance) > 0:
                    trainingPerformances.append(float(min(network.trainingPerformance)))
            
            #Sort training performances
            trainingPerformances = sorted(trainingPerformances)

            #Calculate the population's grade based on its best 4 networks
            grade = float(sum(trainingPerformances[:4]))/4.0

            #Add the calculated grade to the list of grades and print a status line
            grades.append(grade)
            print "Iteration " + str(iterationNumber) + " - Grade: " + str(grade)

    #Generate a plot of performance over time
    plt.suptitle('Genetic Algorithm Performance', fontsize=20)
    
    #Set up y axis limits
    if max(grades) <= 5:
        ymax = 5

    else:
        ymax = max(grades) + 1
    
    #Add in axes
    axes = plt.gca()
    plt.xlim([1, len(grades)])
    plt.ylim([0, ymax])

    #Set up axis ticks
    y_tick_size = 0.5
    plt.xticks(np.arange(1, len(grades) + 1, 1))
    plt.yticks(np.arange(0, ymax + y_tick_size, y_tick_size))

    #Plot the graphs and set up a legend
    plt.plot(range(1,len(grades) + 1), grades, 'r-', marker = "o", label = "Training Performance")
    plt.plot(range(1,len(grades) + 1), [1]*len(grades), 'b-', label="Training Target")
    plt.legend()
    
    #Set up axis labels
    plt.xlabel('Iteration Number', fontsize=16)
    plt.ylabel('Population Grade', fontsize=16)
    
    #plt.show()
    plt.savefig("./Data/Run " + str(runNumber) + "/Overall Performance.png")

#g = [2.361982804038315, 2.2385818347193136, 2.3776056997851445, 2.3951035358990325, 2.3605108440038034, 2.3684446686868545, 2.364004924002877, 2.519939791346689, 2.6341046434749256, 2.5100141897380945, 2.52685976988922, 2.4150586924403954, 2.580738104061143, 2.5502292050278537, 2.490292920526759, 2.4383036658527435, 2.3561073292288324, 2.18901608669301, 2.191661467093774, 2.316211602718154, 2.1575377854165887, 2.0135166045015533, 2.219572113689853, 2.589381054244161, 2.488715667179986]
graphGrades(22)
