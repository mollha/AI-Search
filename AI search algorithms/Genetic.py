import random
#<- - - - - - - - - - - - - - READ IN DATA - - - - - - - - - - - - - - - - ->
with open('NEWAISearchfile012.txt') as cityFile:
    dataString = cityFile.read()                            #reads the file and stores as a string in the variable dataString
    index = dataString.find('SIZE')+7                       #finds the index of the first character after 'SIZE = ' (the first digit describing the size of the file)
    digitString = ""                                        #initialise digitstring as an empty string - this will eventually contain the numberOfCities
    while dataString[index].isdigit():                      #checks to see if the character is a number
        digitString += dataString[index]                    #appends the character to the end of digitString
        index += 1                                          #increments the variable index so that the next character can be checked
    numberOfCities = int(digitString)                       #turns the string into an integer and asssigns it to numberOfCities
    maxSublistSize = numberOfCities - 1                     #maxSublistSize initialised at the number of cities -1
    dataString = dataString[index+1:]                       #removes the unneccessary section of the string
    storedValue = ""                                        #initialise stored value as an empty string
    sublistLength = 0                                       #initialise sublistLength at 0
    distanceSublist = []                                    #initialise distanceSublist as an empty list
    distanceList = []                                       #initialise distanceList as an empty list, this will eventually contain the data in a nested list
    
    for character in dataString:                            #iterates through each character in the file after 'SIZE = '
        if character.isdigit():                             #if the character is a digit, we want to add this to storedValue
            storedValue += character                        #adds the character to stored value (using a string instead of an int so that we keep the value of the number)
        elif storedValue and character == ',':              #string is not empty and the character is a comma - we have the final value of the distance (between two commas)
            distanceSublist.append(int(storedValue))        #append the integer value of the distance to the sublist
            storedValue = ""                                #resets stored value to an empty string
            sublistLength += 1                              #increment the length of the sublist (storing this means we do not have to use len() repeatedly)
            if sublistLength == maxSublistSize:             #if we have reached the maximum length
                maxSublistSize -= 1                         #decrease maxSublistSize by 1
                sublistLength = 0                           #reset sublist length to 0
                distanceList.append(distanceSublist[:])     #add a copy of the sublist to list
                distanceSublist.clear()                     #clear the sublist
    if storedValue:                                         #if stored value is non empty
        distanceSublist.append(int(storedValue))            #append the integer value of the distance to the sublist
        distanceList.append(distanceSublist[:])             #append the sublist to the list
    cityFile.close()                                        #close the file
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->


#<- - - - - - - - - - - - - - - - FUNCTIONS - - - - - - - - - - - - - - - ->
#<---------- Returns the distance between two cities ----------->
def getDistance(city1, city2):
    if city1 != city2:                                                      #if cities are distinct
        minCity = min(city1, city2)                                         #assign the smallest city to minCity
        return distanceList[minCity-1][max(city1,city2)-minCity-1]          #return the distance between the cities
    else:
        return 0                                                            #return 0 if the cities provided are the same
#<-------------------------------------------------------------->

#<----------- Returns the length of a complete tour ------------>
def getTourLength(tour):
    tourLength = 0                                                          #initialises the variable tourLength at 0 so that we can increment it's value
    for index in range(0, numberOfCities-1):                                #index takes the values between 0 and the size of the list
        tourLength += getDistance(tour[index], tour[index+1])               #adds the distance from the current city to the next city
    tourLength += getDistance(tour[-1], tour[0])                            #add the distance from the last city to the start city
    return tourLength                                                       #return the length of the tour
#<-------------------------------------------------------------->

#<------- Selects a tour proportionally to its fitness --------->
def selectionProToFitness(normalisedFitness):
    randomVal = random.random()                                             #random value between 0 and 1
    cumulative = 0                                                          #initialises the variable cumulative at 0
    for index, value in enumerate(normalisedFitness):                       #iterates through the list of normalised fitnesses
        cumulative += value                                                 #cumulative is incremented by the value of each normalised fitness
        if cumulative >= randomVal:                                         #until cumulative is greater than or equal to the random value
            return index                                                    #return the index of the chosen tour
#<-------------------------------------------------------------->

#<------------ Controls the size of the population ------------->
def populationSize():
    return 100                                                              #returns a user-defined population size
#<-------------------------------------------------------------->

#<------------ Controls the number of generations -------------->
def numberOfGenerations():
    return 22                                                               #returns a user-defined max generation
#<-------------------------------------------------------------->
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->

