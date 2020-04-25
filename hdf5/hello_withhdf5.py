import h5py
import numpy as np
import datetime as dt


with h5py.File("file.hdf5", "w") as hdf_file:
    # crete a new dataset and store numpy array
    dataset = hdf_file.create_dataset(name='my_data', shape=(100,), dtype='i')
    dataset[...] = np.arange(100)
    group = hdf_file.create_group('group1')

    # add some metadata to group
    group.attrs['name'] = 'main group'

    # create dataset in group1
    train = np.random.random([100, 100])
    seg_ds = group.create_dataset('train', data=train)

    # we can easily create nested groups
    sub_group = group.create_group('subgroup1/subgroup11')
    ones_arr = np.ones((250, 5000))
    sub_dataset = sub_group.create_dataset('sensors', data=ones_arr)
    sub_dataset.attrs['sensor type'] = 'sensor IO'
    sub_dataset.attrs['date_taken'] = dt.datetime.now().isoformat()

    print("========TESTING=====")
    dset = sub_group.create_dataset("MyDataset", (10, 10, 10), 'f')
    print(dset[0, 0, 0])
    print(dset[0, 2:10, 1:9:3])
    print(dset[:, ::2, 5])
    print(dset[0])
    print(dset[1, 5])
    print(dset[0, ...])
    print(dset[..., 6])

with h5py.File('file.hdf5', 'r') as hdf_file:
    # show all objects in file
    # - my_data
    # - group1
    #       - subgroup1
    #           - subgroup11
    #               - sensors
    #       -train
    print("---FILE TREE---")
    hdf_file.visit(lambda name: print(name))

    # get data set
    print("\n---HDF_FILE.GET('MY_DATA')---")
    dataset = hdf_file.get('my_data')
    print(dataset[0:10])

    # get data set, another way
    print("\n---HDF_FILE.['MY_DATA']---")
    dset2 = hdf_file['my_data']
    print(dset2[0:10])

    # get gruoup
    print("\n---GET GROUP1'S ITEMS---")
    group = hdf_file['group1']
    group.items()

    # iterate over attributes
    print("\n--KEY:VALUE ATTRIBUTES OF GROUP---")
    for item in group.attrs.keys():
        print(f"{item}:{group.attrs[item]}")

    print("\n---KEYS IN FILE---")
    print(hdf_file.keys())
