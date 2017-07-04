import argparse

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