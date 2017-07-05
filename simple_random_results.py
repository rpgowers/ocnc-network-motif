import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

tick = time.time()

nest.set_verbosity(level="M_QUIET")

n, T_ms,R = control_flow.common_args()
P_bar = np.zeros([int(T_ms/2)])
Vpop_mean_bar = np.zeros([int(T_ms)-1])
Vpop_var_bar = np.zeros([int(T_ms)-1])

isi_tot = []
N = n
ndict = {"I_e": 200.0, "tau_m": 20.0}
conn_dict_ee = {'rule': 'fixed_total_number', 'N': N, "autapses" : False}
Jee = 80.0
d = 1.0
syn_dict_ee = {"delay": d, "weight": Jee}

#R = 20 # number of realisations of the random network
V_mean = np.zeros([R])
V_var = np.zeros([R])
start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()

  msd = start_seed + i
  # 'resolution' : 0.1
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

  exc = nest.Create("iaf_psc_alpha",n,params=ndict)
  multimeter = nest.Create("multimeter", 1)
  nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})
  spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
  nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)
  nest.Connect(multimeter, exc)
  nest.Connect(exc,spikedetector)

  nest.Simulate(T_ms)
  dmm = nest.GetStatus(multimeter)
  ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=False)
  PSD,freq = data_analysis.voltage_psd(ts_v,Vms,plot=False)
  V_mean[i] = np.mean(Vms) # mean across all neurons for all time
  V_var[i] = np.var(Vms) # variance across all neurons for all time
  Vpop_mean = np.mean(Vms,axis=0)
  Vpop_var = np.var(Vms,axis=0)

  Vpop_mean_bar += Vpop_mean/R
  Vpop_var_bar += Vpop_var/R
  P = np.mean(PSD,axis=0) # PSD mean across neurons
  P_bar += P/R
  dSD = nest.GetStatus(spikedetector,keys="events")[0]
  isi = data_analysis.isi_extract(dSD,n,plot=False)
  isi_plot = [item for sublist in isi for item in sublist]
  isi_tot = isi_tot + isi_plot

name = 'simple_exc'
data_analysis.voltage_hist_plots(name,V_mean, V_var)
data_analysis.isi_hist_plot(name,isi_tot)
data_analysis.psd_mean_plot(name,P_bar,freq)
data_analysis.spike_plot(name,dSD)
data_analysis.voltage_time_plots(name,Vpop_mean_bar,Vpop_var_bar,ts_v)

tock = time.time()
print("Total elapsed time = %.3fs"%(tock-tick))