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

p_ee = 0.07925 # before 0.1
p_ii = 0.317 # before 0.4
p_ei = 0.07925
p_ie = 0.317
# note currently must keep q_ee = q_ei and q_ii = q_ie
q_ee = 0.3#0.475
q_ii = 0.3#0.325
q_ei = 0.3#0.475
q_ie = 0.3#0.325

conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
conn_dict_ii = {'rule': 'pairwise_bernoulli', 'p': p_ii, "autapses" : False}
conn_dict_ei = {'rule': 'pairwise_bernoulli', 'p': p_ei, "autapses" : False}
conn_dict_ie = {'rule': 'pairwise_bernoulli', 'p': p_ie, "autapses" : False}
syn_spec = [{"delay": 1.0, "weight": 150.0}, {"delay": 1.0, "weight": -150.0}]
conn_spec_q = [{'rule':'pairwise_bernoulli','p':q_ee}, {'rule':'pairwise_bernoulli','p':q_ii}]

start_seed = 100005
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

real_connect_before = np.zeros(R)
real_connect_after = np.zeros(R)

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})
  exc = nest.Create("iaf_psc_alpha",n)
  inh = nest.Create("iaf_psc_alpha",m)

  nest.Connect(exc, exc, conn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii)
  nest.Connect(exc, inh, conn_dict_ei)
  nest.Connect(inh, exc, conn_dict_ie)

  real_connect_before[i] =len(nest.GetConnections())
  # filename = "twostep_test_before.pdf"
  # nodes = [exc,inh]
  # colors = ["lightpink","powderblue"]
  # visualize.plot_network(nodes, colors, filename)
  
  control_flow.twostep_connect(n,m,q_ee,syn_spec)

  real_connect_after[i] =len(nest.GetConnections())

  # filename = "twostep_test_after.pdf"
  # visualize.plot_network(nodes, colors, filename)

ee_before = n*(n-1)*p_ee
ii_before = m*(m-1)*p_ii
ei_before = n*m*p_ei
ie_before = n*m*p_ie

ee_after = ee_before*(1+(1-p_ee)*q_ee)
ii_after = ii_before*(1+(1-p_ii)*q_ii)
ei_after = ei_before+n*m*p_ie*(1-p_ei)*q_ei
ie_after = ie_before+n*m*p_ei*(1-p_ie)*q_ie

print(ee_before+ii_before+ei_before+ie_before)
print(np.mean(real_connect_before))

print(ee_after+ii_after+ei_after+ie_after)
print(np.mean(real_connect_after))

tock = time.time()
print('Elapsed time  = %.3f s'%(tock-tick))