import nest
import numpy as np
import sys
import visualize
import data_analysis

#ST_ms = float(sys.argv[0]) # need to fix with argparse

n = 2
N = 1*n
ndict = {"I_e": 250.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
conn_dict_ee = {'rule': 'fixed_total_number', 'N': N, "autapses" : False}

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

T_ms = 100.0

nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)
PSD = data_analysis.voltage_psd(ts_v,Vms,plot=True)

dSD = nest.GetStatus(spikedetector,keys="events")[0]
evs = dSD["senders"]
ts_s = dSD["times"]

data_analysis.spike_plot(ts_s,evs)