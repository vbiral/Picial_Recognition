#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import das bibliotecas e funções necessárias
import cv2
import funcoes
import time

#Configurações Inicias da detecção de rostos
classificador = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
classificadorolho = cv2.CascadeClassifier("haarcascade-eye.xml")
camera = cv2.VideoCapture(0)

timer_a = time.time()
users=funcoes.ler_users()

resp = funcoes.verifica_resposta_valida('Deseja entrar no modo administrador?[S/N] ')
        

if(resp == 'S' or time.time() - timer_a > 60):
    funcoes.modo_administrador(users, camera, classificador, classificadorolho)
    funcoes.modo_vigilancia(camera, classificador, classificadorolho)
else:
    funcoes.modo_vigilancia(camera, classificador, classificadorolho)

