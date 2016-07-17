import pickle
import os

import mnist
from random import randint, random
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork

def setupDataSet(dataset = mnist.trainingSet):
    global ds
    """ Construct a SupervisedDataSet from a list of 'mnist.number's """

    ds = SupervisedDataSet(784, 10) #784 inputs, 10 outputs

    for sample in dataset[:5000]:
        #Convert the number to a network output (Ex 5 -> [0,0,0,0,0,10,0,0,0,0])
        output = [0 for i in range(10)]
        output[sample.number] = 10

        inpt = []
        #Convert the image matrix to a list of values
        for row in sample.imageData:
            newRow = [float(no) for no in row] #Convert everything to floats
            inpt += newRow

        ds.addSample(inpt, output) #Add the samples to the dataset
            
class netObj:
    global ds
    
    def __init__(self, hiddenLayers):
        """ Construct a feedfoward network with 784 input neurons, 10 output neurons, and a specified number of hidden layers """

        #Create a network (there must be a better way than this)
        if len(hiddenLayers) == 0:
            self.network = buildNetwork(784, 10) #Set up an RBM if needed
            
        else:
            self.cmdString = "784, " + ", ".join(str(x) for x in hiddenLayers) + ", 10"
            self.network = eval("buildNetwork(" + self.cmdString + ")")

        #Store this for breeding later on
        self.geneticData = hiddenLayers
        self.trainingPerformance = [] #Store MSEs and training iterations

    def train(self, tolerance = 0.05, verbose = False, timeout=20, window = None): #The timeout makes sure that bad networks aren't trained for too long
        """ Train on mnist.trainingSet """
        
        self.tolerance = tolerance      #Store the tolerance in case it's needed later

        #Set up some variables
        MSE = tolerance + 1
        trainer = BackpropTrainer(self.network, ds) #  <--- Look here for memory issues

        iterations = 0
        
        #Train until it's MSE is within the tolerance
        while MSE > tolerance:
            try:
                MSE = trainer.train()
                
                if window:
                    window.trainingPercentage += 100.0/float(window.trainingTimeout)
                    window.currentMSE = MSE
                    window.update()
                
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            
            self.trainingPerformance.append(MSE) #Record for graphing later
            
            iterations += 1
            
            if verbose:
                print "MSE:", MSE

            if iterations >= timeout:
                print "Training timeout"
                break

        return MSE

    def evaluate(self):
        #Use mnist.validationSet to check the network
        self.fitness = []

        #Check the network on the validation set
        for testObject in mnist.validationSet:
            
            #Convert the image data to something the network can take
            targetFormat = []
            for row in testObject.imageData:
                targetFormat += list(row)
            

            networkOutput = self.network.activate(targetFormat)     #What the network thinks the digit is
            correctOutput = testObject.activation                           #What the network should think the digit is
            
            self.fitness.append(_compareLists(correctOutput, networkOutput))     #Compare the two outputs

        #Return the average fitness value (lower is better)
        return sum(self.fitness)/len(self.fitness)
    
    def activate(self, imageData):
        """ Activate the network on an image """
        #Convert the image data to something the network can take
        targetFormat = []
        for row in imageData:
            targetFormat += list(row)

        networkOutput = list(self.network.activate(targetFormat))
        bestGuess = networkOutput.index(max(networkOutput))

        print "Best guess is", bestGuess
        return bestGuess

    def save(self, path):
        existingFiles = sorted(os.listdir(path), key=_getNumber) #Find out what networks have already been saved
        
        if len(existingFiles) != 0:
            networkNumber = int(existingFiles[-1].split(" ")[-1]) + 1 #Get the number for this network
        else:
            networkNumber = 0

        path += "/Network " + str(networkNumber) + "/"
        self.path = path
        os.mkdir(path)

        f = open(path + "network.pkl", 'wb')
        pickle.dump(self, f) #Save the network
        f.close()

    def update(self):
        try:
            self.path = self.path
        except NameError:
            print "Cannot update saved network.  The network was never saved in the first place"
            return
        
        f = open(self.path + "network.pkl", 'wb')
        pickle.dump(self, f) #Save the network
        f.close()
        
    def saveSimple(self, path, networkName):
        f = open(path + "/" + networkName + ".net", 'wb')
        pickle.dump(self, f)
        f.close()

    def visualCheck(self):
        raw_input("Hit enter to view the next image, CTRL-C to quit")

        try:
            #Check the network on the validation set
            for testObject in mnist.testSet:
                
                #Convert the image data to something the network can take
                targetFormat = []
                for row in testObject.imageData:
                    targetFormat += list(row)
                

                networkOutput = self.activate(testObject.imageData)     #What the network thinks the digit is
                testObject.display()

                raw_input("")
                
        except KeyboardInterrupt:
            return


