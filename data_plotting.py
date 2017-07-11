import numpy as np
import data_analysis
import control_flow
import time

tick = time.time()

data_dir = 'raw_data'
plot_dir = 'plots'
#name = 'bernoulli_ei' # change later for generality
name, n, T_ms, R, q = control_flow.plotting_args()
m = int(n/4)

# raw spiking data
bin_step = 1
time_bins = np.arange(0,T_ms+bin_step,bin_step)
f_exc = np.zeros([int(T_ms/bin_step)],dtype = int)
f_inh = np.zeros([int(T_ms/bin_step)], dtype = int)

big_bin = 10 # time bins used for pairwise comparisons
time_bins_big = np.arange(0,T_ms+big_bin,big_bin)
exc_coeff_all = []
inh_coeff_all = []

for i in np.arange(R): 
  data_exc_spike = np.load('%s/%s_raw_exc_spikes_q=%s_R=%s.npy'%(data_dir,name,q,i)).T
  data_inh_spike = np.load('%s/%s_raw_inh_spikes_q=%s_R=%s.npy'%(data_dir,name,q,i)).T
  ts_s_exc = data_exc_spike[0]
  send_exc = data_exc_spike[1]
  ts_s_inh = data_inh_spike[0]
  send_inh = data_inh_spike[1]
  f_exc += np.histogram(ts_s_exc,bins=time_bins)[0]
  f_inh += np.histogram(ts_s_inh,bins=time_bins)[0]

  exc_st = data_analysis.st_extract(send_exc,ts_s_exc,n,0)
  inh_st = data_analysis.st_extract(send_inh,ts_s_inh,m,n)
  _, exc_coeff = data_analysis.pair_correlate(exc_st,time_bins_big)
  _, inh_coeff = data_analysis.pair_correlate(inh_st,time_bins_big)
  exc_coeff_all += list(exc_coeff)
  inh_coeff_all += list(inh_coeff)

# spike psds
data_analysis.spike_psd_plot('%s/%s_q=%s_epop'%(plot_dir,name,q),time_bins[1:],f_exc)
data_analysis.spike_psd_plot('%s/%s_q=%s_ipop'%(plot_dir,name,q),time_bins[1:],f_inh)

# spike pairwise correlations
data_analysis.coefficient_histogram('%s/%s_q=%s_epop'%(plot_dir,name,q),exc_coeff_all)
data_analysis.coefficient_histogram('%s/%s_q=%s_ipop'%(plot_dir,name,q),inh_coeff_all)

# voltage means and variances
data_mom = np.loadtxt('%s/%s_vmom_epop_q=%s.txt'%(data_dir,name,q)).T
data_analysis.voltage_time_plots('%s/%s_q=%s_epop'%(plot_dir,name,q),data_mom[1],data_mom[2],data_mom[0])
data_mom = np.loadtxt('%s/%s_vmom_ipop_q=%s.txt'%(data_dir,name,q)).T
data_analysis.voltage_time_plots('%s/%s_q=%s_ipop'%(plot_dir,name,q),data_mom[1],data_mom[2],data_mom[0])

#data_analysis.spike_plot('%s/%s_raster_plot'%(plot_dir,name),dSD)
data_analysis.double_raster('%s/%s_q=%s'%(plot_dir,name,q),ts_s_exc,send_exc,ts_s_inh,send_inh)

tock = time.time()
print(tock-tick)