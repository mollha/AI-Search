import random
import math

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


#<- - - - - - - - - - - - - - - - - - - FUNCTIONS - - - - - - - - - - - - - - - - - - - - >
#<----- controls the temperature of the system ----->
def coolingSchedule(time, currentTemp):
    b = 2
    if time == 0:
        return 1000000000
    return currentTemp/b
#<-------------------------------------------------->

#<----- probability of selecting a worse tour ----->
def probability(temperature, difference):
    return math.exp((-difference*2)/temperature)
#<-------------------------------------------------->

#<----- returns the distance between two cities ---->
def getDistance(city1, city2):
    if city1 != city2:
        minCity = min(city1, city2)
        return distanceList[minCity-1][max(city1,city2)-minCity-1]
    else:
        return 0
#<-------------------------------------------------->
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - >
    

#<- - - - - - - - - - - - - MAIN - SIMULATED ANNEALING - - - - - - - - - - - - - - >
def simulatedAnnealing():
    time = 0                                                                                    #time initialised at 0
    temperature =  coolingSchedule(time, None)                                                  #initial temperature is retrieved
    #<---------------------- generates an intial random tour ---------------------->
    currentState = list(range(1,numberOfCities+1))                                              #generates a path traversing cities in consecutive order
    random.shuffle(currentState)                                                                #shuffles the order of cities in the path
    #<---------------- calculates the length of the initial tour ------------------>
    currentLength = 0                                                                           #initialises the variable currentLength at 0 so that we can increment it's value
    for index in range(0, numberOfCities-1):                                                    #index takes the values between 0 and the size of the array
        currentLength += getDistance(currentState[index], currentState[index+1])                #adds the distance from the current city to the next city
    currentLength += getDistance(currentState[-1],currentState[0])                              #adds the distance from the last city back to the first to find the length of the tour
    #<----------------------------------------------------------------------------->
    
    while temperature > 0:                                                                      #want to continually look for better tours until the temperature is 0
        #<----------------- generates a successor state ------------------->
        indexList = (random.sample(range(0, numberOfCities), 2))                                #randomly selects two positions in the tour so that we can swap the cities in these positions
        indexList.sort()                                                                        #sort these values from lowest to highest
        difference = 0                                                                          #initialise the difference in tour lengths at 0
        for i in range(0,2):                                                                    #i takes the values of 0 and 1 only
            index1 = indexList[i]                                                               #picks one index from the list to focus on for this iteration
            index2 = indexList[i-1]                                                             #the other index becomes index2
            city1 = currentState[index1]                                                        #finds which city is at the current index1
            city2 = currentState[index2]                                                        #finds which other city is being swapped
            prevCity = currentState[index1-1]                                                   #finds which city is behind the city at the specified index in the current best tour
            if index1 != numberOfCities-1:                                                      #checks that the index is not at the end of the array otherwise looking for the next value will produce an error
                nextCity = currentState[index1+1]                                               #finds which city follows the city at the specified index in the current best tour
            else:                                                                               #if the city is at the end of the list
                nextCity = currentState[0]                                                      #next city is the city at the start of the list as we are dealing with a tour

            #<-- calculates the differences in distance for the new tour -->
            if (i==1 or index2-index1 != 1) and (i==0 or index1-index2 != numberOfCities -1):
                difference += getDistance(nextCity,city2) - getDistance(nextCity,city1)
            if (i==0 or index1-index2 != 1) and (i==1 or index2-index1 != numberOfCities -1):
                difference += getDistance(prevCity,city2)- getDistance(prevCity,city1)
        #<----------------------------------------------------------------------->

        #<----------- decides if the successor state will become the current state --------->
        if difference < 0 or random.random() <= probability(temperature, difference):                                               #if difference > 0, new tour is worse therefore keep with certain probability
            currentState[indexList[0]], currentState[indexList[1]] = currentState[indexList[1]], currentState[indexList[0]]         #alter the old tour to the new tour
            currentLength += difference                                                                                             #add the difference to the old tour length to get the length of the new tour
        #<---------------------------------------------------------------------------------->

        #<---------- sets the new time and temperature ---------->
        time += 1                                                       #increment the time
        temperature = coolingSchedule(time, temperature)                #retrieve the new temperature of the system
        #<---------------------------------------------->            
    print('Length of best tour = '+str(currentLength))
    return currentState
#<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - >

