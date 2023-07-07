import numpy as np
from scipy.signal import find_peaks
from scipy.signal import lfilter

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

#return a list of the indexes of the n largest values above a minimum value in a list
def find_n_largest_indexes(list, n, minimumSize):
    indexes = []
    sortedSet = sorted(list, reverse=True)  #sorts the list from largest to smallest
    if len(list) <= n:                 #if there are less items in the list than largest values to find
        for i in range(0, len(list)):  
            indexes.append(i)          #add all indexes to the indexes list
    else:                                                         #otherwise
        for i in range(n):
            indexes.append(np.where(list == sortedSet[i])[0][0])  #find and add the indexes of the first n largest to the indexes list

    #remove values below the minimum size
    deleted = 0  #keeps track of how many have been removed
    for i in range(len(indexes)):
        if list[indexes[i - deleted]] < minimumSize:
            indexes = np.delete(indexes, i - deleted)  #remove the indexes, taking into account how many have been deleted
            deleted += 1
    return indexes  #can also return sortedSet[:n] to get the largest values and not just their indexes

def get_peaks_x_y(data, maxNumberOfPeaks, minPeakSize, filterLevel):  #filter level of 1 means no filter
    b = [1.0 / filterLevel] * filterLevel
    a = 1
    filteredData = lfilter(b, a, data)  #filter the data to try and make the peak finder better
    peaks, properties = find_peaks(normalise_data(filteredData), width = 0, height=0) #returns a list of the indexes of the peaks and a dictionary of their properties
    #calculate a relative size to compare with other peaks, used to find the n largest peaks
    peakSizes = ((properties['peak_heights'] - properties['width_heights'])*100) * (properties['widths'] / len(filteredData)) * 1000   #*100 to make height more important than width, *1000 so that the relative size is more user friendly to change
    largestPeakIndexes = find_n_largest_indexes(peakSizes, maxNumberOfPeaks, minPeakSize)
    return peaks[largestPeakIndexes], data[peaks][largestPeakIndexes]   #peaks[largestPeakIndxexs] is the index of peaks in the data (so 0-2199), data[peaks][largestPeakIndexes] is the data values (y_data) of the peaks