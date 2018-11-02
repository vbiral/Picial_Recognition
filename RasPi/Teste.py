#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import das bibliotecas e funções necessárias
import cv2
import funcoes
import RPi.GPIO as gpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#Configurações iniciais GPIOs
gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #Pino da trinca
gpio.output(12, 1)



#Configurações Inicias da detecção de rostos
classificador = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
classificadorolho = cv2.CascadeClassifier("haarcascade-eye.xml")
camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture = PiRGBArray(camera, size=(640,480))

timer_a = time.time()
users=funcoes.ler_users()

resp = funcoes.verifica_resposta_valida('Deseja entrar no modo administrador?[S/N] ')
        

if(resp == 'S' or time.time() - timer_a > 60):
    funcoes.modo_administrador(users, camera, classificador, classificadorolho, rawCapture)
    funcoes.modo_vigilancia(camera, classificador, classificadorolho, rawCapture)
else:
    funcoes.modo_vigilancia(camera, classificador, classificadorolho, rawCapture)

