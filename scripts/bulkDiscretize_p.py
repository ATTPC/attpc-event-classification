"""
bulkDiscretize_p.py
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

p_data = dd.bulkDiscretize('../data/tilt/p_40000_tilt_largeEvts.h5', 20, 20, 20, CHARGE, NOISE)
sp.sparse.save_npz('../data/tilt/20x20x20/pDisc_40000_20x20x20_tilt_largeEvts.npz', p_data)

print (p_data.shape)
