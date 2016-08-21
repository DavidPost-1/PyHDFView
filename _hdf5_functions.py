# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 14:16:03 2016

@author: Dave
"""

def print_keys(item):   
    if isinstance(item, h5py.Group):
        print(item.name)
        for i in item.keys():
            if isinstance(item[i], h5py.Dataset):
                print('{}*'.format(item[i].name))
                
            elif isinstance(item[i], h5py.Group):
                print_keys(item[i])
                
            else:
                print("Invalid format")

    else:
        print("item should be a h5py.Group object.")
            
    
# open the hdf5 file
def get_structure():
    with h5py.File('test2.hdf5', 'w') as hdf5_file:
        # Create a dataset
        hdf5_file.create_dataset('test_dataset', data = np.arange(0,100,0.1))
        
        
        # Create a group
        grp = hdf5_file.create_group('test_group')
        grp.attrs.create('test', data=3)
        
        grp.create_group('inner group')
        grp['inner group'].create_dataset('inner dataset', data=[1,2,3])
        #grp['inner group'].attrs.create('test', '3')
        
                      
        print_keys(hdf5_file)
        print('\n* = dataset')