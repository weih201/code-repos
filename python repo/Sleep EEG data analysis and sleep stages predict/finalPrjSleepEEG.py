#
#  NAME
#    finalPrj.py
#
#  DESCRIPTION
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m
import pandas as pd
import gc
import random as rd 
import copy
import scipy.stats as stats

from sklearn import  svm,neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

title_font = {'fontname':'Arial', 'size':'14', 'color':'black', 'weight':'normal'}
## ,         'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'12'}
mini_font = {'fontname':'Arial', 'size':'6'}


files = np.array([['S3_BSL.npz', 'S3_REC.npz'],['S1_BSL.npz', 'S1_REC.npz'], 
                  ['S2_BSL.npz', 'S2_REC.npz'],
                    ['S4_BSL.npz', 'S4_REC.npz']])
col_ids = ['c3a2','o2a1','roca2','loca1','emg1','emg2','emg3','c4a1','o1a2'] 

sleep_stages = ['Awake','NREM Stage 1','NREM Stage 2', 'NREM Stage 3',
                'NREM Stage 4','REM Sleep', 'Movement Time', 
                'Unscored'] 
classify_rows =['OvR_S1_BSL.npz', 'MS_S1_BSL.npz','OvR_S1_REC.npz', 'MS_S1_REC.npz',
           'OvR_S2_BSL.npz', 'MS_S2_BSL.npz','OvR_S2_REC.npz', 'MS_S2_REC.npz',
           'OvR_S3_BSL.npz', 'MS_S3_BSL.npz','OvR_S3_REC.npz', 'MS_S3_REC.npz',
           'OvR_S4_BSL.npz', 'MS_S4_BSL.npz','OvR_S4_REC.npz', 'MS_S4_REC.npz']

#####################################################################
###############  Data loading aned transformation ###################
#####################################################################

def load_data(filename):
    data = np.load(filename)
  
    srate = np.int(data['srate'])
    stages = data['stages']
    data = data['DATA']
    gc.collect()
    
    return data,srate,stages

def psd_df(data,srate,stages,col_ids):
    """
    Coverting the original data into the power spectrum density form 
    ans stored in a data frame structure
    every row is an epoch
    the epoch length is 30 sec
    """    
    eeg = pd.DataFrame(data)
    eeg = eeg.T
    eeg.columns = col_ids 
    
    psds_df,avg_psd, freqs = eeg_psds(eeg,srate,stages,col_ids)  
    
    eeg = None
    stages = None          
    gc.collect()
    return psds_df, avg_psd,freqs

def eeg_psds(eeg,rate,stages,col_ids):
    """
    Get the eeg data psd of every 30 second 
    """
    bins = get_bins(eeg,stages)  ## getting the elem index in each 30s bin
##    bins = pd.cut(eeg.index,len(stages)) ## not working
    bi = np.arange(len(stages))  ## the numbe of bins
    
##  Creating a empty dataframe with all channels and stage as the columns  
    col_ids.append('stage')   # creating the columns fo target datframe,
    df_psds = pd.DataFrame(columns= col_ids)    ## creating the df with given columns
##    avg_psd = pd.DataFrame(columns=col_ids)    ## creating df fo avg psd 
    
     
    for i in bi:   ## creating bin
        eeg_epoch = eeg.iloc[bins[i]]  ## get the eeg data in this bin
        stage = stages[i]              ## retriving the stage for this bin
        psd_item,freqs = epoch_psd(eeg_epoch,rate,stage)  ## Getting the df item form 
                                        ## psd, where each channel hold one column 
                                        ## in a row, and the stage hold the last 
                                        ## column in the row
        df_psds.loc[i] = psd_item   ## Appending the itme into the data frame
##        avg_psd.loc[i] = avg_item
    return df_psds,df_psds.groupby(['stage']).sum()/df_psds.groupby(['stage']).\
                count(),freqs   ## Returning the psd data frame

def epoch_psd(epoch,rate,stage):
    """"
    Get the psd of the epoch
    Just keep the 0-5 Hz and 10-15 Hz
    """
    epoch_psd = []
    avg_psd=[]
    for col in epoch.columns:  ## for each channels 
        pxx, freqs = m.psd(epoch[col],512,rate)
        pxx = pxx/np.sum(pxx)       ### Normailzation spectrum power 
        
