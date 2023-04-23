import dpdata
import numpy as np
cp2kmd_dir = '.'
data=dpdata.LabeledSystem(cp2kmd_dir, cp2k_output_name='ll_out', fmt='cp2kdata/md')
data.to_deepmd_raw('deepmd')
data.to_deepmd_npy('deepmd')
