
### code to convert the sentinel 2 JP2 images into the tiff format###########

import os
import time
import Jp2_tiff_Converter as cnv


#######Set the Input and output path##################


inputPath = 'S2A_MSIL1C_20190608T092031_N0207_R093_T34SDF_20190608T105400.zip'
outputPath = ''

start_time = time.time()

cnv.generate_geotiffs(inputPath, outputPath)

print("--- %s seconds ---" % (time.time() - start_time))
#############################################################

#### convert the tiff image into jpg image###########
file_name = os.path.basename(inputPath)[:-4]+ "_PROCESSED"

##### Cut the images in the size of 786*786 and put into the folder###

from PIL import Image

infile = 'merged.jpg'
file_location = file_name+'/'+infile
chopsize = 610

img = Image.open(file_location)
width, height = img.size

if not os.path.exists(file_name+"/ChopedImages/ChopedImages"):
    os.makedirs(file_name+"/ChopedImages/ChopedImages")

# Save Chops of original image
for x0 in range(0, width, chopsize):
   for y0 in range(0, height, chopsize):
      box = (x0, y0,
             x0+chopsize if x0+chopsize <  width else  width - 1,
             y0+chopsize if y0+chopsize < height else height - 1)
      print('%s %s' % (infile, box))
      img.crop(box).save(file_name+'/ChopedImages/ChopedImages/zchop.%s.x%05d.y%05d.jpg' % (infile.replace('.jpg',''), x0, y0))