#        px = np.concatenate([pxx[0:20],pxx[40:60]])  ## Retriving 0-5 and 10-15 hz data
        epoch_psd.append(pxx)                  ##   appending channel psd data into the item 
                                              ##  a column
        avg_psd.append(pxx)
    
    epoch_psd.append(stage)  ## Aooending the stage as the last column of the epoch psd 
    avg_psd.append(stage)
    return epoch_psd ,freqs  ##,avg_psd,

def get_bins(eeg,stages):
    """
    Getting the elem index in each bin
    """
    w = np.int(len(eeg)/len(stages))   ## Length of data in each bin
    odds = len(eeg) - w*len(stages)   ## Possible remain data number which can 
                                      ## binneed into a eaqual

    index = np.arange(len(eeg))
    bins = []
    li=0
    for i in np.arange(len(stages)):
        if odds>0:                      ## When remain data bigger one, add a bit into curr bin
            hi=li+w+1
            odds = odds-1
        else:
            hi=li+w
#        print i,li,hi
        bins.append(index[li:hi])
        li = hi
    return bins

#######################################################
#############  Data visualization  ####################
#######################################################
def plot_data(data,rate,sub,night):
    """
    Plot the loaded raw data
    """
    nrows  = len(data)
    t = np.arange(len(data[0]))/np.float(rate)  ## get the time(sec)
    fig, axx = plt.subplots(nrows = nrows)
    i=0
    for ax in axx:
        ax.plot(t,data[i])
        ax.set_yticklabels([])
        if i<> nrows-1:
            ax.set_xticklabels([])
        ax.set_ylabel(col_ids[i],rotation = 'vertical')
        i=i+1

    plt.subplots_adjust(hspace=0.001)
    plt.subplots_adjust(wspace=0.001)
    axx[0].set_title(str(sub)+' '+str(night)+' input data',**title_font)
    axx[nrows-1].set_xlabel('Time(seconds)')
    plt.show()

def plot_hypnogram(data,rate,stgs,sub,night):
    rows = len(data)
    fig,axx = plt.subplots(nrows=rows)
    
    i = 0
    for ax in axx:
        #Use the specgram function to draw the spectrogram as usual
        Pxx, freqs, bins, im = ax.specgram(data[i],NFFT=512,Fs=rate)
        ax.set_yticks([0,10,20])    
        ax.set_ylim([0,30])
        ax.set_xlim([0,bins[len(bins)-1]])
        
#        ax.set_yticklabels([])
        if i<> rows-1:
            ax.set_xticklabels([])
        ax.set_ylabel(col_ids[i],rotation = 'vertical')
        
        ax2 = ax.twinx() # clone x - axis data
        stages = np.repeat(stgs,10)[:len(bins)]
        
        if len(bins) > len(stages):               ## filling the stages to same length of bins
            fillings = np.ones(len(bins)-len(stages))
            stages =np.append(stages,fillings)
        elif len(bins)<len(stages):
            stages = stages[:(len(bins)-1)]

        ax2.plot(bins, stages, 'b',drawstyle = 'steps')  ## drawstyle='steps' to allow step functions
        ax2.set_ylim([-0.5,7.5])
        ax2.set_xlim([0,bins[len(bins)-1]])

        ax2.set_yticks(np.arange(np.max(stages)+1))
        ax2.set_yticklabels(sleep_stages,**mini_font)
        
        i = i+1
        
    plt.subplots_adjust(hspace=0.001)
    plt.subplots_adjust(wspace=0.001)
    axx[0].set_title('Hypnogram-Sleep Stages graph for '+str(sub)+'_'+str(night)+'.npz')
    axx[rows-1].set_xlabel('Time(seconds)',**axis_font)
    fig.text(0.08, 0.5, 'Hypnogram from 0 to 30 hz', va='center', rotation='vertical')
    plt.show()

def plot_psd(avg_psd, freqs,sub, night):
    stages, chans = avg_psd.shape
    
    for stage in avg_psd.index:
        fig,ax = plt.subplots(nrows=3,ncols=np.int(np.ceil(chans/3)))
        rows,cols = ax.shape
        
        chan = 0
        for row in np.arange(rows):
            for col in np.arange(cols):
                ax[row,col].plot(freqs,avg_psd.ix[stage, chan])
