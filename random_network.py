import nest
import pylab
import numpy as np
import visualize

n = 6
N = 2*n
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

multimeter = nest.Create("multimeter", n)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeter, exc)

spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(exc,spikedetector)

nest.Simulate(1000.0)

dmm = nest.GetStatus(multimeter)[0]
Vms = dmm["events"]["V_m"]
ts_v = dmm["events"]["times"]
dSD = nest.GetStatus(spikedetector,keys="events")[0]
evs = dSD["senders"]
ts_s = dSD["times"]