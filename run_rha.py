import numpy as np
import pylab as pl
from os.path import join as pjoin
import mvpa2.suite as mv
import glob
from scipy.stats import zscore
from mvpa2.mappers.fx import mean_group_sample
from mvpa2.measures import rsa
from scipy.spatial.distance import pdist
import sys
import os
import re
from mvpa2.clfs.knn import kNN

from mvpa2.datasets import Dataset
from mvpa2.base.dataset import hstack, vstack


### Set paths, hemispheres, subject IDs, and append relavent npys to variable "files"

data_path = '/dartfs-hpc/scratch/psyc164/tcat/data/budapest/'
save_path = '/dartfs-hpc/scratch/psyc164/tcat/data'
hemis = ['lh'] #'lh'
subids = [5, 7, 9] #, 10, 13, 20, 21, 24, 29, 34, 52, 114, 120, 134, 142, 278, 416, 499, 522, 535, 560]
files = []

for hemi in hemis:
    for subid in subids:
        sub = '{:0>6}'.format(subid)
        fn = os.path.join(data_path + 'sub-rid' + sub + '*' + hemi + '.npy')
        files.append(sorted(glob.glob(fn)))
        
### Import npys listed in files into a pymvpa Dataset object

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


### Run Connectivity Hyperalignment on Dataset

#### Set mask ids and seed indices to efficiently sample
mask_ids = np.concatenate([
        np.arange(10242, dtype=int), np.arange(10242, dtype=int) + ds.shape[1]])
seed_indices = np.concatenate([
        np.arange(642, dtype=int), np.arange(642, dtype=int) + ds.shape[1]])
mask_ids = np.intersect1d(mask_ids, ds[0].fa.node_indices)

#### Create Custom Searchlight Query engine
# create custom searchlight queryengine
radius = 10
surface = mv.surf.read(pjoin(data_path, '{0}.pial.gii'.format('lh')))
query = mv.SurfaceQueryEngine(surface, radius, distance_metric='dijkstra')


#### Run Response Hyperalignment
slhyper = mv.SearchlightHyperalignment(radius=3, featsel=0.4, queryengine=query)
print 'set up searchlightHA'
mv.debug.active += ['SLC']
slhypmaps = slhyper(ds)
print 'here'

outfile = save_path + 'rsa_hypermaps'
np.save(outfile)