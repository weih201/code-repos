#
#  NAME
#    problem_set4.py
#
#  DESCRIPTION
#    In Problem Set 4, you will classify EEG data into NREM sleep stages and
#    create spectrograms and hypnograms.
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m

from sklearn import  svm,neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB


def load_examples(filename):
    """
    load_examples takes the file name and reads in the data.  It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['examples'], int(data['srate'])

def load_eeg(filename):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['eeg'], int(data['srate'])

def load_stages(filename):
    """
    load_stages takes the file name and reads in the stages data.  It returns an
    array containing the correct stages (one for each 30s epoch)
    """
    data = np.load(filename)
    return data['stages']
    
def extract_psds(examples,rate):
    i_epochs = np.array_split(np.arange(len(examples[0])),10)   ##split 5 minutes to 10 30 sec slice
    l = np.arange(len(examples))    ##the number of data set
    ind_pxx = np.zeros((len(examples),10,257))    ## cumulative power disctribution of sum of ten 30 sec slice
    avg_pxx = np.zeros((len(examples),257))
    ts = 0
    freqs = np.zeros(257)
    for index in i_epochs:
        ts = ts+30
        epochs = examples[:,index]
#        plt.figure()
        for i in l:
            ##YOUR CODE HERE   
#            if i == 0:
#                continue
            Pxx, freqs = m.psd(epochs[i],512,rate)
            Pxx = Pxx/np.sum(Pxx)       ### Normailzation spectrum power 
            max_pxx = np.max(Pxx)       ## Maximum power value
            cumPxx = np.cumsum(Pxx)    ## cumulative power 
            eng_main = cumPxx[8]        ## Main lobe energy (up to 2hz)
            eng_sub =cumPxx[60]-cumPxx[44]  ## sub lobe energy (between 11 to 15 Hz)
            eng_min = cumPxx[40]-cumPxx[24]  ## pwoer energy between 6-10Hz
            
            ind_pxx[i,(ts-30)/30] =  Pxx ## store power distribution
            avg_pxx[i]=avg_pxx[i]+Pxx
            
##            max_pxx_sub = np.max(Pxx[freqs>10])  ## maximum power value in sub-lobe
            bw_indexs = np.where(Pxx>=max_pxx/2) ## half maximum power index
            bw_index = np.max(bw_indexs[0]) - np.min(bw_indexs[0]) ## helf power bandwith
    avg_pxx = avg_pxx/len(i_epochs)
           
    return ind_pxx,avg_pxx, eng_main,eng_sub,eng_min,bw_index, freqs

def plot_example_psds(examples,rate):
    """
    This function creates a figure with 4 lines to show the overall psd for 
    the four sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    ind_pxx,avg_pxx, eng_main,eng_sub,eng_min,bw_index , freqs= extract_psds(examples,rate)
 
    for sampl in ind_pxx:
        plt.figure()
        for epoch in sampl:
            plt.plot(freqs,epoch)   
            plt.xlim(xmax=25)
            plt.ylim(ymax=.2)
#            print 'Pxx maximum: '+str(max_pxx)+' of '+str(i)+' at '+ str(max_freqs)+'Hz'
##            print 'Pxx maximum/Pxx10 Maximum ratio of '+str(i)+' is: '+str(max_pxx*bw_index/max_pxx12)
##            print 'Eng product of mani and sub of  '+str(i)+' is: '+str(eng_main*eng_sub)
##            print 'Eng ratio of main and sub of  '+str(i)+' is: '+str(eng_main/eng_sub)
#        plt.legend(('REM','Stage 1 NREM','Stage 2 NREM','Stage 3/4 NREM'), loc=1)
#        plt.title('The epoch time period between '+str(ts-30)+' to '+str(ts))
#    plt.figure()
#    plt.hist(Pxx,histtype='step')
    plt.figure()
    for pxx in avg_pxx:
        plt.plot(freqs,pxx)
        plt.xlim(xmax=25)
        plt.xlim()
    plt.legend(('REM','Stage 1 NREM','Stage 2 NREM','Stage 3/4 NREM'), loc=1)
    plt.title('Cumulavtive Pxx graph')


