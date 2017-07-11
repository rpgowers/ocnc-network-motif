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

  return P,freq

def mean_voltage_psd(ts_v,Vms,plot=False):
  timestep = (ts_v[1]-ts_v[0])/1000
  N = len(ts_v)
  freq = np.fft.rfftfreq(len(ts_v), d=timestep)
  P = np.zeros([len(freq)])
  F = np.fft.rfft(Vms-np.mean(Vms))*timestep
  P = abs(F)**2
  if plot == True:
    with PdfPages('voltage_psd_plot.pdf') as pdf:
      plt.xlabel('Frequency (Hz)')
      plt.ylabel('Power Spectral Density ($\mu$V/Hz)')
      plt.plot(freq,P.T)
      pdf.savefig()
      plt.close()

  return P,freq

def st_extract(evs,ts_s,n,b):
  st = []
  for i in 1+np.arange(n)+b:
    idx = np.where(evs==i)[0]
    st.append(list(ts_s[idx]))
  return st

def isi_extract(dSD,n,plot=False):
  evs = dSD["senders"]
  ts_s = dSD["times"]
  isi = []
  for i in 1+np.arange(n):
    idx = np.where(evs==i)[0]
    isi.append(list(np.diff(ts_s[idx])))
  if plot == True:
    isi_plot = [item for sublist in isi for item in sublist]
    with PdfPages('isi_histogram.pdf') as pdf:
      plt.hist(np.array(isi_plot))
      pdf.savefig()
      plt.close()
  return isi

def spike_plot(name,dSD):
  evs = dSD["senders"]
  ts_s = dSD["times"]
  with PdfPages('raster_plot_%s.pdf'%(name)) as pdf:
    plt.plot(ts_s,evs,'.')
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron Number")
    pdf.savefig(bbox_inches='tight')
    plt.close()

def double_raster(name,ts_s_exc,send_exc,ts_s_inh,send_inh):
  with PdfPages('%s_double_raster.pdf'%(name)) as pdf:
    size = 2
    plt.plot(ts_s_exc,send_exc,'.',label='excitatory',markersize=size)
    plt.plot(ts_s_inh,send_inh,'.',label='inhibitory',markersize=size)
    plt.xlabel('Time (ms)')
    plt.ylabel('Neuron Number')
    plt.legend()
    pdf.savefig(bbox_inches='tight')
    plt.close()


def voltage_hist_plots(name,V_mean, V_var):
  with PdfPages('vmean_histogram_%s.pdf'%(name)) as pdf:
    plt.hist(V_mean)
    pdf.savefig()
    plt.close()
  with PdfPages('vvar_histogram_%s.pdf'%(name)) as pdf:
    plt.hist(V_var)
    pdf.savefig()
    plt.close()

def voltage_time_plots(name,Vpop_mean,Vpop_var,ts_v): # here V_pop is the population mean
  with PdfPages('%s_vpop_mean_time.pdf'%(name)) as pdf:
    plt.plot(ts_v,Vpop_mean)
    plt.xlabel('Time(ms)')
    plt.ylabel('Population Voltage Mean (mV)')
    pdf.savefig()
    plt.close()
  with PdfPages('%s_vpop_var_time.pdf'%(name)) as pdf:
    plt.plot(ts_v,Vpop_var)
    plt.xlabel('Time(ms)')
    plt.ylabel('Population Voltage Variance (mV^2)')
    pdf.savefig()
    plt.close()

def isi_hist_plot(name,isi):
  with PdfPages('isi_histogram_%s.pdf'%(name)) as pdf:
      plt.hist(np.array(isi))
      pdf.savefig()
      plt.close()

def psd_mean_plot(name,psd,freq):
  with PdfPages('psd_mean_%s.pdf'%(name)) as pdf:
      plt.plot(freq,psd)
      pdf.savefig()
      plt.close()

def spike_psd_plot(name,t,S):
  timestep = (t[1]-t[0])/1000
  N = len(t)
  freq = np.fft.rfftfreq(len(t), d=timestep)
  P = np.zeros([len(freq)])
  F = np.fft.rfft(S-np.mean(S))*timestep
  P = abs(F)**2
  with PdfPages('%s_spike_psd.pdf'%(name)) as pdf:
    plt.plot(freq,P)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Spike PSD')
    pdf.savefig()
    plt.close()

def pair_correlate(ind_st,time_bins):
  n = len(ind_st)
  hist_array = np.zeros([n,len(time_bins)-1])
  for i in np.arange(n):
    hist_array[i] = np.histogram(ind_st[i],bins=time_bins)[0]
        
  coeff_matrix = np.corrcoef(hist_array)
  coeff_vector = np.nan_to_num(coeff_matrix[np.tri(np.shape(coeff_matrix)[0],k=-1,dtype=bool)])
  return hist_array, coeff_vector

def coefficient_histogram(name,coeff_vector):
  with PdfPages('%s_coeff_hist.pdf'%(name)) as pdf:
    plt.hist(coeff_vector)
    plt.xlabel('Correlation coefficient')
    plt.ylabel('Number of occurrences')
    pdf.savefig()
    plt.close()