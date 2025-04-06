# This is the algorithm I have created to identify odd pattern in an array
# Ex: [0,0,0,1,1,0,1,0] 
# In this 1 is supposed to be odd pattern so we should have two segments [3,4] and [6,6]
# We check the average value of the entire array 
# If the segment surrounded by 0 if the average exceeds global average we consider it as one segment

import unicodedata


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
                    reg.append([i-int(2*b),tmp+int(2*b)])
                    i=j
                    break

        i+=1
    return reg

def break_region(arr):
    lp=[]
    for i in range(len(arr)-1):
        lp.append(arr[i+1][1]-arr[i][0])
    return lp.index(max(lp))


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch) and unicodedata.category(ch)[0] != "C")


import cv2
import numpy as np

def find_and_mark_regions(image_path):
  img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  img_o2 = cv2.imread(image_path, cv2.IMREAD_COLOR)
  _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)  # Simple threshold
  sample_rows=[2,3,4,6,7]
  scale=[]
  markers=[]
  for i in sample_rows:
    mid_y=int(binary_img.shape[0]/4)
    region=segmentation(binary_img[mid_y],0)
    brk=break_region(region)
    scale.append(region[brk][1])
    markers.append(region[brk+1][0])

  row=binary_img.shape[0]
  col=binary_img.shape[1]
  m2=max(scale)+int(max(scale)/4)
  m3=min(markers) -int(max(markers)/4)

# Drawing lines to check the working of the algo
# Cv2.line takes opposite (column,row) arguments than we take other wise

  # cv2.line(img_o2,(0,0),(0,row),(0, 255, 0),2)
  # cv2.line(img_o2,(m2,0),(m2,row),(0, 255, 0),2)
  # cv2.line(img_o2,(m3,0),(m3,row),(0, 255, 0),2)
  # cv2.line(img_o2,(col,0),(col,row),(0, 255, 0),2)

  cv2.imwrite("/content/scale_image.jpg", binary_img[:,0:m2])
  cv2.imwrite("/content/marker_image.jpg", binary_img[:,m3:col])
  return(binary_img[:,0:m2],binary_img[:,m3:col])



image_file = "/content/lm 4.jpg"  # Replace with the actual image path.

bi_s,bi_m=find_and_mark_regions(image_file)

import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r'/usr/bin/tesseract'
)

from PIL import Image

extracted_text = pytesseract.image_to_string(bi_m)
data = pytesseract.image_to_data(bi_s, output_type=pytesseract.Output.DICT, config='--psm 11')

text_data = []
for i in range(len(data['text'])):
    if data['text'][i]:  # Check for non-empty text
        text_data.append({
            'text': data['text'][i],
            'top': data['top'][i]  # Y-coordinate of the bounding box
        })

sorted_text = sorted(text_data, key=lambda x: x['top'])
final_text = '\n'.join([item['text'] for item in sorted_text])

print(final_text.split("\n"))

cleaned_extract = [remove_control_characters(item) for item in extracted_text.split("\n")]
cleaned_extract_f=[]
for i in cleaned_extract:
  if i.replace(' ',''):
    cleaned_extract_f.append(i)
print(cleaned_extract_f)