def plot_example_spectrograms(example,rate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    ###YOUR CODE HERE
    Pxx, freqs, bins, im = plt.specgram(example,NFFT=512,Fs=rate)    
    plt.xlabel('Time')
    plt.ylabel('Frequencies')
    return
      

def flatten_pxx(ind_pxx):  ## convert pxx from three dim to two dim
    dim = ind_pxx.shape
    stages = np.zeros(dim[0]*dim[1])
    flat_pxx = np.zeros((dim[0]*dim[1],257))
    
    for sampl in np.arange(0,dim[0]):
        for epoch in np.arange(0,dim[1]):
            index = sampl*dim[1]+epoch
            flat_pxx[index]=ind_pxx[sampl,epoch]
            stages[index] = sampl
    
    return flat_pxx,stages
            
def classify_epoch(epoch,rate):
    """
    This function returns a sleep stage classification (integers: 1 for NREM
    stage 1, 2 for NREM stage 2, and 3 for NREM stage 3/4) given an epoch of 
    EEG and a sampling rate.
    """

    ###YOUR CODE HERE
    examples, srate = load_examples('example_stages.npz')
    ind_pxx,avg_pxx, eng_main,eng_sub,eng_min,bw_index , freqs= extract_psds(examples,srate)
  
##  with logistic classification in scklearn  
    samples, stages = flatten_pxx(ind_pxx)
    
    Pxx, freqs = m.psd(epoch,512,rate)
    Pxx = Pxx/np.sum(Pxx)   ## normailzation power distribution

##    svm
#    svm_classifier =   svm.SVC(gamma=0.001)
#    svm_classifier.fit(samples,stages)
#    stage = svm_classifier.predict(Pxx)
##  correct ness = 66%

### Knn 
#    clf = neighbors.KNeighborsClassifier(n_neighbors = 5)
#    clf.fit(samples, stages) 
#    stage = clf.predict(Pxx)
###   the defauklt k=5 gets the best result correct = 0.53 

### RF
#    rfc = RandomForestClassifier(n_estimators = 1200)
#    rfc  = rfc.fit(samples, stages)
#    stage = rfc.predict(Pxx)
##   Correct ness  0.82
    
## Naive Bayes
##  Gauess model    
#    gnb = GaussianNB()
#    stage =  gnb.fit(samples, stages).predict(Pxx)
###  correctness =0.86    

##  multinomial models
    mnb = MultinomialNB(alpha =0.0002)
    stage =  mnb.fit(samples, stages).predict(Pxx)
##     the best result above is 0.81 
##   submit result: 10/10 (all correct)    
    
### simple kNN classifier with avg power distribution
#    i = -1
#    diffSum=1000
#    stage = 0
#    
#    for px in  avg_pxx:
#        i = i+1
#        diff = np.sum(np.abs(Pxx-px)[1:65]/np.abs(avg_pxx[i])[1:65])
#        if diff < diffSum:
#            diffSum = diff
#            stage = i
##  Correctness:   80.8%       

### simple kNN classifier with all sample power distribution
#    i = -1
#    diffSum=1000
#    stage = 0
#    
#    for sampl in  g_ind_pxx:
#        i = i+1
#        diff = 0
#        
#        for epoch in sampl:
#            diff = diff + np.sum(np.abs((Pxx[1:65]-epoch[1:65])/np.abs(g_avg_pxx[i])[1:65]))
#
#        if diff < diffSum:
#            diffSum = diff
#            stage = i
### Not good enough: 78.5% correctness for testing data

#    cumPxx = np.cumsum(Pxx)
#    eng_main = cumPxx[8]
#    eng_sub =cumPxx[60]-cumPxx[40]
#    
#    val = eng_main*eng_sub
#    
#    
##    Pxx = Pxx/np.sum(cum_pxx,0)
##    stage = 0
##    sim = 0
##    i = -1
##    for pxx in cum_pxx:
##        i = i+1
##        sim_i = np.sum(pxx*Pxx)/np.sum(pxx)/np.sum(Pxx)
##        if sim_i > sim:
##            sim = sim_i
##            stage = i
##    max_pxx = np.max(Pxx)
##    max_pxx12 = np.max(Pxx[freqs>10])
##    bw_indexs = np.where(Pxx>=max_pxx/2)
##    bw_index = np.max(bw_indexs[0])
##    val = max_pxx*bw_index/max_pxx12
##    
#    if eng_main/eng_sub>100:
#        stage = 3n_neighbors 
#    elif val>0.025:
#        stage = 2
#    else:
#        stage = 1


#    plt.figure()
#    plt.plot(freqs,Pxx)   
#    plt.xlim(xmax=25)
#    plt.ylim(ymax=.2)
#    plt.title("Classified as: "+ str(stage))

    return stage

def plot_hypnogram(eeg, stages, srate):
    """
    This function takes the eeg, the stages and sampling rate and draws a 
    hypnogram over the spectrogram of the data.
    """
    
    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes
    
    #Use the specgram function to draw the spectrogram as usual
    Pxx, freqs, bins, im = plt.specgram(eeg,NFFT=512,Fs=srate)

    #Label your x and y axes and set the y limits for the spectrogram
    plt.ylim(ymax=30)
    plt.xlim(0,bins[len(bins)-1])
    plt.xlabel('Time(seconds)')
    plt.ylabel('Frequency(Hz)')
    
    ax2 = ax1.twinx() #Necessary for multiple y-axes
    
    #Use ax2.plot to draw the hypnogram.  Be sure your x values are in seconds
    #HINT: Use drawstyle='steps' to allow step functions in your plot
    stages = np.repeat(stages,10)[:len(bins)]
    ax2.plot(bins, stages, 'b',drawstyle = 'steps')
    plt.ylim(0.5,3.5)
    plt.xlim(0,bins[len(bins)-1])


    #Label your right y-axis and change the text color to match your plot
    ax2.set_ylabel('NREM stage',color='b')

 
    #Set the limits for the y-axis 
 
    #Only display the possible values for the stages
    ax2.set_yticks(np.arange(1,4))
    
    #Change the left axis tick color to match your plot
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')
    
    #Title your plot    
    plt.title('Hypnogram - Test Data')

        
def classifier_tester(classifiedEEG, actualEEG):
    """
    returns percent of 30s epochs correctly classified
    """
    epochs = len(classifiedEEG)
    incorrect = np.nonzero(classifiedEEG-actualEEG)[0]
    percorrect = (epochs - len(incorrect))/epochs*100
    
    print 'EEG Classifier Performance: '
    print '     Correct Epochs = ' + str(epochs-len(incorrect))
    print '     Incorrect Epochs = ' + str(len(incorrect))
    print '     Percent Correct= ' + str(percorrect) 
    print 
    return percorrect
  
    
def test_examples(examples, srate):
    """
    This is one example of how you might write the code to test the provided 
    examples.
    """
    i = 0
    bin_size = 30*srate
    c = np.zeros((4,len(examples[1,:])/bin_size))
    while i + bin_size < len(examples[1,:]):
        for j in range(1,4):
            c[j,i/bin_size] = classify_epoch(examples[j,range(i,i+bin_size)],srate)
        i = i + bin_size
    
    totalcorrect = 0
    num_examples = 0
    for j in range(1,4):
        canswers = np.ones(len(c[j,:]))*j
        correct = classifier_tester(c[j,:],canswers)
        totalcorrect = totalcorrect + correct
        num_examples = num_examples + 1
    
    average_percent_correct = totalcorrect/num_examples
    print 'Average Percent Correct= ' + str(average_percent_correct) 
    return average_percent_correct

def classify_eeg(eeg,srate):
    """
    DO NOT MODIFY THIS FUNCTION
    classify_eeg takes an array of eeg amplitude values and a sampling rate and 
    breaks it into 30s epochs for classification with the classify_epoch function.
    It returns an array of the classified stages.
    """
    bin_size_sec = 30
    bin_size_samp = bin_size_sec*srate
    t = 0
    classified = np.zeros(len(eeg)/bin_size_samp)
    while t + bin_size_samp < len(eeg):
       classified[t/bin_size_samp] = classify_epoch(eeg[range(t,t+bin_size_samp)],srate)
       t = t + bin_size_samp
    return classified
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.
    
    ##PART 1
    #Load the example data
    #Plot the psds
    #Plot the spectrograms
    examples, srate = load_examples('example_stages.npz')
    plot_example_psds(examples,srate) 
    print test_examples(examples, srate)
#            plot_example_spectrograms(example,srate)
    
    #Test the examples
    
    #Load the practice data
    eeg,srate = load_eeg('practice_eeg.npz')
    #Load the practice answers
    ans = load_stages('practice_answers.npz')
    #Classify the practice data
    stages = classify_eeg(eeg,srate)
    #Check your performance
    print classifier_tester(stages,ans)
    #Generate the hypnogram plots
    plot_hypnogram(eeg, stages, srate)


