import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

nest.sli_run("M_WARNING setverbosity")

n, T_ms, R = control_flow.common_args()
m = int(n/4)

p_ee = 0.1
p_ii = 0.4
q_ee = 0.5
q_ii = 0.5
conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
conn_dict_ii = {'rule': 'pairwise_bernoulli', 'p': p_ii, "autapses" : False}

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

real_connect = np.zeros(R)

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})
  exc = nest.Create("iaf_psc_alpha",n)
  inh = nest.Create("iaf_psc_alpha",m)

  nest.Connect(exc, exc, conn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii)

  filename = "twostep_test_before.pdf"
  nodes = [exc]
  colors = ["lightpink","powderblue"]
  visualize.plot_network(nodes, colors, filename)

  control_flow.twostep_connect(exc,q_ee)
  control_flow.twostep_connect(inh,q_ii)

  real_connect[i] = len(nest.GetConnections(exc))

  filename = "twostep_test_after.pdf"
  nodes = [exc]
  visualize.plot_network(nodes, colors, filename)

print(n*(n-1)*p_ee)
print(n*(n-1)*p_ee+n*(n-1)*p_ee*(1-p_ee)*q_ee)
print(np.mean(real_connect))