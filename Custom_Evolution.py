import os
import GA
import networkLib
from shutil import rmtree



trainingParameters = {
    "tolerance" : 0.05,
    "verbose" : True,
    "timeout" : 20,
    }

path = "./Custom Sessions/Session 0" #This will be redefined later, it's just here as a backup for now

def startNewCustomSession():
    global path

    if ".DS_Store" in os.listdir("./Custom Sessions"):
        os.remove(".DS_Store")
        
    #Find a place to store the networks
    try:
        sessionNumber = int(sorted(os.listdir("./Custom Sessions"), key=lambda x: int(x.split(" ")[-1]))[-1].split(" ")[-1]) + 1
 
    except:
        sessionNumber = 0

    path = "./Custom Sessions/Session " + str(sessionNumber)
    os.mkdir(path)

    startInterpreter(path)
    
def startInterpreter(path):
    while True:
        try:
            cmd = raw_input("C>> ")
            if cmd in commands:
                if cmd == "exit": break
                
                commands[cmd]()

            else:
                print "Command not found"

        except KeyboardInterrupt:
            continue

def createNetwork():
    networkStructure = raw_input("Network Structure> ").split(" ")

    networkName = "784 " + " ".join(networkStructure) + " 10"
    print "Creating a network with the following structure: " + networkName
    
    if len(networkStructure) > 1:
           networkStructure = map(int, networkStructure) #Set all the hidden layers to integers
    else:
           networkStructure = []

    network = networkLib.netObj(networkStructure)

    print "Evaluating network now..."
    network_fitness = evaluateNetwork(network)
    
    print "Average Error: " + str(network_fitness)
    
    network.saveSimple(path, networkName + " (" + str(network_fitness)[:5] + ")")

    if raw_input("Would you like to do a manual check? (y/n): ") == "y":
        network.visualCheck()
    
def evaluateNetwork(network):
    global commands
    
    printDict(trainingParameters)
    if raw_input("Do you want to use these parameters? (y/n): ") == "n":
        while True:
            try:
                trainingParameters["tolerance"] = float(raw_input("Target: "))
                trainingParameters["verbose"] = bool(raw_input("Verbose?: "))
                trainingParameters["timeout"] = int(raw_input("Training timeout: "))
            except:
                print "Error encountered! Please start again"
                continue
            
            finally:
                break
    

    try:
        MSE = network.train(tolerance = trainingParameters["tolerance"], verbose = trainingParameters["verbose"], timeout = trainingParameters["timeout"])

    except KeyboardInterrupt:
        print "Training Stopped!"

    except Exception as e:
        print "Training cannot be performed!"
        print e
        return 10000

    fitness = network.evaluate()
    
    return fitness

def loadNetwork():
    existingNetworks = os.listdir(path)

    if ".DS_Store" in existingNetworks:
        del existingNetworks[existingNetworks.index(".DS_Store")]

    for a in existingNetworks:
        print "[" + str(existingNetworks.index(a)) + "] " + a

def printDict(dictionary):
    print ""
    for entry in dictionary:
        print str(entry) + " : " + str(dictionary[entry])

    print ("")
        
commands = {
    "createnet" : createNetwork,
    "exit" : None,
    "loadnet" : loadNetwork
    }

if __name__ == "__main__":
    startNewCustomSession()


