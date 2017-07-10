import argparse
import nest
import numpy as np

def common_args():
  parser = argparse.ArgumentParser(description='Network arguments')
  parser.add_argument(type=int, dest='neurons', help='number of neurons')
  parser.add_argument(type=float, dest='sim_time', help='total simulation time in ms')
  parser.add_argument(type=int, dest='realisations', help='total number of realisations', nargs='?', default = 10)
  args = parser.parse_args()
  n = args.neurons
  T = args.sim_time
  R = args.realisations
  return n,T,R

def twostep_connect(n,conn_spec,syn_spec):
  raw_connect = nest.GetConnections()
  l = len(raw_connect)
  set_connect = np.zeros([l,2],dtype = int)
  flip_connect = np.zeros([l,2],dtype = int)
  for i in np.arange(l):
    set_connect[i] = [raw_connect[i][0],raw_connect[i][1]]
    flip_connect[i] = [raw_connect[i][1],raw_connect[i][0]]
  
  for i in np.arange(l):
    if any((set_connect[:]==flip_connect[i]).all(1))==False:
      if flip_connect[i][0] < n+1: # exc presynaptic neuron
        #print('excitatory')
        #print(flip_connect[i][0],flip_connect[i][1])
        nest.Connect([flip_connect[i][0]],[flip_connect[i][1]],conn_spec[0],syn_spec[0])
      else: # inh presynaptic neuron
        #print('inhibitory')
        #print(flip_connect[i][0],flip_connect[i][1])
        nest.Connect([flip_connect[i][0]],[flip_connect[i][1]],conn_spec[1],syn_spec[0])