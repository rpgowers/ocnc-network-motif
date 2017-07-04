import nest
import numpy as np
import visualize
import data_analysis
import control_flow

# nest.ResetKernel();
msd = np.random.randint(100000)
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
nest.SetKernelStatus({'grng_seed' : msd+N_vp})
nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

n, T_ms = control_flow.common_args()
N = n
p = 0.2
ndict = {"I_e": 250.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
conn_dict_ee = {'rule': 'fixed_total_number', 'N': N, "autapses" : False}
conn_dict_bern = {'rule': 'pairwise_bernoulli', 'p': p, "autapses" : False}

Jee = 20.0
d = 1.0
syn_dict_ee = {"delay": d, "weight": Jee}
nest.Connect(exc, exc, conn_dict_ee, syn_dict_ee)

filename = "random_exc_test.pdf"
nodes = [exc]
colors = ["lightpink"]
visualize.plot_network(nodes, colors, filename)

multimeter = nest.Create("multimeter", 1)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeter, exc)

spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(exc,spikedetector)

nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)
PSD = data_analysis.voltage_psd(ts_v,Vms,plot=True)

dSD = nest.GetStatus(spikedetector,keys="events")[0]

data_analysis.spike_plot(dSD)

ISI = data_analysis.isi_extract(dSD,n,plot=True)
print(len(ISI[0]),len(ISI[1]))