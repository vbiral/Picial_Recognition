#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

import getpass
import RPi.GPIO as gpio
from picamera.array import PiRGBArray
from picamera import PiCamera

def verifica_resposta_valida(pergunta):
    while(1):
        resp = input(pergunta)
        if(resp != 'S' and resp != 's' and resp != 'N' and resp != 'n'):
            print('Resposta Invalida! Tente Novamente!!!!!')
        else:
            break
    resp = resp.upper()
    return resp

def modo_administrador(users, camera, classificador, classificadorolho, rawCapture):
    user = str()
    password = str()
    print('########## Modo Administrativo ##########')

    while(1):
        user = input('Usuario: ')
        password = getpass.getpass('Senha: ')
        if(users[user] == password):
            break
        else:
            print('Usuario ou senha incorretas!!!!!')
            resp = verifica_resposta_valida()
            if(resp == 'S'):
                return 1
    
    while(1):
        print('#### Acesso Concedido ####')
        print('1. Criar novo usuário')
        print('2. Apagar Rosto')
        print('3. Gravar Rosto')
        print('4. Abrir Fechadura')
        print('5. Sair')
        q = input('Escolha uma das opcoes: ')

        if(q == '1'):
            while(1):
                user = input('Usuario: ')
                password = getpass.getpass('Senha: ')
                confirmacao = getpass.getpass('Confirme a senha: ')
                if(password == confirmacao):
                    novo_usuario(user, password)
                    break
                else:
                    print('Senha e confirmacao nao batem!!!!!')
                    resp = verifica_resposta_valida('Deseja tentar novamente?[S/N] ')
                    if(resp == 'N'):
                        break

        elif(q == '2'):
            print('apagar_rosto()')

        elif(q == '3'):
            id = input('Nome: ')
            gravar_rosto(id, camera, classificador, classificadorolho, rawCapture)
                
        elif(q == '4'):
            gpio.output(12, 0)
            
        else:
            return 1
    return 1

def modo_vigilancia(camera, classificador, classificadorolho, rawCapture):
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    
        imagem = frame.array    
        imagemcinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        facesdetectadas = classificador.detectMultiScale(imagemcinza, scaleFactor=1.5, minSize=(100,100))

        #if(facesdetectadas[2] * facesdetectadas[3] != 0):
        
    
        for (x,y,l,a) in facesdetectadas:
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 2)

        cv2.imshow('Face', imagem)

    
        #Botão para cancelar a execução
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if (key==ord("q")):
            break


def ler_users():
    arq = open('/home/pi/Documents/users.txt', 'r')
    users = arq.readlines()
    senhas = {}
    for i in range(len(users)):
        if(i < len(users)-1):
            users[i] = users[i][:-1]
            usuario = users[i][:users[i].find(',')]
            password = users[i][1+users[i].find(','):]
            senhas[usuario] = password
        else:
            usuario = users[i][:users[i].find(',')]
            password = users[i][1+users[i].find(','):]
            senhas[usuario] = password
    return senhas


def novo_usuario(novo_user, nova_pass):
    arq = open('/home/pi/Documents/users.txt', 'a')

    nova_linha = '\n' + novo_user + ',' + nova_pass
    arq.writelines(nova_linha)

    arq.close()
    print('Usuario ' + novo_user + ' adicionado!!!')
    return 1

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

def gravar_rosto(id, camera, classificador, classificadorolho, rawCapture):
    amostra = 1
    numeroamostras = 25
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
        camera.release()
        cv2.destroyAllWindows() 

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
