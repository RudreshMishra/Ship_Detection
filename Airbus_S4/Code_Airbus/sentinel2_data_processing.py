
### code to convert the sentinel 2 JP2 images into the tiff format###########
import sys
import subprocess
import zipfile  
import os
import time
import readline, glob
from pathlib import Path

##########download the gdal merge file from the below link and import here ############
## https://svn.osgeo.org/gdal/trunk/gdal/swig/python/scripts/gdal_merge.py######
import gdal_merge


#######Set the Input and output path##################


inputPath = 'S2A_MSIL1C_20190516T105031_N0207_R051_T31VEC_20190516T125423.zip'
outputPath = ''

start_time = time.time()

generate_geotiffs(inputPath, outputPath)

print("--- %s seconds ---" % (time.time() - start_time))

#### convert the tiff image into jpg image###########

from pgmagick import Image
img = Image('SentinelTrueColor2.tiff') # Input Image
img.write('SentinelTrueColor2.jpg')  # Output Image

##### Cut the images in the size of 786*786 and put into the folder###

from PIL import Image

infile = 'SentinelTrueColor2.jpg'
chopsize = 768

img = Image.open(infile)
width, height = img.size
os.makedirs("ChopedImages")

# Save Chops of original image
for x0 in range(0, width, chopsize):
   for y0 in range(0, height, chopsize):
      box = (x0, y0,
             x0+chopsize if x0+chopsize <  width else  width - 1,
             y0+chopsize if y0+chopsize < height else height - 1)
      print('%s %s' % (infile, box))
      img.crop(box).save('ChopedImage/zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg',''), x0, y0))

