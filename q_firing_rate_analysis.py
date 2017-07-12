import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mp
mp.rcParams.update({'font.size':14})

plot_dir = 'plots'

q  = np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
r_e = np.array([2.0791,2.9583,3.6594,4.7844,7.5184,8.1237,8.5508,10.9740,12.3657,14.2942,16.3136])
r_i = np.array([2.0573,2.8211,3.4152,4.3590,6.6523,7.1498,7.513,9.4613,10.6235,12.2320,13.9028])

with PdfPages('%s/q_firing_plot.pdf'%(plot_dir)) as pdf:
	plt.plot(q,r_e,'o',label='excitatory')
	plt.plot(q,r_i,'o',label='inhibitory')
	plt.xlabel('Second Step Probability, q')
	plt.ylabel('Mean Firing Rate (Hz)')
	plt.legend(loc='best')
	pdf.savefig(bbox_inches='tight')
	plt.close()