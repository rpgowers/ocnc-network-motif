import nest
import numpy as np
import sys
import visualize
import data_analysis
import argparse

parser = argparse.ArgumentParser(description='Network arguments')
parser.add_argument(type=int, dest='neurons', help='number of neurons')
args = parser.parse_args()
n = args.neurons


noise_dict = {'mean' : 0.0, 'std' : 20.0, 'dt' : 1.0}
current_noise = nest.Create('noise_generator', n=1, params=noise_dict)

#n = 2
ndict = {"I_e": 100.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
multimeter = nest.Create("multimeter", n=1)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})

nest.Connect(current_noise,exc)
nest.Connect(multimeter,exc)

T_ms = 300.0

nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)