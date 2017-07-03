import nest
import numpy as np
import visualize
import data_analysis
import control_flow

n, T_ms = control_flow.common_args()


sine_dict = {'amplitude' : 150.0, 'frequency' : 20.0}
oscillator = nest.Create('ac_generator', n = 1, params=sine_dict)

#n = 2
ndict = {"I_e": 150.0, "tau_m": 20.0}
exc = nest.Create("iaf_psc_alpha",n,params=ndict)
multimeter = nest.Create("multimeter", n=1)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})

nest.Connect(oscillator,exc)
nest.Connect(multimeter,exc)

#T_ms = 300.0
nest.Simulate(T_ms)

dmm = nest.GetStatus(multimeter)
ts_v, Vms = data_analysis.voltage_extract(dmm,n,plot=True)