#                ax[row,col].set_xlim(xmax=30)
                ax[row,col].set_title('Channel:'+col_ids[chan])
                chan =  chan+1

        plt.subplots_adjust(hspace = 0.3)
        fig.suptitle(str(sub)+'_'+ str(night)+ '.npz '+sleep_stages[stage]+\
                       ' stage power spectrum density',**title_font)
        plt.show()

def plot_stages(df,sub,night,b_fig):
    stages = df['stage']
    t = np.arange(len(stages))*30
    
    fig_base=2
    if b_fig:
        plt.figure() 
        fig_base = 1
 
## stepwise sleep stages plotting       
    ax = plt.subplot(2,2,fig_base)
    ax.plot(t, stages, 'b',drawstyle = 'steps')
    plt.ylim(-0.5,7.5)
    ax.set_yticks(np.arange(np.max(stages)+1))
    ax.set_yticklabels(sleep_stages)
    plt.xlim(0,t[len(t)-1])
    plt.title('Sleep Stages: '+str(sub)+'_'+str(night),**title_font)
    plt.xlabel('Time(seconds)',**axis_font)
    plt.subplots_adjust(hspace = 0.3,wspace =0.3)
    
### Histogram plot
    ax = plt.subplot(2,2,fig_base+2)
    bins_num = np.max(stages)-np.min(stages)+1
###  This with hist is workinbg     
##    plt.hist(stages,bins=bins_num,range=(-0.5,7.5))  
#    
###  This also working, and give more control    
    hist, bins = np.histogram(stages, bins=bins_num,density=True)
    width = 1
    center = np.arange(np.max(stages)+1)
    plt.bar(center, hist, align='center', width=width)
    plt.title('Histgram of sleep stages: '+str(sub)+ '_'+str(night),**title_font)
    plt.ylabel('Frequency density',**axis_font)
    plt.xticks(center, sleep_stages, rotation=45)
    # Pad margins so that markers don't get clipped by the axes
#    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15,wspace = 0.3)
    plt.show() 
    return hist

#########################################################################
############################## Classifying ##############################
#########################################################################
def classifier(df,sub,night):
##  Classify the and predict stages\
    
    r_trim=0.1
    df = df_trim(df,r_trim,1-r_trim)  ##  trim the start and end of stage
    
    df_test,df_train = dfsmple(df,0.2)  ## splitting
    ans = np.asarray(df_test['stage'],dtype = np.int16)    
        
##  One vs Rest classifer:
    ovr_corrects = []
    for col in col_ids:
        stages = OvRclassifer(df_train[col],df_train['stage'],df_test[col])
#       print stages
        correctness = np.float(np.sum(ans == stages))/len(stages)
        ovr_corrects.append(correctness)
        print "OvR classying correctness for "+str(col)+" channel in "+ \
                      str(sub)+"_"+str(night)+" is :", correctness
           
#  Split manually:    
#    df_test,df_train = dfsmple(df,0.2)
#    ans = np.asarray(df_test['stage'],dtype = np.int16)    
    ms_corrects = []   
    for col in col_ids:
        stages = tt_classifer(df_test[col],df_train[col],df_train['stage'])
 #      print stages
        incorrect = np.nonzero(ans-stages)[0]
  #     correctness = np.float(np.sum(ans == stages))/len(stages)
        correctness = 1-np.float(len(incorrect))/len(stages)
        ms_corrects.append(correctness)
        print "Manual splitting classying correctness for "+str(col)+ \
              " channel in "+str(sub)+"_"+str(night)+" is :", correctness
#
    return ovr_corrects, ms_corrects

def tt_classifer(test,train, train_stages):
    train = shaper(train)
    test = shaper(test)
    stages = np.asarray(train_stages,dtype=np.int16)
    
##    svm
#    svm_classifier =   svm.SVC(gamma=0.001)
#    svm_classifier.fit(train,stages)
#    stage = svm_classifier.predict(test)

### Knn 
#    clf = neighbors.KNeighborsClassifier(n_neighbors = 5)
#    clf.fit(train, stages) 
#    stage = clf.predict(test)

