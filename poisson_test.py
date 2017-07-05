import nest
import numpy as np
import visualize
import data_analysis
import control_flow

msd = 123456
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
nest.SetKernelStatus({'grng_seed' : msd+N_vp})
nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

n,T_ms,R = control_flow.common_args()

poisson_dict = {'rate' : 50.0, 'origin' : 0.0}
poisson_noise = nest.Create("poisson_generator", n=1, params=poisson_dict)
conn_dict_poisson = {'rule': 'all_to_all'}
syn_dict_poisson = {"delay": 1.0, "weight": 150.0}

ndict = {"I_e": 50.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
multimeter = nest.Create("multimeter", n=1)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})

nest.Connect(poisson_noise,exc,conn_dict_poisson,syn_dict_poisson)
nest.Connect(multimeter,exc)

nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)