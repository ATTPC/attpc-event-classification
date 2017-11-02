"""
Testing discretization modules
"""
import sys
sys.path.insert(0, '/home/taylor/Documents/independent-research/modules/')
import dataDiscretization as dd
import scipy as sp

#Whether or not we want to sum charge during discretization
CHARGE = False

C_data = dd.bulkDiscretize('/home/taylor/Documents/independent-research/data/20x20x20/C_40000.h5', 20, 20, 20, CHARGE)
sp.sparse.save_npz('/home/taylor/Documents/independent-research/data/20x20x20/CDisc_40000_nocharge.npz', C_data)

print (C_data.shape)
