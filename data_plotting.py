import numpy as np
import data_analysis

name = 'bernoulli_ei' # change later for generality

# spike psds
data = np.loadtxt('%s_all_exc_spikes.txt'%(name)).T
data_analysis.spike_psd_plot('%s_epop'%(name),data[0],data[1])
data = np.loadtxt('%s_all_inh_spikes.txt'%(name)).T
data_analysis.spike_psd_plot('%s_ipop'%(name),data[0],data[1])