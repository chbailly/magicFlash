from skimage import io
import tifffile as tif
import numpy as np
import scipy

def moy(img):
    return (img[:,:,0] + img [:,:,1] + img[:,:,2])/3

def norm(img):
    sup0(img)
    index = (img >=1)
    img[index] = 1

def sup0(img):
    index = img < 0
    img[index] = 0

def apply_gamma_colour(colour):
    dark = colour < 0.018
    bright = colour >= 0.018
    colour[dark] = 4.5 * colour[dark]
    
    colour[bright] = 1.099 * np.power(colour[bright],0.45) - 0.099
    return colour

def apply_gamma(img):
    return np.stack(
        [apply_gamma_colour(img[:,:,0]),
        apply_gamma_colour(img[:,:,1]),
        apply_gamma_colour(img[:,:,2])], axis=2)

def uint16_gamma(img):
    res = apply_gamma(img)
    norm(res)
    res = res * 65535
    res = res.astype(np.uint16)
    return res

def filter_diff(res, b, colour, sigma):
    res2 = res[:,:,colour]
    b2 = b[:,:,colour]
    b0 = b2 != 0
    b_diff = b2.copy()
    b_diff[b0] = res2[b0] /  b2[b0]

    b_diff2 = scipy.ndimage.gaussian_filter(b_diff,sigma)
    b_diff2 =  b_diff2 * b2
    b_diff2[np.logical_not(b0)] = res2[np.logical_not(b0)]
    return b_diff2

a = tif.imread("D:/images/fillfllash/Capture/xxx0000.tif")
b = tif.imread("D:/images/fillfllash/Capture/xxx0001.tif")

a = a[:,:,0:3]
b = b[:,:,0:3]
    
a = a.astype(np.float64)
b = b.astype(np.float64)


s = a.shape
maxv = 65535
c = 16.0/16.0
    
a = a[400:2800, 500:4500,:]
b = b[400:2800, 500:4500,:]

a = a/maxv
b = b/maxv

res = 20*(b - a)
        
filter_r = filter_diff(res, b, 0, 6)
filter_g = filter_diff(res, b, 1, 6) 
filter_b = filter_diff(res, b, 2, 6)

img3 = np.stack(
    [filter_r, filter_g, filter_b], axis=2
)

tif.imsave('D:/images/fillfllash/Capture/only_flash.tif', uint16_gamma(res))
tif.imsave('D:/images/fillfllash/Capture/clean_result.tif', uint16_gamma(img3))