import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as compare_ssim
import cv2

def normalize8(I):
  mn = I.min()
  mx = I.max()
  mx -= mn
  I = ((I - mn)/mx) * 255
  return I.astype(np.uint8)

def main(path_to_original_image: str, path_to_painted_image: str, path_to_output_image: str):

    with_mask = np.array(plt.imread(f"{path_to_painted_image}")[:, :, :3])
    with_mask = normalize8(with_mask)
    without_mask = np.array(plt.imread(f"{path_to_original_image}")[:, :, :3])
    sz= (without_mask.shape[1], without_mask.shape[0])
    sz2 = (int(sz[0]/2),int(sz[0]/2))

    with_mask = cv2.resize(with_mask, sz)
    
    final_mask = with_mask[:,:,0]*0
    final_ = with_mask[:,:,0]*0
    for channel in range(3):
      grayA=without_mask[:,:,channel]
      grayB=with_mask[:,:,channel]
      grayA=cv2.GaussianBlur(grayA, (21, 21), 0)
      grayB=cv2.GaussianBlur(grayB, (21, 21), 0)
      
      (score, diff) = compare_ssim(grayA, grayB, full=True)
      final_=(final_+diff)/2
      
    cv2.normalize(final_,final_, 0,255,norm_type=cv2.NORM_MINMAX)
    final_ = (final_).astype("uint8")
    final_[final_<250]=0
    final_[final_>=250]=255
    final_ = (final_).astype("uint8")

    cv2.morphologyEx(final_,cv2.MORPH_OPEN, (8,8),final_, anchor=(0,0),iterations=2)
    cv2.morphologyEx(final_,cv2.MORPH_DILATE, (1,1),final_, iterations=13, anchor=(-1,-1))
    cv2.morphologyEx(final_,cv2.MORPH_ERODE, (2,2),final_, iterations=5, anchor=(0,0))

    final_[final_==255] = 1
    final_=np.bitwise_not(final_)
    final_[final_==1] = 255
    final_ = cv2.resize(final_, (sz[0], sz[1]))

    plt.imsave(f"{path_to_output_image}", final_, cmap='gray')
    sys.stdout.flush()
    return 0
  
if __name__ == "__main__":
   main(
        path_to_original_image="original.jpg",
        path_to_painted_image="painted.jpg",
        path_to_output_image="mask.jpg"
   )