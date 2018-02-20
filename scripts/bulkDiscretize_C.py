"""
bulkDiscretize_C.py
===================

Bulk discretization of hdf5 formatted point cloud data.
"""
import sys
sys.path.insert(0, '../modules/')
import dataDiscretization as dd
import scipy as sp

#Whether or not we want to sum charge and add noise during discretization
CHARGE = True
NOISE = True

C_data = dd.bulkDiscretize('../data/tilt/C_40000_tilt.h5', 50, 50, 50, CHARGE, NOISE)
sp.sparse.save_npz('../data/tilt/50x50x50/CDisc_noise_40000_50x50x50_tilt.npz', C_data)

print (C_data.shape)