## RF
    rfc = RandomForestClassifier(n_estimators = 1200)
    rfc  = rfc.fit(train, stages)
    stage = rfc.predict(test)
    
## Naive Bayes
##  Gauess model    
#    gnb = GaussianNB()
#    stage =  gnb.fit(train,stages).predict(test)

##  multinomial models
#    mnb = MultinomialNB(alpha =0.001)
#    stage =  mnb.fit(train, stages).predict(test)

###  decision tree classifier
#    tr = tree.DecisionTreeClassifier()
#    tr = tr.fit(train, stages)
#    stage = tr.predict(test)

    
    return stage

def OvRclassifer(df, stages, df_test):
    df = shaper(df)
    df_test = shaper(df_test)
    stages = np.asarray(stages,dtype=np.int16)

##  with linear svc
#    return OneVsRestClassifier(LinearSVC(random_state=0)).fit(df, stages).predict(df_test)    
    
##  with decision tree classifier
#    return OneVsRestClassifier(tree.DecisionTreeClassifier()).fit(df, stages).predict(df_test)    
 
##  with random forest
    return OneVsRestClassifier(RandomForestClassifier(n_estimators = 1200)).fit(df, stages).predict(df_test)    


def df_trim(df,start,end):
    """
    Filtering out the start and end part of data
    """
    l = len(df)
    i_start = np.int(l*start)
    i_end = np.int(l*end)
    return df[i_start:i_end]

def dfsmple(df, ratio):
    """
    Sampling the processed data frame
    """
    rows = rd.sample(df.index, np.int(len(df.index)*ratio))
    return df.ix[rows], df.drop(rows)

def shaper(data):
    """
    Reshaping the list of arraies of list form data in the data frame column 
    into the two-dimensional array form, so the classifer's fit fit function 
    can read the shape param
    input: an array of list, corresponding to the a column in psd dataframe
    output: a two-dimensional array, the shape is nrow x n_features
    """
    nrow = len(data)
    n_features = len(np.array(data)[0])
    
    shaped = [x for y in data for x in y]
    shaped = np.array(shaped)
    shaped.shape = (nrow,n_features)
    return shaped
    

##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    gc.collect()
    plt.close('all') #Closes old plots.

    files_df = pd.DataFrame(data=files, index=['S3','S1','S2','S4'],
                               columns=['BSL','REC'])

    classify_df = pd.DataFrame(columns=col_ids,index = classify_rows)
    
    for sub in files_df.index:
        b_fig = True
        sub_files = files_df.ix[sub]
        hist_df = pd.DataFrame(columns =['BSL','REC'] )  ## store the returne hist data 
        
        stages_lst = []
        for night in files_df.columns:
            fi = sub_files[night]
            data,rate,stages = load_data(fi)
            stages_lst.append(stages)
            
#            plot_data(data,rate, sub,night)   ## data plotting 
#            plot_hypnogram(data,rate,stages,sub,night)  ## plotting sprogram
#            break
            
## Transoforming the original data into psd spectrum data frame form            
            df, avg_psd, freqs = psd_df(data,rate,stages,copy.deepcopy(col_ids))
            plot_psd(avg_psd, freqs, sub, night)
            break
#            hist_df[night]= plot_stages(df,sub,night,b_fig)
#            b_fig=False
##  Classify the and predict stages
#            OvRCorrect,MSCorrect = classifier(df,sub,night)
#            ovr_index = 'OvR_'+sub+'_'+night+'.npz'
#            ms_index = 'MS_'+sub+'_'+night+'.npz'
#            classify_df.ix[ovr_index] = OvRCorrect
#            classify_df.ix[ms_index] = MSCorrect
#            data = None
#            gc.collect()
#        break
#        d, pval = stats.ks_2samp(hist_df['BSL'], hist_df['REC'])
#        print 'The p value of BSL and REC have the same distribution in '+\
#                sub + ' is : ' + str(pval)
               
#        d, pval = stats.ks_2samp(stages_lst[0], stages_lst[1])
#        print 'The p value of between stages in Baseline and Restore nights of '+\
#                sub + ' is : ' + str(pval)
    
#        
    print classify_df
    classify_df.to_csv('classification.txt',sep='\t')

            


