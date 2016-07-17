import os
import pickle
import GA
import graphics
from shutil import rmtree

#Start a new session (most of this works within GA.continuousEvolution)
def createSession(popSize = 45, iterations = 10, mutate=0.2, extraParents=0.1, originalParents=0.2, hiddenLayers = 3, maxLayerSize = 15, trainingTimeout = 10, trainingTarget = 1.0):
    global window
    population = GA.networkLib.createPopulation(popSize, hiddenLayers, maxLayerSize)

    #Startup the graphics window
    window = graphics.StatusWindow(iterations, popSize, trainingTimeout, trainingTarget)
    window.update()
    #raise Exception("Program stopped!")
    
    #Set up an object to store evolutionary parameters
    params = GA.EvolutionObject()
    
    params.popSize = popSize
    params.iterations = iterations
    params.mutate = mutate
    params.extraParents = extraParents
    params.originalParents = originalParents
    params.trainingTimeout = trainingTimeout
    params.trainingTarget = trainingTarget

    #Start the program
    GA.continuousEvolution(population, params, graphicsWindow = window)

#Load up a new session
def loadSession(runNumber, openSecondToLast=True):
    try:
        directory = "./Data/Run " + str(runNumber)
        iterations = os.listdir(directory)
        
    except OSError:
        print "Directory not found"
        return None

    #Setup iterationNumber (prepares the program to import networks)
    if openSecondToLast and len(iterations) > 1:
        iterationNumber = int(iterations[-2].split()[-1])

    else:
        iterationNumber = int(iterations[-1].split()[-1])

    #Start loading networks
    directory += "/Iteration " + str(iterationNumber)
    networks = os.listdir(directory)

    population = []
    for network in networks:
        f = open(directory + "/" + network + "/network.pkl", 'rb')
        population.append(pickle.load(f))
        f.close()

    try:
        evolutionParameters = pickle.load(open("./Data/Run " + str(runNumber) + "/evolution_parameters.pkl"))
    
    except IOError:
        print "Cannot find parameters file!  Using default settings"

        evolutionParameters = GA.EvolutionObject()
    
    return population, evolutionParameters

#Resume a new session
def resumeSession(runNumber):
    #raise Exception("Not properly integrated with new graphics!  Exiting...")
    population, params = loadSession(runNumber)

    path = "./Data/Run " + str(runNumber)

    #Get the iteration number
    try:
        os.remove(path + "/.DS_Store") #Try and get rid of .DS_Store

    except:
        pass
    
    iterNumber = int(sorted(os.listdir(path)[1:], key=lambda x: int(x.split(" ")[-1]))[-1].split(" ")[-1]) + 1

    """
    #What that (^) line does
     - Gets a list of all files in the directory ./Data/Run # and get rid of evolution_parameters.pkl     os.listdir(path)[1]
     - Sorts the list based on the number after 'Iteration '                                              sorted(os.listdir(path), key=lambda x: int(x.split(" ")[-1])
     - Gets the last element and extracts its number                                                      [-1].split(" ")[-1])
     - Increments that number by 1                                                                         + 1
    """
    
    #Startup the graphics window
    window = graphics.StatusWindow(params.iterations, params.popSize, params.trainingTimeout, params.trainingTarget)
    
    #Restart evolution
    GA.continuousEvolution(population, params, run_number = runNumber, start_iteration_number = iterNumber, graphicsWindow = window)
    
#Delete a session
def deleteSession(runNumber, warn=True):
    #Skip the warning message if warn==False
    if warn:
        #Warn the user
        if raw_input("This will completely remove a session.  Are you REALLY sure you want to do this (yes/no)? ").lower() != "yes":
            print "./Data/Run " + str(runNumber) + " was not deleted"
            return None

    try:
        rmtree("./Data/Run " + str(runNumber))
        print "./Data/Run " + str(runNumber) + " was deleted"
        
    except OSError:
        print "Can't find directory - ./Data/Run " + str(runNumber)

def generateParameters(popSize = 100, iterations = 25, mutate = 0.15, extraParents = 0.1, originalParents = 0.2, hiddenLayers = 15, maxLayerSize = 45, trainingTimeout = 12, trainingTarget = 1.0):

    #Set up an object to store evolutionary parameters
    params = GA.EvolutionObject()
    
    params.popSize = popSize
    params.iterations = iterations
    params.mutate = mutate
    params.extraParents = extraParents
    params.originalParents = originalParents
    params.trainingTimeout = trainingTimeout
    params.trainingTarget = trainingTarget

    pickle.dump(params, open("Generated evolution_parameters.pkl", 'w'))
    
def viewParams(runNumber):
    if not os.path.exists("./Data/Run " + str(runNumber)): raise Exception("Path not found!")

    return pickle.load('./Data/Run ' + str(runNumber) + "/evolution_parameters.pkl")
                         
#pop, params = loadSession(8)

#print pop
#print params
"""
if __name__ == "__main__":
    createSession(

        popSize = 25,
        iterations = 25,
        mutate = 0.2,
        extraParents = 0.1,
        originalParents = 0.2,
        hiddenLayers = 1,
        maxLayerSize = 15,
        trainingTimeout = 10,
        trainingTarget = 1.0

        )
"""


#resumeSession(22)