def breedNetworks(maleNet, femaleNet, bias = 0.5, P_mutate = 0.15, maxMutateVal = 10, P_randomAddition = 0.05, P_randomSubtraction = 0.05, P_addNewLayers = 0.1):
    """
    Breed two networks together and return a child network

    bias - How much the building algorithm is biased towards the male (or longer) parent [1 is more biased than 0, 0.5 is even]
    P_mutate - Probability of a mutation occuring
    maxMutateVal - Largest value a mutation will assign
    P_randomAddition - Probability of a random layer being added on
    P_randomSubtraction - Probability of a layer being deleted
    P_addNewLayers - Probability of a child receiving layers from the longer parent
    """

    #We don't need the entire network, just the hidden layers
    male = maleNet.geneticData
    female = femaleNet.geneticData

    if len(male) < len(female):
        #Female is longer, so put it in member_1
        member_1 = female
        member_2 = male

    else:
        #Either the male is longer, or it doesn't matter
        member_1 = male
        member_2 = female

    child = [] #Set up the child list

    #Iterate through the longer list in order to build the child
    for ind in range(len(member_1)):
        if ind < len(member_2):

            #Choose from member_1
            if random() < bias:
                child.append(member_1[ind])

            #Choose from member_2
            else:
                child.append(member_2[ind])
                
        else:
            #If we have run out of indices in member_2, either add a layer from member_1 or do nothing

            if random() < P_addNewLayers:
                child.append(member_1[ind])


    #Now that the child has been built, apply some mutations (if necessary)
    if random() < P_mutate:
        indToMutate = randint(0, len(child) - 1)
        value = randint(0, maxMutateVal)
        child[indToMutate] = value

    #Introduce the possibility of new, random layers being added
    if random() < P_randomAddition:
        child.append(randint(0, maxMutateVal))

    #Introduce the possibility of layer deletion
    if random() < P_randomSubtraction:
        del child[randint(0, len(child) - 1)]

    #Remove zeros
    for no in range(len(child) - 1):
        if child[no] == 0:
            del child[no]
        
    childObj = netObj(child)    #Create a network object from the child's dimensions

    return childObj

def _compareLists(listA, listB):
    try:
        a = [float(x)/max(listA) for x in listA]
        b = [float(x)/max(listB) for x in listB]
        
    except ZeroDivisionError:
        print "Bad formatting - list comparison failed"
        return 10000.0
    
    similarity = sum([abs(b[i] - a[i]) for i in range(len(listA))])/len(listA) * 1.0

    return similarity

def _createPath(run_number, iteration_number, network_number):
    return "./Data/Run " + str(run_number) + "/Iteration " + str(iteration_number) + "/Network " + str(network_number) + "/network.pkl"

#Extract the number from strings like 'Network 23'
def _getNumber(string):
    return int(string.split(" ")[-1])

def createMember(hiddenLayers = randint(0,10), maxLayerSize = 256):
    hiddenLayers = [randint(0, maxLayerSize) for x in range(hiddenLayers)]
    network = netObj(hiddenLayers)

    return network

def createPopulation(popSize, hiddenLayers = randint(0,256), maxLayerSize = randint(0,10)):
    pop = [createMember(hiddenLayers, maxLayerSize) for x in range(popSize)]
    return pop

def loadNetwork(path, run_number=None, iteration_number=None, network_number=None):
    """ Load up a network from a stored file """

    if run_number and iteration_number and network_number:
        path = _createPath(run_number, iteration_number, network_number)
        
    return pickle.load(open(path))

"""
a = netObj([91,45])
a.assignDataSet()
a.train(2, True)
#a.train(2, True)
"""
#b = netObj([])
setupDataSet()
#b.activate(mnist.trainingSet[0].imageData)
"""
c = [0,0,0,1,0,0]
d = [0,4,0,-1,0,0]
print _compareLists(c,d)
"""
