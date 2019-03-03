#Dylan Waters
#Assignment 3
#CS 3580 with Dr. Ball

#imports
import numpy
import csv
import matplotlib.pyplot as plt
import pandas
# from scipy import stats
from random import randint

#print my name!
print("Dylan Waters")
print("")

#lists to hold various data for later sections
countryList = []
chocolateRating = []
countryRatingList = []
cocoaPercent = []
cocoaPercentVsRating = []
companyName = []
beanOriginAndRating = []

#open and read the file
with open("flavors_of_cacao.csv") as datafile:
    output = csv.reader(datafile, delimiter=",")
    next(output) #skip first row

    for row in output:
        countryList.append(row[5])
        chocolateRating.append(float(row[6]))
        countryRatingList.append( (row[5], float(row[6])) )
        cocoaPercent.append(float(row[4].replace("%","")))
        companyName.append(row[0])
        #bean origin needs to check the strings a bit
        if(row[8] != "\xa0" and row[8] != ""):
            beanOriginAndRating.append( (row[8], float(row[6])) )


#gets a list of the average rating for each country
countryRatingList.sort()
currentCountryString = ""
currentCountryRatingSum = 0
currentCountryRatingCount = 0
#the avg list
avgRatingList = []
#for each tuple in the country rating list, compound the rating for each country
for pair in countryRatingList:
    if(currentCountryString == ""):
        currentCountryString = pair[0]
        currentCountryRatingSum = pair[1]
        currentCountryRatingCount = 1
        continue
    if(pair[0] == currentCountryString):
        currentCountryRatingSum += pair[1]
        currentCountryRatingCount += 1
        continue
    #on a new country, this means one country is done
    if(pair[0] != currentCountryString):
        #appends the country and the avg rating, then resets for the next country
        avgRatingList.append( (currentCountryString, currentCountryRatingSum / currentCountryRatingCount) )
        currentCountryString = pair[0]
        currentCountryRatingSum = pair[1]
        currentCountryRatingCount = 1
        continue

#prints the top five countries
avgRatingList.sort(key=lambda tup: tup[1], reverse = 1)
print("Top Countries:")
for i in range(0,5):
    print(avgRatingList[i])
print("")

#count of the ratings, get mode rating while we're at it
chocRateMode = 0
modeCnt = 0
ratingList = []
ratingCountList = []
print("Number of each rating:")
for i in numpy.arange(5.0, 0.0, -0.25):
    #prints a count for each rating in .25 increments
    print(i, end=": ")
    print(chocolateRating.count(i))
    ratingList.append(i)
    ratingCountList.append(chocolateRating.count(i))
    #gets the mode chocolate rating, used in the univariate stats section
    if(chocolateRating.count(i) > modeCnt):
        chocRateMode = i
        modeCnt = chocolateRating.count(i)
print("")
print("displaying graph...")

plt.figure(3)
plt.bar(ratingList, ratingCountList, 1/1.5)
plt.suptitle("Count of each chocolate rating")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

#univariate stats
#starting with chocolateRating
chocRateMean = 0
#compounds chocolate rating and divides by the total elements
for i in range(0, len(chocolateRating)):
    chocRateMean += chocolateRating[i]
chocRateMean = chocRateMean/len(chocolateRating)
print("Mean chocolate rating: " + str(chocRateMean))
#we got the mode earlier
print("Mode chocolate rating: " + str(chocRateMode))

#sorts the list and gets the middle value
#make sure to copy by value this list!
chocRateSorted = list(chocolateRating)
chocRateSorted.sort()
medianChocRate = chocRateSorted[int(len(chocRateSorted)/2)]
print("Median chocolate rating: " + str(medianChocRate))
print("")

#cocoaPercent
#mean is same as above algorithm for chocolate rating mean
cocoaPercentMean = 0
for i in range(0, len(cocoaPercent)):
    cocoaPercentMean += cocoaPercent[i]
