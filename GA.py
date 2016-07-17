import os
import pickle
import networkLib
from random import random, randint

#Store all of the paremeters
class EvolutionObject():
    trainingTimeout = 15
    trainingTarget = 2
    popSize = 4
    iterations = 10
    mutate=0.15
    extraParents=0.1
    originalParents=0.15
    
    def __init__(self):
        pass
    
#Get each network to evaluate itself
def judgeNetworkFitness(member, trainFirst = True, numberOfRounds = None):
    if window:
        window.trainingPercentage = 0.0 #Update the number of networks trained
        window.update()
                
    if trainFirst:
        print "Training..."
        window.statusReport("Training network...")
        
        try:
            member.train(evolutionObject.trainingTarget, True, timeout=evolutionObject.trainingTimeout, window = window)
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        
        except:
            print "Training Failure"
            
            if window:
                window.statusReport("Training Failure!  Network rejected")
                window.popPercentage += 100.0/window.popSize #Update the number of networks trained
                window.update()
                
            return 10000

    print "Evaluating..."
    if window: window.statusReport("Evaluating network...")

    fitness = member.evaluate() #Test the network
    
    if window:
        window.popPercentage += 100.0/window.popSize #Update the number of networks trained
        window.update()

    
    return fitness

#Genetic Evolution system for NNs
def evolve(pop, evo_object):
    """Evolve a population by one iteration"""

    #if not popSize: popSize = len(pop)
    #Sort by error (lowest-first)
    #Select breeding group
    #Add in random (lesser performing) members for diversity
    #Refill the population by breeding the breeding group

    popSize = evo_object.popSize
    mutate = evo_object.mutate
    extraParents = evo_object.extraParents
    originalParents = evo_object.originalParents

    if window:
        window.popPercentage = 0.0 #Update the number of networks trained
    
    pop = sorted(pop, key=judgeNetworkFitness)                        #Sort the population by each member's fitness
    parents = pop[:int(len(pop) * (1 - originalParents))]             #Select the parents (the top 15% of the population)
    everyoneElse = pop[int(len(pop) * (1 - originalParents)):]        #The population to select the other members from

    for network in pop: network.update()
        
    grade = 0.0
    for member in pop:
        try:
            grade += (float(member.trainingPerformance[-1])/float(len(pop))) # <------ Statistical error here (maybe)

        except IndexError:
            grade += 0 #Ignore the network's performance
            
    if window:
        window.currentGrade = grade
        window.update()
    
    extraParents = []                    #Parents added randomly (for genetic diversity)
    print "Population sorted"
    if window: window.statusReport("Population sorted")
    
    #Populate extraParents
    for member in everyoneElse:
        if random() < extraParents:
            extraParents.append(member)

    for parent in extraParents:
        parents.append(parent)        #Add the extra parents to the pool of parents

    #Mutate a random selection of members
    for member_idx in range(len(parents)):
        if random() < mutate:
            member = list(parents[member_idx].geneticData)
            
            index_to_mutate = randint(0, len(member) - 1)                   #Number to mutate in member (don't mutate the first number, because it could cause issues with leading zeros)
            number_to_mutate_to = str(range(10)[randint(0, 9)])    #Value to assign to the aforementioned index

            member = list(member)
            member[index_to_mutate] = number_to_mutate_to #Perform the mutation

            parents[member_idx] = networkLib.netObj([int(x) for x in member]) #Adjust the entry in 'parents'
            print "Mutation performed"
            
    #Crossover the parents to create children
    newPop = parents #Initialize the new population with the surviving parents

    identicalParents = 0
    
    #Breed the parents to create enough new children to satisfy popSize
    while len(newPop) < popSize:
        maleParent = parents[randint(0, len(parents) - 1)]      #Select a male parent
        femaleParent = parents[randint(0, len(parents) - 1)]    #Select a female parent

        if identicalParents >= len(parents):
            raise(Exception("All Parents Identical"))
        
        #Skip the parents if they are identical
        if maleParent == femaleParent:
                identicalParents += 1
                continue

        #Create a new child and add it to the population
        newChild = networkLib.breedNetworks(maleParent, femaleParent)
        newPop.append(newChild)

    print "Breeding done"
    if window: window.statusReport("Breeding complete")
    
    return newPop


def continuousEvolution(pop, evo_object, run_number = None, start_iteration_number = 0, graphicsWindow=None):
    global window
    global evolutionObject
    
    window = graphicsWindow
    window.iterationNumber = start_iteration_number
    evolutionObject = evo_object

    if window: window.popSize = evo_object.popSize
    if window: window.trainingTimeout = evo_object.trainingTimeout
    
    #Setup a new session if no run_number has been supplied
    if not run_number:
        run_number = int(sorted(os.listdir("./Data")[1:], key=lambda x: int(x.split(" ")[-1]))[-1].split(" ")[-1]) + 1
        
        """
        #What that (^) line does
         - Gets a list of all files in the directory ./Data     os.listdir("./Data"
         - Sorts the list based on the number after 'Run '      sorted(os.listdir("./Data")[1:], key=lambda x: int(x.split(" ")[-1])
              - Ignore evolution_parameters.pkl
         - Gets the last element and extracts its number        [-1].split(" ")[-1])
         - Increments that number by 1                          + 1
        """

    path = "./Data/Run " + str(run_number) + "/Iteration " + str(start_iteration_number)
    os.makedirs(path)
    
    #Save the evolution parameters
    pickle.dump(evo_object, open("./Data/Run " + str(run_number) + "/evolution_parameters.pkl", 'w'))
    
    print "Saving Networks..."
    if window: window.statusReport("Saving Networks...")
    
    for network in pop: network.save(path)

    run = True
    
    for iteration_number in range(start_iteration_number, evo_object.iterations):
        print "------------- Iteration " + str(iteration_number + 1) + " ------------"
        
        if window:
            window.iterationNumber = iteration_number + 1
            window.statusReport("Iteration "  + str(iteration_number + 1))

        #Report the current percentage complete
        if window:
            window.overallPercentage = (iteration_number / float(evo_object.iterations)) * 100.0
            window.update()
            
        try:
            pop = evolve(pop, evo_object)
            
        except KeyboardInterrupt:
            run = False
            print "Training Stopped"
            if window: window.statusReport("Training Stopped")
        
        print "Saving Networks..."
        if window: window.statusReport("Saving Networks...")
        
        path = "./Data/Run " + str(run_number) + "/Iteration " + str(iteration_number + 1)
        os.makedirs(path)
        for network in pop: network.save(path)

        #Stop if the run flag is set to False
        if not run:
            print "Save complete!"
            if window: window.statusReport("Saving Complete!")
            break

    #Report the current percentage complete
    if window and run:
        window.overallPercentage = 100.0
        window.update()
        window.statusReport("Evolution complete!")
        
if __name__ == "__main__":
    pop = networkLib.createPopulation(4, hiddenLayers = 1, maxLayerSize = 4)
    #newPop = evolve(pop, 5)
    continuousEvolution(pop)
