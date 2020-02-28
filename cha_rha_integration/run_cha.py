# from notebook create_connectivity_correlation_matrices.ipynb

import numpy as np
import glob, os
from os.path import exists, join

from mvpa2.base import externals
from mvpa2.base.param import Parameter
from mvpa2.base.constraints import *
from mvpa2.base.dataset import hstack, vstack
from mvpa2.base.types import is_datasetlike

from mvpa2.datasets import Dataset

from mvpa2.mappers.zscore import zscore
from mvpa2.mappers.fxy import FxyMapper
from mvpa2.mappers.svd import SVDMapper

from mvpa2.measures.searchlight import Searchlight
from mvpa2.measures.base import Measure

from mvpa2.algorithms.searchlight_hyperalignment import SearchlightHyperalignment
from mvpa2.algorithms.connectivity_hyperalignment import ConnectivityHyperalignment

# experimental sparse matrix usage for faster computing with possible extra mem load
# from searchlight_hyperalignment import SearchlightHyperalignment

from mvpa2.algorithms.hyperalignment import Hyperalignment

from mvpa2.support.due import due, Doi
import mvpa2.suite as mv

data_path = '/dartfs-hpc/scratch/psyc164/tcat/data/budapest/'
save_path = '/dartfs-hpc/scratch/psyc164/tcat/data'
hemis = ['L'] #'R'
subids = [5, 7, 9] #, 10, 13, 20, 21, 24, 29, 34, 52, 114, 120, 134, 142, 278, 416, 499, 522, 535, 560]
files = []

for hemi in hemis:
    for subid in subids:
        sub = '{:0>6}'.format(subid)
        fn = os.path.join(data_path + 'sub-rid' + sub + '*' + hemi + '.npy')
        files.append(sorted(glob.glob(fn)))

# import 
targets = range(1,21)
ds = None
for x in range(len(files)):
    d = Dataset(np.load(files[x][0]))#mv.gifti_dataset(files[x], targets=targets)
    if ds is None:
        ds = d
    else:      
        ds = vstack((ds,d))

# create subject labels and assign to dataset
chunk_list = np.repeat(range(len(subids)), (ds.shape[0]/len(subids))) # repeat subid for number of timepoints per sub
ds.sa['chunks'] = chunk_list
ds.fa['node_indices'] = range(ds.shape[1])
#zscore dataset in place
_ = zscore(ds)


ds.shape

radius = 100
surface =  mv.surf.read(join(data_path, '{0}.pial.gii'.format('lh')))
debug.active += ['SHPAL','SLC']

mask_ids = np.concatenate([
        np.arange(10242, dtype=int), np.arange(10242, dtype=int) + ds.shape[1]])
seed_indices = np.concatenate([
        np.arange(642, dtype=int), np.arange(642, dtype=int) + ds.shape[1]])
mask_ids = np.intersect1d(mask_ids, ds[0].fa.node_indices)

print('Starting CHA now')
hyper = ConnectivityHyperalignment(
    mask_node_ids=mask_ids,
    mask_ids=mask_ids,
    seed_indices=seed_indices,
    seed_queryengines=[mv.SurfaceQueryEngine(surface, 13.0)] * ds.shape[0],
    npcs=None,
    # npcs=3,
    queryengine=[mv.SurfaceQueryEngine(surface, 20.0)] * ds.shape[0],
    nproc=32,
    nblocks=128,
    compute_recon=False,
    featsel=1.0,
    dtype='float64')
mappers = hyper(ds)
h5save(savepath+'mappers2.hdf5.gz', mappers, compression=9)


