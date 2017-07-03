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
      plt.close()

  return ts_v, Vms

def voltage_psd(ts_v,Vms,plot=False):
  n = len(Vms)
  timestep = (ts_v[1]-ts_v[0])/1000
  N = len(ts_v)
  freq = np.fft.rfftfreq(len(ts_v), d=timestep)
  P = np.zeros([n,len(freq)])
  for i in np.arange(n):
    F = np.fft.rfft(Vms[i]-np.mean(Vms[i]))*timestep
    P[i] = abs(F)**2
  if plot == True:
    with PdfPages('voltage_psd_plot.pdf') as pdf:
      plt.xlabel('Frequency (Hz)')
      plt.ylabel('Power Spectral Density ($\mu$V/Hz)')
      plt.plot(freq,P.T)
      pdf.savefig()
      plt.close()

  return P

def isi_extract(dSD,n,plot=False):
  evs = dSD["senders"]
  ts_s = dSD["times"]
  isi = []
  for i in 1+np.arange(n):
    idx = np.where(evs==i)[0]
    isi.append(np.diff(ts_s[idx]))
  isi = np.vstack(isi) # this will break if the neurons don't have the same number of spikes
  if plot == True:
    with PdfPages('isi_histogram.pdf') as pdf:
      plt.hist(isi.flatten())
      pdf.savefig()
      plt.close()
  return isi


def spike_plot(dSD):
  evs = dSD["senders"]
  ts_s = dSD["times"]
  with PdfPages('raster_plot.pdf') as pdf:
    plt.plot(ts_s,evs,'.')
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron Number")
    pdf.savefig(bbox_inches='tight')
    plt.close()