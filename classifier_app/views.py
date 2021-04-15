from django.shortcuts import render
import pandas as pd
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
from keras.models import load_model,model_from_json
from keras.preprocessing import image
import json
# Create your views here.


def index(request):
    context={'a':1}
    return render(request,'classifier_app/index.html',context)


json_file = open('/home/prathamesh/Fire-Smoke-Detection-WebApp/models/model_mobilenet.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
nn_m = model_from_json(loaded_model_json)

nn_m.load_weights('/home/prathamesh/Fire-Smoke-Detection-WebApp/models/weights_mobilenet.h5')

def predictImage(request):
    print(request)
    print(request.POST.dict())
    fileobj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName=fs.save(fileobj.name,fileobj)
    filePathName=fs.url(filePathName)
    testimage= '/home/prathamesh/Fire-Smoke-Detection-WebApp'+filePathName
    img = image.load_img(testimage, target_size=(128, 128))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) /255.0
    classes = nn_m.predict(x)
    result_df = pd.DataFrame(list(nn_m.predict(x)[0]),index=['Fire','Neutral','Smoke'],columns=['result'])
    predictedLabel = result_df.result.idxmax()


    context={'filePathName':filePathName,'predictedLabel':'The classification of the image is: '+predictedLabel}
    return render(request,'classifier_app/index.html',context)

def viewDataBase(request):
    listOfImages = os.listdir('/home/prathamesh/Fire-Smoke-Detection-WebApp/media/')
    listOfImagesPath = ['/media/'+i for i in listOfImages]
    context={'listOfImagesPath':listOfImagesPath}
    return render(request,'classifier_app/viewDB.html',context)
