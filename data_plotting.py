import numpy as np
import data_analysis

name = 'bernoulli_ei' # change later for generality

# voltage means and variances
data_mom = np.loadtxt('%s_vmom_epop.txt'%(name)).T
data_analysis.voltage_time_plots('%s_epop'%(name),data_mom[1],data_mom[2],data_mom[0])
data_mom = np.loadtxt('%s_vmom_ipop.txt'%(name)).T
data_analysis.voltage_time_plots('%s_ipop'%(name),data_mom[1],data_mom[2],data_mom[0])

# spike psds
data = np.loadtxt('%s_all_exc_spikes.txt'%(name)).T
data_analysis.spike_psd_plot('%s_epop'%(name),data[0],data[1])
data = np.loadtxt('%s_all_inh_spikes.txt'%(name)).T
data_analysis.spike_psd_plot('%s_ipop'%(name),data[0],data[1])

# spike pairwise correlations
data = np.loadtxt('%s_epop_spike_correlations.txt'%(name))
data_analysis.coefficient_histogram('%s_epop'%(name),data)
data = np.loadtxt('%s_ipop_spike_correlations.txt'%(name))
data_analysis.coefficient_histogram('%s_ipop'%(name),data)
