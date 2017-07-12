import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow
nest.sli_run("M_WARNING setverbosity")

tick = time.time()

name = 'twostep_ei_equiprob'
data_dir = 'raw_data'

n, T_ms, R = control_flow.common_args()
m = int(n/4)

exc_dict = {"I_e": 0.0, "tau_m": 20.0}
inh_dict = {"I_e": 0.0, "tau_m": 20.0}

# note currently must keep q_ee = q_ei and q_ii = q_ie
q = 1.0
q_ee = q
q_ii = q
q_ei = q
q_ie = q
p_old = 0.1 # p value of homogeneously connected network
p = ((1+q)-np.sqrt((1+q)**2-4*p_old*q))/(2*q)
print(p)
p_ee = p
p_ii = p
p_ei = p
p_ie = p

ee_before = n*(n-1)*p_ee
ii_before = m*(m-1)*p_ii
ei_before = n*m*p_ei
ie_before = n*m*p_ie
#print(ee_before+ii_before+ei_before+ie_before)

ee_after = ee_before*(1+(1-p_ee)*q_ee)
ii_after = ii_before*(1+(1-p_ii)*q_ii)
ei_after = ei_before+n*m*p_ie*(1-p_ei)*q_ei
ie_after = ie_before+n*m*p_ei*(1-p_ie)*q_ie
print(ee_after+ii_after+ei_after+ie_after)

conn_dict_ee = {'rule': 'pairwise_bernoulli', 'p': p_ee, "autapses" : False}
conn_dict_ii = {'rule': 'pairwise_bernoulli', 'p': p_ii, "autapses" : False}
conn_dict_ei = {'rule': 'pairwise_bernoulli', 'p': p_ei, "autapses" : False}
conn_dict_ie = {'rule': 'pairwise_bernoulli', 'p': p_ie, "autapses" : False}

d = 1.0
Jee = 40
Jii = -40*4
Jei = 40
Jie = -40*4

syn_dict_ee = {"delay": d, "weight": Jee}
syn_dict_ii = {"delay": d, "weight": Jii}
syn_dict_ei = {"delay": d, "weight": Jei}
syn_dict_ie = {"delay": d, "weight": Jie}

conn_spec_q = [{'rule':'pairwise_bernoulli','p':q_ee}, {'rule':'pairwise_bernoulli','p':q_ii}]
syn_spec_q = [{"delay": d, "weight": Jee}, {"delay": d, "weight": Jii}]

poisson_dict = {'rate' : 1200.0, 'origin' : 0.0}
conn_dict_poisson = {'rule': 'all_to_all'}
syn_dict_poisson = {"delay": 1.0, "weight": 20.0}

Vpop_mean_exc = np.zeros([int(T_ms)-1])
Vpop_var_exc = np.zeros([int(T_ms)-1])
Vpop_mean_inh = np.zeros([int(T_ms)-1])
Vpop_var_inh = np.zeros([int(T_ms)-1])

raw_spikes_exc = 0 # number of total excitatory spikes
raw_spikes_inh = 0 # number of total inhibitory spikes

real_connect_after = np.zeros(R)

start_seed = 100000
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]

for i in np.arange(R):
  nest.ResetKernel()
  msd = start_seed + i
  nest.SetKernelStatus({'grng_seed' : msd+N_vp})
  nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

  exc = nest.Create("iaf_psc_alpha",n,params=exc_dict)
  inh = nest.Create("iaf_psc_alpha",m,params=inh_dict)
  random_vals = np.random.rand(n+m)*15-70
  for k,j in enumerate(exc+inh):
    nest.SetStatus([j],{'V_m' : random_vals[k]})
  # first step of connections
  nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)
  nest.Connect(inh, inh, conn_dict_ii, syn_dict_ii)
  nest.Connect(exc, inh, conn_dict_ei, syn_dict_ei)
  nest.Connect(inh, exc, conn_dict_ie, syn_dict_ie)
  # second step of connections
  control_flow.twostep_connect(n,m,q_ee,syn_spec_q)
  real_connect_after[i] =len(nest.GetConnections())

  poisson_noise = nest.Create("poisson_generator", n=1, params=poisson_dict)
  multimeter_exc = nest.Create("multimeter", n=1, params={"withtime":True, "record_from":["V_m"]})
  multimeter_inh = nest.Create("multimeter", n=1, params={"withtime":True, "record_from":["V_m"]})
  spikedetector_exc = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
  spikedetector_inh = nest.Create("spike_detector", params={"withgid": True, "withtime": True})

  nest.Connect(poisson_noise,exc,conn_dict_poisson,syn_dict_poisson)
  nest.Connect(poisson_noise,inh,conn_dict_poisson,syn_dict_poisson)
  nest.Connect(multimeter_exc,exc)
  nest.Connect(multimeter_inh,inh)
  nest.Connect(exc,spikedetector_exc)
  nest.Connect(inh,spikedetector_inh)

  nest.Simulate(T_ms)

  dmm_exc = nest.GetStatus(multimeter_exc)
  dmm_inh = nest.GetStatus(multimeter_inh)
  ts_v, Vms_exc = data_analysis.voltage_extract(dmm_exc,n,plot=False)
  ts_v, Vms_inh = data_analysis.voltage_extract(dmm_inh,m,plot=False)

  Vpop_mean_exc += np.mean(Vms_exc,axis=0)/R # population mean of excitatory neurons
  Vpop_var_exc += np.var(Vms_exc,axis=0)/R # population variance of excitatory neurons
  Vpop_mean_inh += np.mean(Vms_inh,axis=0)/R # population mean of excitatory neurons
  Vpop_var_inh += np.var(Vms_inh,axis=0)/R # population variance of excitatory neurons

  dSD_exc = nest.GetStatus(spikedetector_exc,keys="events")[0]
  ts_s_exc = dSD_exc["times"]
  send_exc = dSD_exc["senders"]
  dSD_inh = nest.GetStatus(spikedetector_inh,keys="events")[0]
  ts_s_inh = dSD_inh["times"]
  send_inh = dSD_inh["senders"]
  raw_spikes_exc += len(ts_s_exc)
  raw_spikes_inh += len(ts_s_inh)
  # save spikes
  np.save('%s/%s_raw_exc_spikes_q=%s_R=%s'%(data_dir,name,q_ee,i),np.array([ts_s_exc,send_exc]).T)
  np.save('%s/%s_raw_inh_spikes_q=%s_R=%s'%(data_dir,name,q_ee,i),np.array([ts_s_inh,send_inh]).T)

print(np.mean(real_connect_after))
print(raw_spikes_exc/(n*R*T_ms/1000))
print(raw_spikes_inh/(m*R*T_ms/1000))

# voltage mean and variance with time
data = np.array([ts_v,Vpop_mean_exc,Vpop_var_exc]).T
np.savetxt('%s/%s_vmom_epop_q=%s.txt'%(data_dir,name,q_ee),data)
data = np.array([ts_v,Vpop_mean_inh,Vpop_var_inh]).T
np.savetxt('%s/%s_vmom_ipop_q=%s.txt'%(data_dir,name,q_ee),data)

tock = time.time()
print('Elapsed time = %.3f'%(tock-tick))