import os 
import numpy as np 
from tqdm import tqdm 
from skimage import io 
from skimage import transform
from path import root_dir, mkdir_if_not_exist
import pandas as pd 

data_dir = os.path.join(root_dir, 'datasets')

train_img = 'images'
mask_gt = 'labels_converted'

train_img_dir = os.path.join(data_dir, train_img)
mask_gt_dir = os.path.join(data_dir,mask_gt)

train_img_ids = list()
if os.path.isdir(train_img_dir):
    train_img_ids = [fname.rsplit('.',maxsplit = 1)[0] for fname in os.listdir(train_img_dir)
                    if fname.endswith('.jpg')]
    train_img_ids.sort()

train_image_npy_prefix = 'train_img'
mask_gt_npy_prefix = 'mask_gt'

def load_image_by_ids(image_id, fname_fn, from_dir, output_size = None, return_size = False):
    img_fnames = fname_fn(image_id)
    if isinstance(img_fnames, str):
        img_fnames = [img_fnames, ]

    assert isinstance(img_fnames, tuple) or isinstance(img_fnames, list)

    images = []
    image_size = []

    for img_fname in img_fnames:
        img_fname = os.path.join(from_dir, img_fname)
        if not os.path.exists(img_fname):
            raise FileNotFoundError('Image {} does not exist'.format(img_fname))
        image = io.imread(img_fname)

        image_sizes = append(np.asarray(image.shape[:2]))

        if output_size: 
            image = transform.resize(image, (output_size,output_size),
                                    order = 1, mode = 'constant', cval = 0, clip = True, 
                                    preserve_range = True, anti_aliasing=True)
        image = image.astype(np.unit8)
        images.append(image)
    if return_size: 
        if len(images) == 1:
            return images[0], image_sizes[0]
        else:
            return np.stack(images,axis = -1), image_sizes
    if len(images) == 1:
        return images[0]
    else:
        return np.stack(images, axis = 1) #masks 

def load_images(image_ids, from_dir, output_size=None, fname_fn=None, verbose=True, return_size=False):
    images = []

    if verbose:
        print('loading images from', from_dir)

    if return_size:

        image_sizes = []
        for image_id in tqdm(image_ids):
            image, image_size = load_image_by_ids(image_id,
                                                 from_dir=from_dir,
                                                 output_size=output_size,
                                                 fname_fn=fname_fn,
                                                 return_size=True)
            images.append(image)
            image_sizes.append(image_size)

        return images, image_sizes


    else:
        for image_id in tqdm(image_ids):
            image = load_image_by_ids(image_id,
                                     from_dir=from_dir,
                                     output_size=output_size,
                                     fname_fn=fname_fn)
            images.append(image)

        return images

def load_training_images(output_size=None):
    suffix = '' if output_size is None else '_%d' % output_size
    images_npy_filename = os.path.join(train_img_dir, '%s%s.npy' % (train_image_npy_prefix, suffix))

    if os.path.exists(images_npy_filename):
        images = np.load(images_npy_filename)
    else:
        images = load_images(image_ids=train_img_ids,
                             from_dir=train_img_dir,
                             output_size=output_size,
                             fname_fn=lambda x: '%s.jpg' % x)
        images = np.stack(images).astype(np.uint8)
        np.save(images_npy_filename, images)
    return images

def load_training_masks(output_size=None):
    suffix = '' if output_size is None else '_%d' % output_size
    npy_filename = os.path.join(mask_gt_dir, 'train_masks%s.npy' % suffix)
    if os.path.exists(npy_filename):
        masks = np.load(npy_filename)
    else:
        masks = load_images(image_ids=train_img_ids,
                            from_dir=mask_gt_dir,
                            output_size=output_size,
                            fname_fn=lambda x: '%s_mask.jpg' % x)
        masks = np.stack(masks)
        np.save(npy_filename, masks)
    return masks

def load_training_data(output_size=None,
                       num_partitions=5,
                       idx_partition=0,
                       test_split=0.):
    x = load_training_images(output_size=output_size)
    y = load_training_masks(output_size=output_size)
    return partition_data(x=x, y=y, k=num_partitions, i=idx_partition, test_split=test_split)
    
def partition_data(x, y, k=5, i=0, test_split=1. / 6, seed=42):
    assert isinstance(k, int) and isinstance(i, int) and 0 <= i < k

    n = x.shape[0]

    n_set = int(n * (1. - test_split)) // k
    # divide the data into (k + 1) sets, -1 is test set, [0, k) are for train and validation
    indices = np.array([i for i in range(k) for _ in range(n_set)] +
                       [-1] * (n - n_set * k),
                       dtype=np.int8)

    np.random.seed(seed)
    np.random.shuffle(indices)

    valid_indices = (indices == i)
    test_indices = (indices == -1)
    train_indices = ~(valid_indices | test_indices)

    x_valid = x[valid_indices]
    y_valid = y[valid_indices]

    x_train = x[train_indices]
    y_train = y[train_indices]

    x_test = x[test_indices]
    y_test = y[test_indices]

    return (x_train, y_train), (x_valid, y_valid), (x_test, y_test)