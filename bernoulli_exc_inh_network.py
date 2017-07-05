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

exc_dict = {"I_e": 50.0, "tau_m": 20.0}
inh_dict = {"I_e": 50.0, "tau_m": 20.0}

p_ee = 0.1
p_ii = 0.1
p_ei = 0.1
p_ie = 0.4

conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
conn_dict_ii = {'rule': 'pairwise_bernoulli', 'p': p_ii, "autapses" : False}
conn_dict_ei = {'rule': 'pairwise_bernoulli', 'p': p_ei, "autapses" : False}
conn_dict_ie = {'rule': 'pairwise_bernoulli', 'p': p_ie, "autapses" : False}

d = 1.0
Jee = 100
Jii = -100
Jei = 100
Jie = -100

syn_dict_ee = {"delay": d, "weight": Jee}
syn_dict_ii = {"delay": d, "weight": Jii}
syn_dict_ei = {"delay": d, "weight": Jei}
syn_dict_ie = {"delay": d, "weight": Jie}

start_seed = 100002
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

  filename = "bernoulli_exc_inh_test.pdf"
  nodes = [exc,inh]
  colors = ["lightpink","powderblue"]
  visualize.plot_network(nodes, colors, filename)