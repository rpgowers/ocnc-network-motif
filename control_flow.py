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

def plotting_args():
  parser = argparse.ArgumentParser(description='Network arguments')
  parser.add_argument(type=str, dest='name', help='name of simulation')
  parser.add_argument(type=int, dest='neurons', help='number of neurons')
  parser.add_argument(type=float, dest='sim_time', help='total simulation time in ms')
  parser.add_argument(type=int, dest='realisations', help='total number of realisations', nargs='?', default = 10)
  parser.add_argument(type=str, dest = 'q_value', help = 'secondary connection probability')
  args = parser.parse_args()
  name = args.name
  n = args.neurons
  T = args.sim_time
  R = args.realisations
  q = args.q_value
  return name,n,T,R,q

def twostep_connect(n,m,q,syn_spec):
  raw_connect = nest.GetConnections()
  set_connect = np.array(raw_connect)[:,:2]
  
  adjmat = np.zeros([n+m,n+m])
  adjmat[set_connect[:,0]-1,set_connect[:,1]-1] = 1
  newmat = (adjmat.T-adjmat) > 0

  R = np.random.rand(int(newmat.sum()))
  ind = R > q
  row,col = np.where(newmat)
  newmat[row[ind],col[ind]] = 0

  pre,post = np.where(newmat)
  pre += 1
  post += 1
  pre_exc = pre[pre < n+1]
  post_exc = post[pre < n+1]
  pre_inh = pre[pre > n]
  post_inh = post[pre > n]
  #print(pre_exc)

  # exc_pre = []
  # exc_post = []
  # inh_pre = []
  # inh_post = []
  # for i in np.arange(l):
  #   if any((set_connect[:]==flip_connect[i]).all(1))==False:
  #     if flip_connect[i][0] < n+1: # exc presynaptic neuron
  #       exc_pre += [flip_connect[i][0]]
  #       exc_post += [flip_connect[i][1]]
  #       #nest.Connect([flip_connect[i][0]],[flip_connect[i][1]],conn_spec[0],syn_spec[0])
  #     else: # inh presynaptic neuron
  #       inh_pre += [flip_connect[i][0]]
  #       inh_post += [flip_connect[i][1]]
  #       #nest.Connect([flip_connect[i][0]],[flip_connect[i][1]],conn_spec[1],syn_spec[0])
  
  nest.Connect(pre_exc,post_exc,'one_to_one',syn_spec[0])
  nest.Connect(pre_inh,post_inh,'one_to_one',syn_spec[1])