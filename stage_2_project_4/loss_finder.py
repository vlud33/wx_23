import numpy as np

#return the minimum and maximum when given a set of data
def find_min_max(data):
    return min(data), max(data)

#return a normalised set of data (maximum is 1 and the minimum is 0) when given a set of data
def normalise_data(data):
    normalised = data.copy()
    minimum, maximum = find_min_max(data)
    for i in range(len(data)):
        normalised[i] = (data[i]-minimum)/(maximum-minimum)
    return normalised

#returns the percentage increase between two values
def percentage_increase(initialData, finalData):
    if initialData == 0 or finalData == 0:
        percentage = None
    else:
        percentage = ((finalData - initialData) / initialData) * 100 
    return percentage

#calculates the percentage increases between regular points in a set of data
def percentage_increases(data, sampleRate):
    percentages = []
    previousPoint = data[0]
    for i in range(sampleRate, len(data)-sampleRate, sampleRate):
        percentages.append(percentage_increase(previousPoint, data[i]))
        previousPoint = data[i]
    return percentages

#returns a list of indexes of a data list that are below a significance level
def get_significant_data_indexes(data, significance):
    indexes = []
    for i in range(len(data)):
        if data[i]:
            if data[i] < significance:
                indexes.append(i)
    return indexes

#removes consecutive points from a list and just leaves the start and end values in seperate lists
def get_boundary_indexes(indexes):
    startEndIndexes = []
    listCount = 0
    for i in range(len(indexes)):
        if i == 0 or indexes[i] != indexes[i-1] + 1:
            startEndIndexes.append([indexes[i]])
            listCount += 1
        else:
            startEndIndexes[listCount-1].append(indexes[i])
            if len(startEndIndexes[listCount-1]) > 2:
                startEndIndexes[listCount-1].remove(indexes[i-1])
    return startEndIndexes

#takes the index of a value in a data set of dataLength 
def index_to_time(index, dataLength, dataStartTime, dataEndTime):
    time = (index * ((dataEndTime - dataStartTime) / dataLength)) + dataStartTime
    return time

#converts a list of two values of start sampled index and end sampled index and returns their indexes in 
def sampled_indexes_to_data_indexes(sampleIndexes, sampleRate):
    dataIndexes = []
    dataIndexes.append(sampleIndexes[0] * sampleRate)
    if len(sampleIndexes) == 1:
        dataIndexes.append(dataIndexes[0] + sampleRate)
    else:
        dataIndexes.append((sampleIndexes[1] * sampleRate) + sampleRate)
    return dataIndexes

#gets the data of the drop and returns information about it
def quantise_drop(data, dataIndex1, dataIndex2, dataStartTime, dataEndTime):
    startTime = index_to_time(dataIndex1, len(data), dataStartTime, dataEndTime)
    stopTime = index_to_time(dataIndex2, len(data), dataStartTime, dataEndTime)
    percentageDrop = -percentage_increase(data[dataIndex1], data[dataIndex2])
    return startTime, stopTime, percentageDrop

#main function that calls the other functions and finds and displays drops in a set of data
#data (2D array): the y data
#sampleRate (int): the rate at which the data is sampled to find drops
#significanceLevel (negative int): the minumum negative percentage increase that a drop must have in order to qualify as a drop
def find_drops(data, sampleRate, significanceLevel):
    data = normalise_data(data)
    percentages = percentage_increases(data, sampleRate)
    significantIndexes = get_significant_data_indexes(percentages, significanceLevel)
    boundaryIndexes = get_boundary_indexes(significantIndexes)
    drops = []
    for i in range(len(boundaryIndexes)):
        drops.append(sampled_indexes_to_data_indexes(boundaryIndexes[i], sampleRate))
    return drops