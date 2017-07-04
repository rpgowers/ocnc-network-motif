import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

tick = time.time()

n, T_ms, R = control_flow.common_args() # here n is the number of excitatory neurons

exc_dict = {"I_e": 250.0, "tau_m": 20.0}
inh_dict = {"I_e": 250.0, "tau_m": 20.0}
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
Jee = 20
Jii = -20
Jei = 20
Jie = -20

syn_dict_ee = {"delay": d, "weight": Jee}
syn_dict_ii = {"delay": d, "weight": Jii}
syn_dict_ei = {"delay": d, "weight": Jei}
syn_dict_ie = {"delay": d, "weight": Jie}

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()

  exc = nest.Create("iaf_psc_alpha",n,params=exc_dict)
  inh = nest.Create("iaf_psc_alpha",m,params=exc_dict)

  nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii, syn_dict_ii)
  nest.Connect(exc, inh, conn_dict_ei, syn_dict_ei)
  nest.Connect(inh, exc, conn_dict_ie, syn_dict_ie)

  filename = "random_exc_inh_test.pdf"
  nodes = [exc,inh]
  colors = ["lightpink","powderblue"]
  visualize.plot_network(nodes, colors, filename)

tock = time.time()
print("Total elapsed time = %.3fs"%(tock-tick))