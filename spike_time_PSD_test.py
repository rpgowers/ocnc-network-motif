import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

nest.sli_run("M_WARNING setverbosity")

n, T_ms, R = control_flow.common_args()

p_ee = 0.1
conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
exc_dict = {"I_e": 200.0, "tau_m": 20.0}

d = 1.0
Jee = 100
syn_dict_ee = {"delay": d, "weight": Jee}

bin_step = 1
time_bins = np.arange(0,T_ms+bin_step,bin_step)

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})
  exc = nest.Create("iaf_psc_alpha",n,exc_dict)
  spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
  nest.Connect(exc, exc, conn_dict_ee,syn_dict_ee)
  nest.Connect(exc,spikedetector)
  
  nest.Simulate(T_ms)

  dSD = nest.GetStatus(spikedetector,keys="events")[0]
  ts_s = dSD["times"]
  f = np.histogram(ts_s,bins=time_bins)[0]

name = 'spike_PSD_test'
data_analysis.spike_plot(name,dSD)
data_analysis.spike_psd_plot(name,time_bins[1:],f)
import matplotlib.pylab as plt
plt.plot(time_bins[1:],f)
plt.show()