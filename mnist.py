import pickle
import numpy as np
import pygame
from time import sleep

#Duplicate of the Arduino map function (needed for processing autoencoder data)
def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

class number:
    def __init__(self, imageData, number, isMatrix=True, isAutoEncoderOutput = False):
        if isAutoEncoderOutput:
            for px in range(len(imageData)):
                if imageData[px] < 0:
                    new_px = 0
                else:
                    new_px = imageData[px]
                
                new_px = map(new_px, 0, 1, 0, 100)/100.0

                if new_px > 1: new_px = 1
                imageData[px] = new_px
            
        if not isMatrix:
            #Assume the image is 28px x 28px
            matrix = [(imageData[28 * ind: 28 * (ind + 1)]) for ind in range(28)]
            imageData = matrix

        
        self.imageData = imageData
        self.number = number
        self.activation = [0 for x in range(10)]
        self.activation[number] = 10

    #Display the number in a pygame window
    def display(self):
        #Set up the window
        pygame.init()
        screenSize = 280
        screen = pygame.display.set_mode((screenSize, screenSize))
        pygame.display.set_caption("MNIST Data Display")

        scalar = screenSize / 28 #Set the scalar

        #Zero out the position
        x = 0
        y = 0

        #Run through the data, printing rectangles
        for row in self.imageData:
            for col in row:
                pygame.draw.rect(screen, (int(255 * col), int(255 * col), int(255 * col)), (x, y, scalar, scalar))
                x += scalar #Increment the x value

            #Reset x and increment y
            x = 0
            y += scalar

        #Set up the text
        numberFont = pygame.font.Font(None, 35)
        numberText = numberFont.render(str(self.number), 1, (255,255,255))
        screen.blit(numberText, (5, 5))

        #Make sure the exit button hasn't been pressed
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return None
        
        pygame.display.flip() #Show the image

    #Same as display above, but modified to show output strength
    def display_autoencoder(self):
        #Set up the window
        pygame.init()
        screenSize = 280
        screen = pygame.display.set_mode((screenSize, screenSize))
        pygame.display.set_caption("MNIST Data Display")

        scalar = screenSize / 28 #Set the scalar

        #Zero out the position
        x = 0
        y = 0

        #Run through the data, printing rectangles
        for row in self.imageData:
            for col in row:
                color = (255,255,255)
                
                #If the value is negative, edit the red channel
                if col < 0:
                    col = abs(map(col, -0.1, 0, 255, 0))
                    if col > 255: col = 255
                    if col < 0: col = 0

                    color = (int(col), 0, 0)

                #If the value is positive, edit the green channel
                elif col > 0:
                    col = abs(map(col, 0, 1, 0, 255))
                    if col > 255: col = 255
                    if col < 0: col = 0

                    color = (0, int(col), 0)

                #If the value is exactly zero, edit the blue channel
                else:
                    color = (0,0,200)
                
                    
                pygame.draw.rect(screen, color, (x, y, scalar, scalar))
                x += scalar #Increment the x value

            #Reset x and increment y
            x = 0
            y += scalar

        #Set up the text
        numberFont = pygame.font.Font(None, 35)
        numberText = numberFont.render(str(self.number), 1, (255,255,255))
        screen.blit(numberText, (5, 5))

        #Make sure the exit button hasn't been pressed
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return None
        
        pygame.display.flip() #Show the image

def load_MNIST():
    """Load the MNIST library"""
    global trainingSet, validationSet, testSet
    global images

    #Import and unpickle the MNIST library
    f = open("mnist.pkl", "rb")
    training_set, validation_set, test_set = pickle.load(f)
    f.close()

    #Prepare the images
    trainingImages = get_images(training_set)
    validationImages = get_images(validation_set)
    testImages = get_images(test_set)

    trainingSet = []
    validationSet = []
    testSet = []

    #Process the images from training set
    for img in range(len(trainingImages)):
        trainingSet.append(number(trainingImages[img], training_set[1][img]))

    #Process the images from the validation set
    for img in range(len(validationImages)):
        validationSet.append(number(validationImages[img], validation_set[1][img]))

    #Process the images from the test set
    for img in range(len(testImages)):
        testSet.append(number(testImages[img], test_set[1][img]))

    return trainingSet, validationSet, testSet

"""
The following function is based on Michael Nielsen's code for displaying 
MNIST digits.  The code can be found at the following URL:
https://github.com/colah/nnftd/blob/master/fig/chap3/mnist.py
"""
def get_images(training_set):
    """ Return a list containing the images from the MNIST data
    set. Each image is represented as a 2-d numpy array."""
    flattened_images = training_set[0]
    numpyArrays = [np.reshape(f, (-1, 28)) for f in flattened_images]
    
    return numpyArrays

def showDatasetSample(sample):
    value = list(sample[1]).index(1)              #Transform network outputs to numbers [0,0,1,0,0,0,0,0,0,0] -> 2
    tmp = number(sample[0], value, False)   #Create a temporary number object
    tmp.display()                           #Display the object

def dramaticShowAll(ds):
    for img in ds:
        img.display()
        sleep(0.5)
        
load_MNIST()
#dramaticShowAll(testSet)