#<- - - - - - - - - - - - - - CROSSOVER TECHNIQUES - - - - - - - - - - - - - - - - ->
#<- convert children into valid tours and return the fittest child -> 
def convert(childList):   
    for i in range(0,2):                                                                #i takes the values 0 and 1
        child, otherChild = childList[i], childList[i-1]                                #tours are assigned to variables child and other child
        duplicateIndexes = []                                                           #initialise the list of duplicate indexes as an empty list
        cityList = [0]*numberOfCities                                                   #create a list of length numberOfCities - initialised with zero (a 1 represents that a city appears in the child)
                    
        for index, city in enumerate(child):                                            #for each index and city in a child
            if cityList[city-1] == 1:                                                   #indicates that the city is already in the child
                duplicateIndexes.append(index)                                          #add the city to the list of duplicates
            else:
                cityList[city-1] = 1                                                    #set position to 1 once the city appears in the child

        count = -1                                                                      #count is initially -1
        for dupIndex in duplicateIndexes:                                               #for each duplicate index in the list of duplicate indexes
            while True:
                count+=1                                                                #increment value of count by 1
                altCity = otherChild[count]                                             #alternative city is taken from the other child                                                                #if we have checked every city in the otherChild and still have not replaced all duplicate indexes
                if cityList[altCity-1] == 0:                                            #if the alternative city does not exist in the child already
                    cityList[altCity-1] = 1                                             #mark the city at altCity as already in the child
                    child[dupIndex] = altCity                                           #replace the duplicate city with a new city
                    break                                                               #exit the while loop
    if getTourLength(child) < getTourLength(otherChild):                                #if the length of child is less than otherchild
        return child                                                                    #return child (fittest child)
    else:
        return otherChild                                                               #otherwise return the otherchild which must be fitter
#<------------------------------------------------------------------------------>

#<--- Each city in child is selected from either parent with probability 0.5 --->
def uniformCrossover(tour1, tour2):
    child1 = []; child2 = []                                #initialises children as empty lists
    for index in range(0, numberOfCities):                  #iterate through every position of the tour
        if random.randint(0,1) == 0:                        #pick a number between 0 and 1 with probability 0.5
            child1.append(tour1[index])                     #take the next city in child 1 from tour1
            child2.append(tour2[index])                     #take the next city in child 2 from tour2
        else:
            child1.append(tour2[index])                     #take the next city in child 1 from tour2
            child2.append(tour1[index])                     #take the next city in child 2 from tour1
    return convert([child1, child2])                        #children are converted into valid tours and the fittest child is returned
#<------------------------------------------------------------------------------>

#<------ 1 of more crossover points are selected, segments are alternating ----->
def multipointCrossover(tour1, tour2, noOfPoints):
    indexList = random.sample(range(0, numberOfCities-2), noOfPoints)   #randomly selects n distinct crossover positions
    indexList.sort(); indexList.append(numberOfCities-1)                #sort indexes in ascending order and add the last index to the list
    child1 = []; child2 = []                                            #initialises children as empty lists
    currentIndex = 0                                                    #current index is initially 0 (begign at index 0) - this means that the first segment begins at the first city
    tourList = [tour1, tour2]                                           #adds both tours to a list
    count = 0                                                           #initialises count at 0
    for index in indexList:                                             #for position in the list
        child1 += tourList[count][currentIndex:index+1]                 #add a segment of a tour to child 1
        child2 += tourList[count-1][currentIndex:index+1]               #add a segment from the other tour to child 2
        count = (count+1)%2                                             #this alternates which tour each segement is taken from
        currentIndex = index + 1                                        #current index becomes the next index in the list
    return convert([child1, child2])                                    #children are converted into valid tours and the fittest child is returned
#<------------------------------------------------------------------------------>
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->



#<- - - - - - - - - - - - - - MUTATION METHODS - - - - - - - - - - - - - - - - - ->
#----------------- Sets the probability of a mutation occuring ------------------>
def mutationProbability():
    return 0.02                                                                         #user defined probability of mutation
#<------------------------------------------------------------------------------->

#<---------- Swaps two cities in an existing tour to produce a new one ---------->
def swapMutation(tour):
    indexList = (random.sample(range(0, numberOfCities), 2))                            #randomly selects two positions in the tour so that we can swap the cities in these positions
    length1 = getTourLength(tour)
    tour[indexList[0]], tour[indexList[1]] = tour[indexList[1]], tour[indexList[0]]     #swap two cities in the tour
    length2 = getTourLength(tour)
    if length1 < length2:
        tour[indexList[0]], tour[indexList[1]] = tour[indexList[1]], tour[indexList[0]]
    return tour                                                                         #return the mutated tour  
#<------------------------------------------------------------------------------->

