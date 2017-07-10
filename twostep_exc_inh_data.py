import nest
import numpy as np
import time
import visualize
import data_analysis
import control_flow
nest.sli_run("M_WARNING setverbosity")

tick = time.time()

name = 'twostep_ei'
data_dir = 'raw_data'

n, T_ms, R = control_flow.common_args()
m = int(n/4)

exc_dict = {"I_e": 150.0, "tau_m": 20.0}
inh_dict = {"I_e": 150.0, "tau_m": 20.0}

p_ee = 0.07925 # before 0.1
p_ii = 0.317 # before 0.4
p_ei = 0.07925
p_ie = 0.317

ee_before = n*(n-1)*p_ee
ii_before = m*(m-1)*p_ii
ei_before = n*m*p_ei
ie_before = n*m*p_ie
# note currently must keep q_ee = q_ei and q_ii = q_ie
q_ee = 0.3
q_ii = 0.3
q_ei = 0.3
q_ie = 0.3

ee_after = ee_before*(1+(1-p_ee)*q_ee)
ii_after = ii_before*(1+(1-p_ii)*q_ii)
ei_after = ei_before+n*m*p_ie*(1-p_ei)*q_ei
ie_after = ie_before+n*m*p_ei*(1-p_ie)*q_ie
print(ee_after+ii_after+ei_after+ie_after)
