from keras.models import load_model

import keras.backend as K
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from skimage.io import imread,imshow
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import sys
import shutil
sys.path.insert(0, '/media/rudresh/New Volume 1/Air_bus/Airbus_S4/Code_Airbus')

import locateImg
K.clear_session()

#### customized loss function to evaluate the loss of model#############

def dice_loss(y_true, y_pred):
    smooth = 1.
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = y_true_f * y_pred_f
    score = (2. * K.sum(intersection) + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
    return 1. - score

def bce_logdice_loss(y_true, y_pred):
    return binary_crossentropy(y_true, y_pred) - K.log(1. - dice_loss(y_true, y_pred))

def dice_p_bce(in_gt, in_pred):
    return 1e-3*binary_crossentropy(in_gt, in_pred) - dice_coef(in_gt, in_pred)

def true_positive_rate(y_true, y_pred):
    return K.sum(K.flatten(y_true)*K.flatten(K.round(y_pred)))/K.sum(y_true)

def dice_coef(y_true, y_pred, smooth=1):
    intersection = K.sum(y_true * y_pred, axis=[1,2,3])
    union = K.sum(y_true, axis=[1,2,3]) + K.sum(y_pred, axis=[1,2,3])
    return K.mean( (2. * intersection + smooth) / (union + smooth), axis=0)


##########load the trained model my_model.h5 with the weight and configuration loaded on top of it  #########
model = load_model('my_model.h5', custom_objects={'bce_logdice_loss': bce_logdice_loss,'dice_coef':dice_coef,'true_positive_rate':true_positive_rate})




def load_model(inputPath):
    safe_file_name= os.path.basename(inputPath)[:-4]+ ".SAFE"
    file_name = os.path.basename(inputPath)[:-4]+ "_PROCESSED"
    cropped_image = file_name+"/ChopedImages"
    test_paths = os.listdir(cropped_image)
    
    if not os.path.exists(file_name+"/resultImages"):
        os.makedirs(file_name+"/resultImages")
    
    result_path = os.path.basename(inputPath)[:-4]+ "_PROCESSED"+"/resultImages"
    
    
    desired_batch_size=4
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
            cropped_image,
            target_size=(768, 768),
            color_mode="rgb",
            shuffle = False,
            class_mode='categorical',
            batch_size=desired_batch_size)
    
    filenames = test_generator.filenames
    nb_samples = len(filenames)
    test_generator.reset()
    probabilities = model.predict_generator(test_generator, steps = 
                                       np.ceil(nb_samples/desired_batch_size))
    
    for i in range(0,nb_samples):
        generated_image=np.reshape(probabilities[i], (768, 768))
        if(np.amax(generated_image)>0.4):
            cordinate_x =int(filenames[i][42:-11])
            cordinate_y =int(filenames[i][49:-4])
            x,y =(np.where(generated_image==np.amax(generated_image)))
            Actual_cordinate_x=cordinate_x+x[0]
            Actual_cordinate_y=cordinate_y+y[0]
            print(locateImg.getCoordinatesOfpixel(safe_file_name,Actual_cordinate_x,Actual_cordinate_y,10980,10980))
            print(filenames[i])
            shutil.copy(cropped_image+'/'+filenames[i], result_path+'/')
            plt.imsave(result_path+'/'+filenames[i][13:-4]+'_location_'+str(Actual_cordinate_x)+','+str(Actual_cordinate_y)+'.jpg', generated_image)