#<------------------- Scrambles a portion of the tour --------------------------->
def scrambleMutation(k,tour):
    scrambleSize = int(k*numberOfCities)                                                #portion of tour that is "scrambled"
    index = random.randint(0,numberOfCities-1)                                          #randomly generate an integer between 0 and numberOfCities-1 - this marks the position in the tour where te scrambled portion ends
    mutList = []                                                                        #initialises variable mutlist as an empty list
    for pos in range(index-scrambleSize, index):                                        #we iterate through each position in the scrambled position, ending at index (the end of the scrambled portion)
        mutList.append(tour[pos])                                                       #append the city in each position to mutList
    random.shuffle(mutList)                                                             #shuffle the cities in the scrambled position
    count = 0                                                                           #initialise variable count at 0, this is used to count through the cities in scrambled portion
    for pos in range(index-scrambleSize, index):                                        #for each position in the scrambled portion of the tour
        tour[pos] = mutList[count]                                                      #replace the city in this position with its shuffled counter part in mutList
        count += 1                                                                      #increment count by 1
    return tour                                                                         #return the mutated tour
#<------------------------------------------------------------------------------>
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->
        

#<- - - - - - - - - - - - - - - - MAIN - GENETIC - - - - - - - - - - - - - - - ->
def Genetic():
    generation = 1                                                      #initialise variable generation at 1 - this keeps track of the number of populations
    
    #<---------- generate an initial population --------->
    population = [];                                                    #population initialised as an empty list
    tour = list(range(1,numberOfCities+1))                              #generates a path traversing cities in consecutive order
    for iteration in range(0,populationSize()):                         #generate the number of tours required to meet the population size
        random.shuffle(tour)                                            #randomly shuffle the list of cities to produce a new tour
        population.append(tour[:])                                      #population is represented as a list of tours, we append the tour to the population
    fittestMember = tour[:]                                             #fittest member is initially a random tour
    minTourLength = getTourLength(tour)                                 #minTourLength initially takes the value of the length of a random tour in the population                                             #
    #<--------------------------------------------------->

    
    while generation < numberOfGenerations():                           #terminates when the generation (number of populations) is a user defined size
        newPopulation = []                                              #new population is initially an empty list
        newPopSize = 0                                                  #new population size is initally 0

    #<--- create list of tour lengths --->
        tourLengthList = []; fitnessSum = 0                             #list containing tour lengths is initally empty, sum of fitnesses is initially 0
        for tour in population:                                         #iterates through each tour in the population
            tourLength = getTourLength(tour)                            #calculate the tour length of each tour
            fitnessSum += tourLength                                    #increment the variable fitnessSum by the tour length
            tourLengthList.append(tourLength)                           #add the new tour length to the list of tour lengths
            if tourLength < minTourLength:                              #keep track of fittest member in population
                minTourLength = tourLength                              #make the smaller tour length the new minimum tour length
                fittestMember = tour[:]                                 #assign a copy of the tour to the variable fittestMember - this now contains the best tour so far
    #<------------------------------------>
                
        #<--- normalise tour lengths for selection-proportional-to-fitness --->
        normalisedFitness = [val / fitnessSum for val in tourLengthList]                    #for each tour length, divide by the fitness sum and assign to a new list of normalised fitnesses
        #<-------------------------------------------------------------------->

        while newPopSize <= populationSize():                                               #repeat as many times as the population size (so that we can 

            #<------- select two individuals indexes  -------->
            member1 = population[selectionProToFitness(normalisedFitness)]                  #select a member of the population
            member2 = population[selectionProToFitness(normalisedFitness)]                  #select another member of the population (could be two of the same)
            #<------------------------------------------------>

            #<------------ crossover and mutate -------------->  
            fittestChild = multipointCrossover(member1, member2, 2)                         #fittest of the children produced in crossover
            if random.random() <= mutationProbability():                                    #generate a random value between 0 and 1, if it is less than or equal to the probability of mutation
                fittestChild = swapMutation(fittestChild)                                   #mutate the fittest child
            #<------------------------------------------------>

            #<------------ add to new population ------------->
            newPopulation.append(fittestChild)                                              #add the fittest child to the new population
            newPopSize += 1                                                                 #increment the value of newPopSize by 1
            #<------------------------------------------------>
            
        population = newPopulation[:]                                                       #population becomes the new population
        generation += 1                                                                     #increment the generation by 1

    #<-- Checks the final population for better tours than the current best -->
    for tour in population:                                                                 #iterate through each tour in the population
        tourLength = getTourLength(tour)                                                    #get the length of the current tour
        if tourLength < minTourLength:                                                      #if this length is better than the current minimum
            minTourLength = tourLength                                                      #replace the current minimum with the length of the new shortest tour
            fittestMember = tour[:]                                                         #assign a copy of the tour to the variable fittest member
    #<------------------------------------------------------------------------>                                           
    print('Length of best tour = '+str(minTourLength))
    return fittestMember
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->

