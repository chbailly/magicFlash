# magicFlash

Please look at the wiki to see the example images

## Problems with fill flash

The flash adds light which helps to brighten shadows and reduce the difference with ambiant light. 
It can not cancel the difference but it can be enough to make it neglectible. 
It also mixes white balances, so the shadows will be more affected by the flash while the other parts will have the white balance of the ambient light.

## Post processing

It is difficult to match exactly the intensity of shadows with a mask. Besides, the white balance of the shadows does not match exactly with the other parts of the image.
So most of the time, it will be difficult to reduce the contrast without any major unwanted visual impacts.

## an alternative

Shoot 2 images, one without flash and one with flash. You will be able to balance the images perfectly with a clean result

# How to use it

## shoot your images

## export to tiff and align them

Find below an example with dcraw and image_stack:
dcraw64.exe -W -T -4 DSC00169.ARW
dcraw64.exe -W  -T -4 DSC00170.ARW
align_image_stack.exe" -a xxx -C DSC00169.tiff DSC00170.tiff

## launch the script (change the name of the input files)

# The logic behind

Let's call:
* A: the ambient image
* F: the image with flash

## The pure flash image

provided the both images were shot with the exact same exposure settings, then the pure flash image is:
P = F - A
very simple... 

The result:
* shadows completely gone !!!
* new shadows can appear if the flash is not at the same location as the camera. In the examples posted, the built-in flash is moved on top right part of the body camera (Sony A6500), that's why some new shadows appear. Al so there is the shadows from the lens...
* We have now an image with only one white balance (from the flash). All the parts match perfectly (shadows or not)
* But it can be noisy....

## the clean image

Here is the trick.
P image is noisy but F is not. How can P can take advantage of this ??

P is F minus the ambient light, but it is relative so we wil consider instead P/F. It also includes the differences of the white balance.

So P/F in reality is not noisy, so we can smooth P/F very easily. Note that we smooth only the shadows, we do not smooth the details of the scene !!

So we compute a P/F for the red, green, blue channels independently and the tool computes:
F - (P/F) * F

But with a ratio P/F which is smoothed with a gaussian filter whose standard deviaton can be set. Again this does NOT smoot the details of the image, but it will have an impact on the edges of the shadows

# use for masking

It is possible to compute a shadow image which represents the relative difference, as explained above. 

# Possible uses

* Allow to acentuate the effects of a flash in bright sun light. This may be off camera flash 
* fill flash for a portrait, so disminish the effects of the shadow
* mix ambient/flash light at will