cocoaPercentMean = cocoaPercentMean/len(cocoaPercent)
print("Mean cocoa percent: " + str(cocoaPercentMean))

#loops through cocoaPercents and takes the highest count
cocoaPercentMode = 0
cocoaModeCnt = 0
for i in range(0, 100):
    if(cocoaPercent.count(i) > cocoaModeCnt):
        cocoaPercentMode = i
        cocoaModeCnt = cocoaPercent.count(i)
print("Mode cocoa percent: " + str(cocoaPercentMode))

#sorts the list copying by value, and then finds the middle value
cocoaPercentMedian = 0
cocoaPercentSorted = list(cocoaPercent)
cocoaPercentSorted.sort()
cocoaPercentMedian = cocoaPercentSorted[int(len(cocoaPercentSorted)/2)]
print("Median cocoa percent: " + str(cocoaPercentMedian))
print("")

#first correlation
#gets the correlation coefficient
print("Correlation coefficient: ", end="")
print(numpy.corrcoef(cocoaPercent, chocolateRating)[0, 1] )
#describe relationship
print("As the percent of cocoa increases, the chocolate rating tends to be slightly lower")
print("displaying graph...")
#perform linear regression and plot the graph
linReg1 = numpy.polyfit(cocoaPercent, chocolateRating, 1)
linReg1_fn = numpy.poly1d(linReg1)
plt.figure(1)
plt.plot(cocoaPercent, chocolateRating, 'yo', cocoaPercent, linReg1_fn(cocoaPercent), '--k')
plt.suptitle("Correlation between percent cocoa and rating")
plt.ylabel("Rating")
plt.xlabel("Percent cocoa")
plt.show()
print("")

#second correlation
#create a dataframe using pandas
companyVsRatingList = [('company name', companyName),('ratings', chocolateRating)]
df = pandas.DataFrame.from_items(companyVsRatingList)
# get the dummies value for company name
df_dummies = pandas.get_dummies(df['company name'])
#concat the original with the dummies
df_new = pandas.concat([df, df_dummies], axis=1)
#drop the ratings column
df_new = df_new.drop(['ratings'],axis=1)
# get the correlation and store that as a new dataframe
df_corr = df_new.corr()
#gets 5 random numbers for indexes in the dataframe
randNumList = []
# for i in range(0, 5):
#     randNumList.append(randint(0, len(df_corr)-1))

chosenCompNames = ["A. Morin", "Arete", "Dandelion", "Pralus", "Soma"]
listOfUniqueCompNames = df_corr.columns.values
# print(listOfUniqueCompNames)
for j in range(0, 5):
    for i in range(0, len(df_corr)):
        if(df_corr.columns.values[i] == chosenCompNames[j]):
            randNumList.append(i)


#describe the correlation matrix
print("This is the correlation matrix for A. Morin, Arete, Dandelion, Pralus, and Soma.")
print("All of the companies have a negative correlation with their pairs of companies, indicating a general negative trend between ratings for companies")
print("The company Pralus has the 'highest' correlation, which shows it has the largest negative trend compared to other company's ratings")
print("Generally, all the companies have a very small correlation, which indicates that the companies are not correlated")
print("")

#print the randomly chosen company names
print("     ", end ="")
for i in range(0, 5):
    print(df_corr.columns.values[randNumList[i]], end= " -- ")
print(" ")

#find the highest correlation while displaying the matrix
highestCorrelation = 0.0
highestCompString = ""
for i in range(0, 5):
    #prints the row company name
    print(df_corr.columns.values[randNumList[i]], end = " ")
    for j in range(0, 5):
        #prints the value in the dataframe index from the random list
        print(df_corr.values[randNumList[i]][randNumList[j]], end = " ")
        #check to see if this index is the highest correlation
        if(abs(df_corr.values[randNumList[i]][randNumList[j]]) > highestCorrelation and abs(df_corr.values[randNumList[i]][randNumList[j]]) < 1):
            highestCorrelation = abs(df_corr.values[randNumList[i]][randNumList[j]])
            highestCompString = df_corr.columns.values[randNumList[i]]
    print(" ")
