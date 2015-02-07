#
#  NAME
#    problem_set2_solutions.py
#
#  DESCRIPTION
#    Open, view, and analyze action potentials recorded during a behavioral
#    task.  In Problem Set 2, you will write create and test your own code to
#    create tuning curves.
#

#Helper code to import some functions we will use
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as mlab
from scipy import optimize
from scipy import stats


def load_experiment(filename):
    """
    load_experiment takes the file name and reads in the data.  It returns a
    two-dimensional array, with the first column containing the direction of
    motion for the trial, and the second column giving you the time thespk_times

    animal began movement during thaht trial.
    """
    data = np.load(filename)[()];
    return np.array(data)

def load_neuraldata(filename):
    """
    load_neuraldata takes the file name and reads in the data for that neuron.
    It returns an arary of spike times.
    """
    data = np.load(filename)[()];
    return np.array(data)
    
def bin_spikes(trials, spk_times, time_bin):
    """
    bin_spikes takes the trials array (with directions and times) and the spk_times
    array with spike times and returns the average firing rate for each of the
    eight directions of motion, as calculated within a time_bin before and after
    the trial time (time_bin should be given in seconds).  For example,
    time_bin = .1 will count the spikes from 100ms before to 100ms after the 
    trial began.
    
    dir_rates should be an 8x2 array with the first column containing the directions
    (in degrees from 0-360) and the second column containing the average firing rate
    for each direction
    """
    dirs=np.unique(trials[:,0])
    dir_rates = np.zeros((len(dirs),2)) 
    dir_rates = np.column_stack((dirs,dir_rates))
    
    for direction, time in trials:
        index = plt.find(dir_rates[:,0]==direction)
        dir_rates[index,2]=dir_rates[index,2]+1
        t_low = time - time_bin
        t_high = time + time_bin
        dir_rates[index,1] = dir_rates[index,1] + np.sum((spk_times > t_low) & (spk_times < t_high ))
                
    for count in dir_rates:
        count[1]=count[1]/time_bin/2/count[2]
    
    dir_rates = np.delete(dir_rates,2,1)
    return dir_rates

    
def plot_tuning_curves(direction_rates, title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates) and plots a histogram and 
    polar representation of the tuning curve. It adds the given title.
    """
    plt.subplot(2,2,1)
    plt.bar(direction_rates[:,0],direction_rates[:,1],width=45)
    plt.xlabel("Directions of Motion (degrees)")
    plt.ylabel("Firing Rates (spikes/s)")
    plt.title(title)
    plt.xlim([0,360])
#    plt.axis([0,360,0,40])
##    plt.xticks(direction_rates[:,0])
    plt.xticks(direction_rates[:,0]+45./2,direction_rates[:,0].astype(int))
    
    direction_rates = np.vstack((direction_rates,direction_rates[0])) 
    
    plt.subplot(2,2,2,polar=True)
    theta = direction_rates[:,0]*np.pi/180
    plt.polar(theta,direction_rates[:,1],label="Firing Rates (spikes/s)")
    plt.legend(loc=8,prop={'size':8})
    plt.title(title)
    
   
    
def roll_axes(direction_rates):
    """
    roll_axes takes the x-values (directions) and y-values (direction_rates)
    and return new x and y values that have been "rolled" to put the maximum
    direction_rate in the center of the curve. The first and last y-value in the
    returned list should be set to be the same. (See problem set directions)
    Hint: Use np.roll()
    """
    m_ind = np.argmax(direction_rates[:,1])
    roll_degrees = 4-m_ind
    new_ys = np.roll(direction_rates[:,1],roll_degrees,axis=0)
    new_ys = np.append(new_ys,new_ys[0])
    new_xs = (np.arange(0,361,direction_rates[1,0])-roll_degrees*direction_rates[1,0]) 
    
    if np.amax(new_xs)>360:
        new_xs=new_xs-360
    elif np.amin(new_xs)<-360:
        new_xs=new_xs+360
        
    return new_xs, new_ys, roll_degrees    
    

def normal_fit(x,mu, sigma, A):
    """
    This creates a normal curve over the values in x with mean mu and
    variance sigma.  It is scaled up to height A.
    """
    n = A*mlab.normpdf(x,mu,sigma)
    return n

def fit_tuning_curve(centered_x,centered_y):
    """
    This takes our rolled curve, generates the guesses for the fit function,
    and runs the fit.  It returns the parameters to generate the curve.
    """
    max_y = np.amax(centered_y)
    max_x = centered_x[np.argmax(centered_y)]
    sigma = 90
    p, cov = optimize.curve_fit(normal_fit,centered_x, centered_y, p0=[max_x, sigma, max_y])
    
    fit_xs = np.arange(centered_x[0],centered_x[-1])
    fit_ys = normal_fit(fit_xs,p[0],p[1],p[2])
    roll_num = np.sum(fit_xs<0)
    fit_xs[0:roll_num] = fit_xs[0:roll_num] + 360
    fit_ys = np.roll(fit_ys,-roll_num)
    fit_xs = np.roll(fit_xs,-roll_num)

    return np.column_stack((fit_xs,fit_ys))
    


def plot_fits(direction_rates,fit_curve,title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates and fit_curve) and plots the 
    actual values with circles, and the curves as lines in both linear and 
    polar plots.
    """
    xs = direction_rates[:,0]
    ys = direction_rates[:,1]
    
    fit_xs = fit_curve[:,0]
    fit_ys = fit_curve[:,1]

    plt.subplot(2,2,3)
    plt.plot(xs,ys,'o',hold=True)
    plt.plot(fit_xs,fit_ys,'-')
