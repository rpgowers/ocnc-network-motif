import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages

def voltage_extract(dmm,n,plot=False):
  ts_v = dmm[0]["events"]["times"][0::n]
  Vms = np.zeros([n,len(ts_v)])
  for i in np.arange(n):
    Vms[i] = dmm[0]["events"]["V_m"][i::n]
  if plot == True:
    with PdfPages('voltage_plot.pdf') as pdf:
      plt.xlabel('Time (ms)')
      plt.ylabel('Membrane Voltage (mV)')
      plt.plot(ts_v,Vms.T)
      pdf.savefig()

  return ts_v, Vms

def voltage_psd(ts_v,Vms,plot=False):
  n = len(Vms)
  timestep = (ts_v[1]-ts_v[0])/1000
  freq = np.fft.rfftfreq(len(ts_v), d=timestep)
  P = np.zeros([n,len(freq)])
  for i in np.arange(n):
    F = np.fft.rfft(Vms[i]-np.mean(Vms[i]))
    P[i] = abs(F)**2

  return P