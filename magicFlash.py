from skimage import io
import tifffile as tif
import numpy as np
import scipy
import matplotlib

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

    diff1 = scipy.ndimage.gaussian_filter(res2, sigma)
    diff2 = scipy.ndimage.gaussian_filter(b2, sigma)
    b0 = diff2 >  0
    filt_image = b2.copy()
    filt_image[b0] = diff1[b0]/diff2[b0]
    filt_image = filt_image * b2
    filt_image[np.logical_not(b0)] = res2[np.logical_not(b0)]
    return filt_image

def compute_shadows(ambiant, flash):
    hsv1 = matplotlib.colors.hsv_to_rgb(ambiant)[:,:,2]
    hsv2 = matplotlib.colors.hsv_to_rgb(flash)[:,:,2]
    hsv1 = scipy.ndimage.gaussian_filter(hsv1, 6)
    hsv2 = scipy.ndimage.gaussian_filter(hsv2, 6)

    v0 = hsv2 != 0
    
    res = hsv1.copy()
    res[v0] = hsv1[v0]/hsv2[v0]
    m = np.average(res[v0])
    res[v0] = res[v0]/m
    res[np.logical_not(v0)] = 1
    res[res < 0] = 1

    res2 = 0.2 * np.log(res)

    res3 = ambiant.copy()
    pos2 = res2 > 0
    neg2 = res2 <= 0

    zeros = np.zeros(
        (res2.shape[0], res2.shape[1],)
    )

    res3[neg2, 0] = -res2[neg2]
    res3[neg2, 1] = zeros[neg2]
    res3[neg2, 2] = zeros[neg2]

    res3[pos2, 0] = zeros[pos2]
    res3[pos2, 1] = res2[pos2]
    res3[pos2, 2] = zeros[pos2]

    return res3 

a = tif.imread("D:/images/fillfllash/Capture/xxx0000.tif")
b = tif.imread("D:/images/fillfllash/Capture/xxx0001.tif")

a = a[:,:,0:3]
b = b[:,:,0:3]
    
a = a.astype(np.float64)
b = b.astype(np.float64)


s = a.shape
maxv = 65535
c = 16.0/16.0
    
#a = a[400:2800, 500:4500,:]
#b = b[400:2800, 500:4500,:]

a = a/maxv
b = b/maxv

res = 20*(b - a)
sup0(res)

filter_r = filter_diff(res, b, 0, 5.8)
filter_g = filter_diff(res, b, 1, 5.8) 
filter_b = filter_diff(res, b, 2, 5.8)

img3 = np.stack(
    [filter_r, filter_g, filter_b], axis=2
)
shadows = compute_shadows(a, b)
tif.imsave('D:/images/fillfllash/Capture/only_flash.tif', uint16_gamma(res))
tif.imsave('D:/images/fillfllash/Capture/clean_result.tif', uint16_gamma(img3))
tif.imsave('D:/images/fillfllash/Capture/shadows.tif', uint16_gamma(shadows))