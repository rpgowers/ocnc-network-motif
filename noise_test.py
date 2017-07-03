import nest
import numpy as np
import visualize
import data_analysis
import control_flow

msd = 123456
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
nest.SetKernelStatus({'grng_seed' : msd+N_vp})
nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

n,T_ms = control_flow.common_args()


noise_dict = {'mean' : 0.0, 'std' : 20.0, 'dt' : 1.0}
current_noise = nest.Create('noise_generator', n=1, params=noise_dict)

ndict = {"I_e": 100.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
multimeter = nest.Create("multimeter", n=1)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})

nest.Connect(current_noise,exc)
nest.Connect(multimeter,exc)

#T_ms = 300.0
nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)