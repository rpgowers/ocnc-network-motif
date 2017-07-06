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
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})
  exc = nest.Create("iaf_psc_alpha",n)

  nest.Connect(exc, exc, conn_dict_ee)

  filename = "twostep_test_before.pdf"
  nodes = [exc]
  colors = ["lightpink","powderblue"]
  visualize.plot_network(nodes, colors, filename)

  control_flow.twostep_connect(exc,0.8)

  filename = "twostep_test_after.pdf"
  visualize.plot_network(nodes, colors, filename)