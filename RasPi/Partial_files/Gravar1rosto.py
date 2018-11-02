#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import das bibliotecas e funções necessárias
import cv2
import funcoes
import numpy as np
import os
import RPi.GPIO as gpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#Configurações iniciais GPIOs
gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #Pino da trinca

#Configurações Inicias da detecção de rostos
classificador = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
classificadorolho = cv2.CascadeClassifier("haarcascade-eye.xml")
camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture = PiRGBArray(camera, size=(640,480))

id = 2
amostra = 1
numeroamostras = 10
largura = 200
altura = 200
print('Capturando as faces...')

while(1):
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        imagem = frame.array    
        imagemcinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        print(np.average(imagemcinza))

        facesdetectadas = classificador.detectMultiScale(imagemcinza, scaleFactor=1.5, minSize=(150,150))

        for (x,y,l,a) in facesdetectadas:
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 2)
            regiao = imagem[y:y + a, x:x + l]
            regiaocinzaolho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)

            olhosdetectados = classificadorolho.detectMultiScale(regiaocinzaolho)

            for(ox, oy, ol, oa) in olhosdetectados:
                cv2.rectangle(regiao, (ox, oy), (ox+ol, oy+oa), (0, 255, 0), 2)

                if(cv2.waitKey(1) & 0xFF == ord('q')):
                    if(np.average(imagemcinza) > 110):
                        imagemface = cv2.resize(imagemcinza[y:y + a, x:x + l], (largura, altura))
                        cv2.imwrite('fotos/pessoa.' + str(id) + '.' + str(amostra) + '.jpg', imagemface)
                        print('Foto ' + str(amostra) + 'capturada com sucesso!')
                        amostra = amostra+1
        cv2.imshow('Face', imagem)
        cv2.waitKey(1)
        if(amostra >= numeroamostras + 1):
                break
        rawCapture.truncate(0)
    print('Faces capturadas om sucesso')
    cv2.destroyAllWindows() 