print("Company with highest correlation: " + highestCompString + ": " + str(highestCorrelation))

print("displaying graph...")
#display the graph for the highest company
topCompRatings = []
otherCompRatings = []
topCompPercent = []
for i in range(0, len(companyName)):
    #get each rating and cocoa percent for the matching company
    if(companyName[i] == highestCompString):
        topCompRatings.append(chocolateRating[i])
        topCompPercent.append(cocoaPercent[i])
#create the plot and linear regression
linReg2 = numpy.polyfit(topCompPercent, topCompRatings, 1)
linReg2_fn = numpy.poly1d(linReg2)
plt.figure(2)
plt.plot(topCompPercent, topCompRatings, 'bo', topCompPercent, linReg2_fn(topCompPercent), '--k')
plt.suptitle(highestCompString + " Percent Cocoa vs Rating")
plt.xlabel('Percent cocoa')
plt.ylabel('Rating')
plt.show()
print("")

#independent thought
print("Question: What countries produce the best beans according to rating?")
print("To answer this question, I obtained a list of the bean origin country and the rating")
print("I then sorted the list and got an average rating for each country")
print("The top ten countries for bean origins will now be printed out")
print("As always, it's important the data is understood; some of these top countries have only one or a few data points")
beanOriginAndRating.sort()
beanCountries = []
beanRatings = []
beanProviderCount = []
currTuple = beanOriginAndRating[0]
beanCountryStr = currTuple[0]
beanCountryAvgRating = currTuple[1]
currBeanCnt = 1
# loop through the tuples of bean origin and rating getting the avg for each country before appending it to the countries and rating list
for i in range(1, len(beanOriginAndRating)):
    currTuple = beanOriginAndRating[i]
    if(currTuple[0] == beanCountryStr):
        currBeanCnt += 1
        beanCountryAvgRating += currTuple[1]
        continue
    if(currTuple[0] != beanCountryStr):
        beanCountries.append(beanCountryStr)
        beanRatings.append( beanCountryAvgRating/currBeanCnt )
        beanProviderCount.append(currBeanCnt)
        beanCountryStr = currTuple[0]
        beanCountryAvgRating = currTuple[1]
        currBeanCnt = 1
        continue
#create a list of the top origin countries
bestCountryList = []
for i in range(0, len(beanCountries)):
    bestCountryList.append( (beanCountries[i], beanRatings[i], beanProviderCount[i]) )
#sort the list and display the top ten countries
bestCountryList.sort(key=lambda tup: tup[1], reverse = 1)
print("Top Bean Country Origins:")
for i in range(0,10):
    newTup = bestCountryList[i]
    print(i+1, end=": ")
    print(newTup[0] + ": " + str(newTup[1]))
print("")

print("Since there are few entries for those countries, let's find the countries that provide for the highest count of companies")
bestCountryList.sort(key=lambda tup: tup[2], reverse = 1)
print("Top Bean Country Origins:")
for i in range(0,10):
    newTup = bestCountryList[i]
    print(i+1, end=": ")
    print(newTup[0] + ": " + str(newTup[2]))
print("")

print("From this, let's look at countries that provide for at least 30 chocolate bars and find the highest average rating from that")
highCountOfCountries = []
for i in range(0, len(bestCountryList)):
    newTup = bestCountryList[i]
    if(newTup[2] >= 30):
        highCountOfCountries.append(newTup)
highCountOfCountries.sort(key=lambda tup: tup[1], reverse = 1)
print("Countries that provide for at least 30 chocolate bars with the highest ratings: ")
for i in range(0, len(highCountOfCountries)):
    newTup = highCountOfCountries[i]
    print(i+1, end=": ")
    print(newTup[0] + ": " + str(newTup[1]))
