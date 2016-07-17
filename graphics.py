import pygame

class Colors():
    black = (0,0,0)
    white = (255,255,255)
    gray = (127, 127, 127)
    lightgray = (240, 240, 240)
    
    red = (255, 0, 0)
    green = (0,255,0)
    blue = (0,0,255)

    orange = (225, 115, 0)
    yellow = (225, 225, 0)
    navy = (0, 0, 180)
    
class StatusWindow():
    #Percentage progress indicators
    overallPercentage = 0.0
    popPercentage = 0.0
    popSize = 100.0
    trainingPercentage = 0.0
    trainingTimeout = 0.0

    #Current network training indicators
    startMSE = 5.0
    currentMSE = 2.0
    lastMSE = 1.0
    targetMSE = 2.0
    percentImprovement = 0.0

    #Population Information
    currentGrade = 1.0
    lastGrade = 1.0
    overallPercentImprovement = 0.0

    status_report = ""
    iterationNumber = 0
    
    def __init__(self, iterations, popSize, trainingTimeout=15, trainingTarget=2):
        pygame.init()
        size = width, height = 1000, 600
        self.screen = pygame.display.set_mode(size)
        self.targetMSE = trainingTarget
        
        self.screen.fill(Colors.white)
        pygame.display.flip()
        
        pygame.display.set_caption("Genetic Algorithm Neural Network Status Window")

    def update(self):
        percentImprovement = ((self.startMSE - self.currentMSE) / self.startMSE) * 100.0
        error = self.currentMSE - self.targetMSE
        
        #Update the display
        pygame.event.get()

        #Set up some text stuff
        fontSize = 33
        bigFontSize = 50
        biggestFontSize = 75
        font = pygame.font.Font(None, fontSize)
        bigFont = pygame.font.Font(None, bigFontSize)
        biggestFont = pygame.font.Font(None, biggestFontSize)

        #Draw percentage indicator backgrounds
        pygame.draw.rect(self.screen, Colors.lightgray, (77,102,67,398))
        pygame.draw.rect(self.screen, Colors.lightgray, (222,102,67,398))
        pygame.draw.rect(self.screen, Colors.lightgray, (367,102,67,398))

        #Draw percentage indicator fills
        pygame.draw.rect(self.screen, Colors.green, (77,102 + (398 * (1 - self.overallPercentage/100)),67,398 * (self.overallPercentage/100)))
        pygame.draw.rect(self.screen, Colors.navy, (222,102 + (398 * (1 - self.popPercentage/100)),67,398 * (self.popPercentage/100)))
        pygame.draw.rect(self.screen, Colors.red, (367,102 + (398 * (1 - self.trainingPercentage/100)),67,398 * (self.trainingPercentage/100)))

        #Draw percentage indicator borders
        pygame.draw.rect(self.screen, Colors.gray, (75,100,70,400), 2)
        pygame.draw.rect(self.screen, Colors.gray, (220,100,70,400), 2)
        pygame.draw.rect(self.screen, Colors.gray, (365,100,70,400), 2)

        #Draw percentage indicator labels
        overallLabel = font.render("Overall Progress", 1, Colors.black)
        popLabel = font.render("Population Progress", 1, Colors.black)
        trainingLabel = font.render("Training Progress", 1, Colors.black)
        
        self.screen.blit(pygame.transform.rotate(overallLabel, 90), (45, 220))
        self.screen.blit(pygame.transform.rotate(popLabel, 90), (188, 190))
        self.screen.blit(pygame.transform.rotate(trainingLabel, 90), (337, 200))

        #Draw percentage indicator levels
        overallLevel = font.render(str(self.overallPercentage)[:5] + "%", 1, Colors.black)
        popLevel = font.render(str(self.popPercentage)[:5] + "%", 1, Colors.black)
        trainingLevel = font.render(str(self.trainingPercentage)[:5] + "%", 1, Colors.black)
        
        self.screen.blit(overallLevel, (77, 510))
        self.screen.blit(popLevel, (222, 510))
        self.screen.blit(trainingLevel, (367, 510))

        #Network-specific labels
        networkStats_label = bigFont.render("Network - Specific Statistics", 1, Colors.black)
        self.screen.blit(networkStats_label, (470, 60))
        
        #Current MSE
        currentMSE_label = font.render("Current MSE", 1, Colors.black)
        currentMSE_status = bigFont.render(str(self.currentMSE)[:4], 1, Colors.black)
        
        self.screen.blit(currentMSE_label, (500, 110))
        self.screen.blit(currentMSE_status, (550, 160))
        
        #Target MSE
        currentMSE_label = font.render("Target MSE", 1, Colors.black)
        currentMSE_status = bigFont.render(str(self.targetMSE)[:4], 1, Colors.black)
        
        self.screen.blit(currentMSE_label, (660, 110))
        self.screen.blit(currentMSE_status, (710, 160))
        
        #Error
        currentMSE_label = font.render("Error", 1, Colors.black)
        currentMSE_status = bigFont.render(str(self.currentMSE - self.targetMSE)[:4], 1, Colors.black)
        
        self.screen.blit(currentMSE_label, (840, 110))
        self.screen.blit(currentMSE_status, (840, 160))

        #Percentage improvement
        percentImprovement = ((self.lastMSE - self.currentMSE) / self.lastMSE) * 100.0
        self.lastMSE = self.currentMSE
        percentImprovement_label = font.render("Percentage Improvement", 1, Colors.black)
        
        if percentImprovement > 0:
            percentImprovement_status = biggestFont.render("+" + str(percentImprovement)[:5] + "%", 1, Colors.green)
            
        elif percentImprovement < 0:
            percentImprovement_status = biggestFont.render(str(percentImprovement)[:5] + "%", 1, Colors.red)
            
        else:
            percentImprovement_status = biggestFont.render(str(percentImprovement)[:5] + "%", 1, Colors.black)
            
        self.screen.blit(percentImprovement_label, (590, 240))
        self.screen.blit(percentImprovement_status, (660, 280))
        
        
        #Overall statistics labels
        overallStats_label = bigFont.render("Overall Statistics", 1, Colors.black)
        self.screen.blit(overallStats_label, (570, 390))

        #Overall grade
        grade_label = font.render("Grade", 1, Colors.black)
        grade_status = bigFont.render(str(self.currentGrade)[:4], 1, Colors.black)
        
        self.screen.blit(grade_label, (520, 440))
        self.screen.blit(grade_status, (530, 470))
        
        #Overall error
        error_label = font.render("Error", 1, Colors.black)
        error_status = bigFont.render(str(self.currentGrade - self.targetMSE)[:4], 1, Colors.black)
        
        self.screen.blit(error_label, (680, 440))
        self.screen.blit(error_status, (690, 470))
        
        #Overall improvement
        overallPercentImprovement = ((float(self.lastGrade) - float(self.currentGrade)) / float(self.lastGrade)) * 100.0
        self.lastGrade = self.currentGrade
        overallPercentImprovement_label = font.render("Improvement", 1, Colors.black)
        
        if overallPercentImprovement > 0:
            overallPercentImprovement_status = bigFont.render("+" + str(overallPercentImprovement)[:5] + "%", 1, Colors.green)
            
        elif overallPercentImprovement < 0:
            overallPercentImprovement_status = bigFont.render(str(overallPercentImprovement)[:5] + "%", 1, Colors.red)
            
        else:
            overallPercentImprovement_status = bigFont.render(str(overallPercentImprovement)[:5] + "%", 1, Colors.black)
            
        #overallPercentImprovement_status = bigFont.render(str(self.currentMSE - self.targetMSE)[:4], 1, Colors.black)
 
        self.screen.blit(overallPercentImprovement_label, (800, 440))
        self.screen.blit(overallPercentImprovement_status, (830, 470))

        #Draw the status report
        status_report_text = font.render("Status:    " + self.status_report, 1, Colors.black)
        self.screen.blit(status_report_text, (30, 570))

        #Draw the iteration number
        iterationNumber_text = font.render("Iteration " + str(self.iterationNumber), 1, Colors.black)
        self.screen.blit(iterationNumber_text, (30, 30))
        
        pygame.display.flip()
        self.screen.fill(Colors.white)

    #Display the most recent important event
    def statusReport(self, report):
        self.status_report = report
        self.update()

    #Kill the graphical display
    def kill(self):
        print "Graphics stopping"
        pygame.quit()

#a = StatusWindow(1,1,1)
#a.update()
#raw_input("waiting")
#pygame.quit()
