import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

nest.sli_run("M_WARNING setverbosity")

tick = time.time()

n, T_ms, R = control_flow.common_args() # here n is the number of excitatory neurons

exc_dict = {"I_e": 200.0, "tau_m": 20.0}
inh_dict = {"I_e": 200.0, "tau_m": 20.0}
N_ee = n
m = int(n/4)
N_ii = m
N_ei = m 
N_ie = n

conn_dict_ee = {'rule': 'fixed_total_number', 'N': N_ee, "autapses" : False}
conn_dict_ii = {'rule': 'fixed_total_number', 'N': N_ii, "autapses" : False}
conn_dict_ei = {'rule': 'fixed_total_number', 'N': N_ei, "autapses" : False}
conn_dict_ie = {'rule': 'fixed_total_number', 'N': N_ie, "autapses" : False}

d = 1.0
Jee = 100
Jii = -100
Jei = 100
Jie = -100

syn_dict_ee = {"delay": d, "weight": Jee}
syn_dict_ii = {"delay": d, "weight": Jii}
syn_dict_ei = {"delay": d, "weight": Jei}
syn_dict_ie = {"delay": d, "weight": Jie}

P_bar_exc = np.zeros([int(T_ms/2)])
P_bar_inh = np.zeros([int(T_ms/2)])
Vpop_mean_bar_exc = np.zeros([int(T_ms)-1])
Vpop_var_bar_exc = np.zeros([int(T_ms)-1])
Vpop_mean_bar_inh = np.zeros([int(T_ms)-1])
Vpop_var_bar_inh = np.zeros([int(T_ms)-1])
V_mean_exc = np.zeros([R])
V_mean_inh = np.zeros([R])
V_var_exc = np.zeros([R])
V_var_inh = np.zeros([R])

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

  exc = nest.Create("iaf_psc_alpha",n,params=exc_dict)
  inh = nest.Create("iaf_psc_alpha",m,params=inh_dict)
  multimeter_exc = nest.Create("multimeter", 1)
  multimeter_inh = nest.Create("multimeter", 1)
  nest.SetStatus(multimeter_exc, {"withtime":True, "record_from":["V_m"]})
  nest.SetStatus(multimeter_inh, {"withtime":True, "record_from":["V_m"]})

  nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii, syn_dict_ii)
  nest.Connect(exc, inh, conn_dict_ei, syn_dict_ei)
  nest.Connect(inh, exc, conn_dict_ie, syn_dict_ie)
  nest.Connect(multimeter_exc, exc)
  nest.Connect(multimeter_inh, inh)

  nest.Simulate(T_ms)
  dmm_exc = nest.GetStatus(multimeter_exc)
  dmm_inh = nest.GetStatus(multimeter_inh)
  ts_v, Vms_exc = data_analysis.voltage_extract(dmm_exc,n,plot=False)
  ts_v, Vms_inh = data_analysis.voltage_extract(dmm_inh,m,plot=False)
  PSD_exc,freq = data_analysis.voltage_psd(ts_v,Vms_exc,plot=False)
  PSD_inh,freq = data_analysis.voltage_psd(ts_v,Vms_inh,plot=False)

  P_exc = np.mean(PSD_exc,axis=0)
  P_inh = np.mean(PSD_inh,axis=0)
  P_bar_exc += P_exc/R
  P_bar_inh += P_inh/R
  V_mean_exc[i] = np.mean(Vms_exc) # mean across all neurons for all time
  V_mean_inh[i] = np.mean(Vms_inh) # mean across all neurons for all time
  V_var_exc[i] = np.var(Vms_exc) # variance across all neurons for all time
  V_var_inh[i] = np.var(Vms_inh) # variance across all neurons for all time
  Vpop_mean_exc = np.mean(Vms_exc,axis=0) # population mean of excitatory neurons
  Vpop_var_exc = np.var(Vms_exc,axis=0) # population variance of excitatory neurons
  Vpop_mean_inh = np.mean(Vms_inh,axis=0) # population mean of excitatory neurons
  Vpop_var_inh = np.var(Vms_inh,axis=0) # population variance of excitatory neurons
  Vpop_mean_bar_exc += Vpop_mean_exc/R
  Vpop_var_bar_exc += Vpop_var_exc/R
  Vpop_mean_bar_inh += Vpop_mean_inh/R
  Vpop_var_bar_inh += Vpop_var_inh/R

name = 'simple_exc_inh_epop'
data_analysis.psd_mean_plot(name,P_bar_exc,freq)
data_analysis.voltage_hist_plots(name,V_mean_exc, V_var_exc)
data_analysis.voltage_time_plots(name,Vpop_mean_bar_exc,Vpop_var_bar_exc,ts_v)

name = 'simple_exc_inh_ipop'
data_analysis.psd_mean_plot(name,P_bar_inh,freq)
data_analysis.voltage_hist_plots(name,V_mean_inh, V_var_inh)
data_analysis.voltage_time_plots(name,Vpop_mean_bar_inh,Vpop_var_bar_inh,ts_v)

tock = time.time()
print("Total elapsed time = %.3fs"%(tock-tick))