import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow
nest.sli_run("M_WARNING setverbosity")

tick = time.time()

n, T_ms, R = control_flow.common_args()
m = int(n/4)

exc_dict = {"I_e": 150.0, "tau_m": 20.0}
inh_dict = {"I_e": 150.0, "tau_m": 20.0}

p_ee = 0.1
p_ii = 0.4
p_ei = 0.1
p_ie = 0.4

conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
conn_dict_ii = {'rule': 'pairwise_bernoulli', 'p': p_ii, "autapses" : False}
conn_dict_ei = {'rule': 'pairwise_bernoulli', 'p': p_ei, "autapses" : False}
conn_dict_ie = {'rule': 'pairwise_bernoulli', 'p': p_ie, "autapses" : False}

d = 1.0
Jee = 65
Jii = -65
Jei = 65
Jie = -65

syn_dict_ee = {"delay": d, "weight": Jee}
syn_dict_ii = {"delay": d, "weight": Jii}
syn_dict_ei = {"delay": d, "weight": Jei}
syn_dict_ie = {"delay": d, "weight": Jie}

poisson_dict = {'rate' : 20.0, 'origin' : 0.0}
conn_dict_poisson = {'rule': 'all_to_all'}
syn_dict_poisson = {"delay": 1.0, "weight": 65.0}

bin_step = 1
time_bins = np.arange(0,T_ms+bin_step,bin_step)
f_exc = np.zeros([int(T_ms/bin_step)],dtype = int)
f_inh = np.zeros([int(T_ms/bin_step)], dtype = int)

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

  exc = nest.Create("iaf_psc_alpha",n,params=exc_dict)
  inh = nest.Create("iaf_psc_alpha",m,params=inh_dict)

  nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii, syn_dict_ii)
  nest.Connect(exc, inh, conn_dict_ei, syn_dict_ei)
  nest.Connect(inh, exc, conn_dict_ie, syn_dict_ie)
  poisson_noise = nest.Create("poisson_generator", n=1, params=poisson_dict)
  multimeter_exc = nest.Create("multimeter", n=1, params={"withtime":True, "record_from":["V_m"]})
  multimeter_inh = nest.Create("multimeter", n=1, params={"withtime":True, "record_from":["V_m"]})
  spikedetector_exc = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
  spikedetector_inh = nest.Create("spike_detector", params={"withgid": True, "withtime": True})

  nest.Connect(poisson_noise,exc,conn_dict_poisson,syn_dict_poisson)
  nest.Connect(poisson_noise,inh,conn_dict_poisson,syn_dict_poisson)
  nest.Connect(multimeter_exc,exc)
  nest.Connect(multimeter_inh,inh)
  nest.Connect(exc,spikedetector_exc)
  nest.Connect(inh,spikedetector_inh)

  nest.Simulate(T_ms)

  dmm_exc = nest.GetStatus(multimeter_exc)
  dmm_inh = nest.GetStatus(multimeter_inh)
  ts_v, Vms_exc = data_analysis.voltage_extract(dmm_exc,n,plot=False)
  ts_v, Vms_inh = data_analysis.voltage_extract(dmm_inh,m,plot=False)

  Vpop_mean_exc = np.mean(Vms_exc,axis=0) # population mean of excitatory neurons
  Vpop_var_exc = np.var(Vms_exc,axis=0) # population variance of excitatory neurons
  Vpop_mean_inh = np.mean(Vms_inh,axis=0) # population mean of excitatory neurons
  Vpop_var_inh = np.var(Vms_inh,axis=0) # population variance of excitatory neurons

  dSD_exc = nest.GetStatus(spikedetector_exc,keys="events")[0]
  ts_s_exc = dSD_exc["times"]
  f_exc += np.histogram(ts_s_exc,bins=time_bins)[0]

  dSD_inh = nest.GetStatus(spikedetector_inh,keys="events")[0]
  ts_s_inh = dSD_inh["times"]
  f_inh += np.histogram(ts_s_inh,bins=time_bins)[0]

  #exc_st = data_analysis.st_extract(dSD_exc,n)
  #inh_st = data_analysis.st_extract(dSD_inh,m)

name = 'bernoulli_ei'

# voltage mean and variance with time

# total number of spikes with time
data = np.array([time_bins[1:],f_exc]).T
np.savetxt('%s_all_exc_spikes.txt'%(name),data)
data = np.array([time_bins[1:],f_exc]).T
np.savetxt('%s_all_inh_spikes.txt'%(name),data)