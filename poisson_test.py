import nest
import numpy as np
import visualize
import data_analysis
import control_flow

msd = 123456
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
nest.SetKernelStatus({'grng_seed' : msd+N_vp})
nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

n,T_ms,R = control_flow.common_args()

poisson_dict = {'rate' : 10.0, 'origin' : 0.0}
nest.Create("poisson_generator",n=1, params=poisson_dict)
