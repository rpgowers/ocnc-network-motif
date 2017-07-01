import numpy as np

def voltage_save(dmm,n):
  ts_v = dmm[0]["events"]["times"][0::n]
  Vms = np.zeros([n,len(ts_v)])
  for i in np.arange(n):
    Vms[i] = dmm[0]["events"]["V_m"][i::n]
    
  return ts_v, Vms