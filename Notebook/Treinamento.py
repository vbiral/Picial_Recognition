# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:50:24 2018

@author: biral
"""

import cv2
import numpy as np
import os

def getimagemcomid():
    caminhos = [os.path.join('fotos',f) for f in os.listdir('fotos')]
    faces=[]
    ids=[]
    for caminhoimagem in caminhos:
        imagemface = cv2.cvtColor(cv2.imread(caminhoimagem),cv2.COLOR_BGR2GRAY)
        id = int(os.path.split(caminhoimagem)[-1].split('.')[1])
        print(id)
        ids.append(id)
        faces.append(imagemface)
    return np.array(ids), faces

eigenface = cv2.face.EigenFaceRecognizer_create()
fisherface = cv2.face.FisherFaceRecognizer_create()
lbph = cv2.face.LBPHFaceRecognizer_create()
                  
ids, faces = getimagemcomid() 
print('Treinando...')

eigenface.train(faces, ids)
eigenface.write('classificadorEigen.yml')

fisherface.train(faces, ids)
fisherface.write('classificadorFisher.yml')

lbph.train(faces, ids)
lbph.write('classificadorLBPH.yml')

print('Treinamento Realizado')
