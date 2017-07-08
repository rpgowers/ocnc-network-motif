import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow

nest.sli_run("M_WARNING setverbosity")

n, T_ms, R = control_flow.common_args()

p_ee = 0.1
q_ee = 0.99
conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

real_connect = np.zeros(R)

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

  #control_flow.twostep_connect(exc,q_ee)
  # try it manually ...
  raw_connect = nest.GetConnections(exc)
  l = len(raw_connect)
  
  set_connect = np.zeros([l,2],dtype = int)
  flip_connect = np.zeros([l,2],dtype = int)
  for j in np.arange(l):
    set_connect[j] = [raw_connect[j][0],raw_connect[j][1]]
    flip_connect[j] = [raw_connect[j][1],raw_connect[j][0]]
  conn_spec = {'rule':'pairwise_bernoulli','p':q_ee}
  syn_spec = {"delay": 1.0, "weight": 65.0}
  for j in np.arange(l):
    #if flip_connect[j] not in set_connect:
    if any((set_connect[:]==flip_connect[j]).all(1))==False:
      #print((flip_connect[j][0],flip_connect[j][1]))
      nest.Connect([exc[flip_connect[j][0]-1]],[exc[flip_connect[j][1]-1]],conn_spec,syn_spec)

  real_connect[i] = len(nest.GetConnections(exc))
  #print(real_connect[i])

  filename = "twostep_test_after.pdf"
  nodes = [exc]
  visualize.plot_network(nodes, colors, filename)

print(n*(n-1)*p_ee)
print(n*(n-1)*p_ee+n*(n-1)*p_ee*(1-p_ee)*q_ee)
print(np.mean(real_connect))