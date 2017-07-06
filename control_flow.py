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

def twostep_connect(net,p):
  raw_connect = nest.GetConnections(net)
  l = len(raw_connect)
  set_connect = np.zeros([l,2],dtype = int)
  flip_connect = np.zeros([l,2],dtype = int)
  for i in np.arange(l):
  	set_connect[i] = [raw_connect[i][0],raw_connect[i][1]]
  	flip_connect[i] = [raw_connect[i][1],raw_connect[i][0]]
  conn_spec = {'rule':'pairwise_bernoulli','p':p}
  syn_spec = {"delay": 1.0, "weight": 150.0}
  for i in np.arange(l):
  	if flip_connect[i] not in set_connect:
  	  nest.Connect([net[flip_connect[i][0]-1]],[net[flip_connect[i][1]-1]],conn_spec,syn_spec)