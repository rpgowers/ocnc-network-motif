import nest
import numpy as np
import visualize
import data_analysis
import control_flow

n, T_ms = control_flow.common_args()
P_bar = np.zeros([int(T_ms/2)])
isi_tot = []
N = n
ndict = {"I_e": 250.0, "tau_m": 20.0}
conn_dict_ee = {'rule': 'fixed_total_number', 'N': N, "autapses" : False}
Jee = 20.0
d = 1.0
syn_dict_ee = {"delay": d, "weight": Jee}

R = 20 # number of realisations of the random network
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
  # uncomment to check a different network is being created each time:

  # filename = "random_exc_test_%s.pdf"%(i)
  # nodes = [exc]
  # colors = ["lightpink"]
  # visualize.plot_network(nodes, colors, filename)

  nest.Simulate(T_ms)
  dmm = nest.GetStatus(multimeter)
  ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=False)
  PSD,freq = data_analysis.voltage_psd(ts_v,Vms,plot=False)
  V_mean[i] = np.mean(Vms) # mean across all neurons for all time
  V_var[i] = np.var(Vms) # variance across all neurons for all time
  P = np.mean(PSD,axis=0)
  P_bar += P/R
  dSD = nest.GetStatus(spikedetector,keys="events")[0]
  isi = data_analysis.isi_extract(dSD,n,plot=False)
  isi_plot = [item for sublist in isi for item in sublist]
  isi_tot = isi_tot + isi_plot

import matplotlib.pylab as plt
print(V_mean)
print(V_var)
#plt.hist(np.array(isi_tot))
#plt.show()
#plt.plot(freq,P_bar)
#plt.show()