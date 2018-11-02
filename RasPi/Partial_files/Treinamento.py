import cv2
import numpy as np
import funcoes
import os

eigenface = cv2.createEigenFaceRecognizer()
#eigenface = cv2.face.EigenFaceRecognizer_create()
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
