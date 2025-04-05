# This is the algorithm I have created to identify odd pattern in an array
# Ex: [0,0,0,1,1,0,1,0] 
# In this 1 is supposed to be odd pattern so we should have two segments [3,4] and [6,6]
# We check the average value of the entire array 
# If the segment surrounded by 0 if the average exceeds global average we consider it as one segment
def segmentation(arr,odd_val):
    en_ar=[]
    for i in arr:
        if i==odd_val:
            en_ar.append(1)
        else:
            en_ar.append(0)
    b=sum(en_ar)/len(en_ar)
    k=0
    l=0
    p=0
    i=0
    reg=[]
    while i < (len(en_ar)):
        if en_ar[i]==1:
            k=0
            l=0
            for j in range(i, len(en_ar)):
                k+=en_ar[j]
                l+=1
                if (en_ar[j]==0 and k/l>b) or j==len(en_ar)-1:
                    tmp=j-1 if j!=len(en_ar)-1 else j
                    reg.append([i,tmp])
                    i=j
                    break
        i+=1
    return reg



# Here I take the Linkage map image and try to find and segmemtize different maps in an image
# I grayscale the image and take the mid portion of the image and use the above mentioned logic for segmentization
# I draw the lines to see whether the algorithm is able to segmentize the image
import cv2
import numpy as np

def find_and_mark_regions(image_path):
  img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  img_o2 = cv2.imread(image_path, cv2.IMREAD_COLOR)
  _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)  # Simple threshold
  mid_line=[]
  mid_y=int(binary_img.shape[0]/2)
  region=segmentation(binary_img[mid_y],0)
  row=binary_img.shape[0]
  col=binary_img.shape[1]
  print(region)
  for i in range(len(region)):
    cv2.line(img_o2,(region[i][0],0),(region[i][0],row),(0, 255, 0),1)
    cv2.line(img_o2,(region[i][1],0),(region[i][1],row),(255,0,255),1)
  cv2.line(img_o2,(0,mid_y),(img_o2.shape[1],mid_y),(255,0,255),1)
  cv2.imwrite("/content/marked_image.jpg", img_o2) 

      

image_file = "/content/linkage_map.png"  # Replace with the actual image path.
find_and_mark_regions(image_file)