#    plt.legend(["original","fit"])        

    plt.xlabel("Directions of Motion (degrees)")
    plt.ylabel("Firing Rates (spikes/s)")
#    plt.title(title)
    plt.xlim([0,360])
#    plt.axis([0,360,0,40])

    plt.subplot(2,2,4,polar=True)
    original_theta = xs*np.pi/180
    plt.polar(original_theta,ys,'o')

    fit_theta = fit_xs*np.pi/180
    plt.polar(fit_theta,fit_ys,label="Firing Rates (spikes/s)")
    plt.legend(loc=8,prop={'size':8})
#    plt.title(title)

def von_mises_fitfunc(x, A, kappa, l, s):
    """
    This creates a scaled Von Mises distrubition.
    """
    return A*stats.vonmises.pdf(x, kappa, loc=l, scale=s)

def fit_von_mises_curve(x,y):
    """
    This takes to fit the von mises curve, 
    it returns the parameters to generate the curve.
    """
    r_x = x*np.pi/180.
    max_y = np.amax(y)
    max_x = r_x[np.argmax(y)]
    p, cov = optimize.curve_fit(von_mises_fitfunc,r_x, y, p0=[max_y, 4, max_x,1])
    
    fit_xs = np.arange(x[0],x[-1])*np.pi/180
    fit_ys = von_mises_fitfunc(fit_xs,p[0],p[1],p[2],p[3])
    
    roll_num = np.sum(fit_xs<0)
    fit_xs[0:roll_num] = fit_xs[0:roll_num] + 2.*np.pi
    fit_xs = fit_xs*180/np.pi

    fit_ys = np.roll(fit_ys,-roll_num)
    fit_xs = np.roll(fit_xs,-roll_num)

    return np.column_stack((fit_xs,fit_ys))

    
def preferred_direction(fit_curve):
    """
    The function takes a 2-dimensional array with the x-values of the fit curve
    in the first column and the y-values of the fit curve in the second.  
    It returns the preferred direction of the neuron (in degrees).
    """
    pd = fit_curve[np.argmax(fit_curve[:,1]),0]
  
    print "The preferred direction(degrees) is : ", pd
    return pd
    
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    spk_times_name = 'neuron3'
    spk_times_name_file = spk_times_name +'.npy'    
    
    trials = load_experiment('trials.npy')   
    spk_times = load_neuraldata(spk_times_name_file) 
    direction_rates = bin_spikes(trials, spk_times, 0.1)
    

    old_params = plt.rcParams
    plt.rcParams['figure.figsize'] = 13,7
    plt.subplots_adjust(hspace = 0.4)

    plot_tuning_curves(direction_rates, spk_times_name.capitalize()+" Tuning Curve")
    
    centered_x, centered_y, deg = roll_axes(direction_rates)
    
    fit_curve = fit_tuning_curve(centered_x,centered_y)    
    plot_fits(direction_rates,fit_curve,spk_times_name.capitalize()+" Tuning Curve - Fit")
    
    preferred_direction(fit_curve)
    
    fit_curve = fit_von_mises_curve(centered_x,centered_y) 
    preferred_direction(fit_curve)
    plt.figure()
    plot_fits(direction_rates,fit_curve,spk_times_name.capitalize()+" Von Mises Fitting")

    plt.rcParams = old_params

#    ctl = 'y'
#    while ctl == 'y' :  
#       spk_times_name = raw_input("Please input spike times signal file: ")
#       print "You entered: ", spk_times_name
#       
#       spk_times_name_file = spk_times_name +'.npy'
#       
#       spk_times = load_neuraldata('example_spikes.npy') 
#       direction_rates = bin_spikes(trials, spk_times, 0.1)
#        
#       old_params = plt.rcParams
#       plt.rcParams['figure.figsize'] = 13,7
#       plt.subplots_adjust(hspace = 0.4)
#    
#       plot_tuning_curves(direction_rates, spk_times_name.capitalize()+" Tuning Curve")
#        
#       centered_x, centered_y, deg = roll_axes(direction_rates)
#        
#       fit_curve = fit_tuning_curve(centered_x,centered_y)    
#       plot_fits(direction_rates,fit_curve,spk_times_name.capitalize()+" Tuning Curve - Fit")
#        
#       preferred_direction(fit_curve)
#        
#       fit_curve = fit_von_mises_curve(centered_x,centered_y) 
#       preferred_direction(fit_curve)
##       plt.figure()
##       plot_fits(direction_rates,fit_curve,spk_times_name.capitalize()+" Von Mises Fitting")
#    
#       plt.rcParams = old_params
#       
#       ctl=raw_input("Do you want continue (y/n)? ")
# 
#    print "Good bye!"
