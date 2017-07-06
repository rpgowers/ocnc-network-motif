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

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()
  nest.SetKernelStatus({'dict_miss_is_error' : False})
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})
  exc = nest.Create("iaf_psc_alpha",n)

  nest.Connect(exc, exc, conn_dict_ee)

  raw_connect = nest.GetConnections(exc)
  l = len(raw_connect)
  set_connect = np.zeros([l,2],dtype = int)
  flip_connect = np.zeros([l,2],dtype = int)
  for i in np.arange(l):
  	set_connect[i] = [raw_connect[i][0],raw_connect[i][1]]
  	flip_connect[i] = [raw_connect[i][1],raw_connect[i][0]]
  conn_spec = {'rule':'pairwise_bernoulli','p':1.0}
  syn_spec = {"delay": 1.0, "weight": 150.0}
  for i in np.arange(l):
  	if flip_connect[i] not in set_connect:
  	  #nest.Connect(5,2,{'rule':'one_to_one'})
  	  nest.Connect(exc[flip_connect[i][0]-1],exc[flip_connect[i][1]-1],conn_spec)#,syn_spec)

  filename = "twostep_test.pdf"
  nodes = [exc]
  colors = ["lightpink","powderblue"]
  visualize.plot_network(nodes, colors, filename)