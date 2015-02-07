#
#  NAME
#    problem_set1.py
#
#  DESCRIPTION
#    Open, view, and analyze raw extracellular data
#    In Problem Set 1, you will write create and test your own spike detector.
#

import numpy as np
import matplotlib.pylab as plt

def load_data(filename):
    """
    load_data takes the file name and reads in the data.  It returns two 
    arrays of data, the first containing the time stamps for when they data
    were recorded (in units of seconds), and the second containing the 
    corresponding voltages recorded (in units of microvolts - uV)
    """
    data = np.load(filename)[()];
    return np.array(data['time']), np.array(data['voltage'])
    
def bad_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTime - all the times where a spike (action potential) was detected
         
    This function is bad at detecting spikes!!! 
        But it's formated to get you started!
    """
    
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        APTimes = []
        return APTimes
    
    numAPs = np.random.randint(0,len(time))//10000 #and this is why it's bad!!
 
    # Now just pick 'numAPs' random indices between 0 and len(time)
    APindices = np.random.randint(0,len(time),numAPs)
    
    # By indexing the time array with these indices, we select those times
    APTimes = time[APindices]
    
    # Sort the times
    APTimes = np.sort(APTimes)
    
    return APTimes
    
def good_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTime - all the times where a spike (action potential) was detected
    """
 
    APTimes = []
       
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        return APTimes
    
    ##Your Code Here!
    spike_th= 0.5*max(voltage) ## spikes must be at least 50% of maximum voltage
    spikes=list(time[voltage>spike_th])
    
    spikes=[[y for y in spikes if abs(y-x)<0.001] for x in spikes]
    
    def uniq(lst):
        last = object()
        for item in lst:
            if item == last:
                continue
            yield item
            last = item
    spikes=uniq(spikes)
    APTimes=[elem[(len(elem)-1)/2] for elem in spikes]
        
    
    return APTimes
    

def get_actual_times(dataset):
    """
    Load answers from dataset
    This function takes the following input:
        dataset - name of the dataset to get answers for

    This function returns the following output:
        APTimes - spike times
    """    
    return np.load(dataset)
    
def detector_tester(APTimes, actualTimes):
    """
    returns percentTrueSpikes (% correct detected) and falseSpikeRate
    (extra APs per second of data)
    compares actual spikes times with detected spike times
    This only works if we give you the answers!
    """
    
    JITTER = 0.025 #2 ms of jitter allowed
    
    #first match the two sets of spike times. Anything within JITTER_MS
    #is considered a match (but only one per time frame!)
    
    #order the lists
    detected = np.sort(APTimes)
    actual = np.sort(actualTimes)
    
    #remove spikes with the same times (these are false APs)
    temp = np.append(detected, -1)
    detected = detected[plt.find(plt.diff(temp) != 0)]
 
    #find matching action potentials and mark as matched (trueDetects)
    trueDetects = [];
    for sp in actual:
        z = plt.find((detected >= sp-JITTER) & (detected <= sp+JITTER))
        if len(z)>0:
            for i in z:
                zz = plt.find(trueDetects == detected[i])
                if len(zz) == 0:
                    trueDetects = np.append(trueDetects, detected[i])
                    break;
    percentTrueSpikes = 100.0*len(trueDetects)/len(actualTimes)
    
    #everything else is a false alarm
    totalTime = (actual[len(actual)-1]-actual[0])
    falseSpikeRate = (len(APTime) - len(actualTimes))/totalTime
    
    print 'Action Potential Detector Performance performance: '
    print '     Correct number of action potentials = ' + str(len(actualTimes))
    print '     Percent True Spikes = ' + str(percentTrueSpikes)
    print '     False Spike Rate = ' + str(falseSpikeRate) + ' spikes/s'
    print 
    return {'Percent True Spikes':percentTrueSpikes, 'False Spike Rate':falseSpikeRate}
    
    
def plot_spikes(time,voltage,APTimes,titlestr):
    """
    plot_spikes takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the raw voltage signal
    and indicating the location of detected spikes with red tick marks (|)
    """
    plt.figure()
    ##Your Code Here    
    plt.plot(time,voltage,'b')
    ymark=np.ones(len(APTimes))*(max(voltage)+8)
    plt.plot(APTimes,ymark,'r|')
    plt.xlabel("Time(s)")
    plt.ylabel("Voltage(uV)")
    plt.title(titlestr)
    ## End of my code
    plt.show()
    
def plot_waveforms(time,voltage,APTimes,titlestr):
    """
    plot_waveforms takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the waveforms for each
    detected action potential
    """
   
    plt.figure()
   
    ## Your Code Here   
    for spike in APTimes:
        l_index=plt.find(time<=spike-0.003)
        l_i=l_index[len(l_index)-1]
        
        h_index=plt.find(time<=spike+0.003)
        h_i=h_index[len(h_index)-1]
        
        ts=time[range(l_i,h_i)]-spike
        vs=voltage[range(l_i,h_i)]
        plt.plot(ts,vs,'b')
        plt.xlim(-0.003,0.003)
                
    plt.xlabel("Time(s)")
    plt.ylabel("Voltage (uV)")  
    plt.title(titlestr)          
    plt.show()
    

        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    ctl = 'y'
    while ctl == 'y' :  
       signal= raw_input("Please input signal file: ")
       print "You entered: ", signal
       
       signalFile=signal+'.npy'
       t,v = load_data(signalFile)    
       actualTimes = get_actual_times(signalFile)
    #  APTime = bad_AP_finder(t,v)
       APTime = good_AP_finder(t,v)
       plot_spikes(t,v,APTime,'Action Potentials in '+signal+' Signal ')
       plot_waveforms(t,v,APTime,'Waveforms in '+signal+' Signal ')
 #      detector_tester(APTime,actualTimes)
       ctl=raw_input("Do you want continue (y/n)? ")
 
    print "Good bye!"
    
 
