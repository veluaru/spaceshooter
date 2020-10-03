import cv2
import numpy as np
#import time
#import matplotlib.pyplot as plt
    
#Definimos los rangos del color a que necesitamos
Low = np.array([100, 100, 20])
High = np.array([125, 255, 255])
spacecraftPosition=0

cap = cv2.VideoCapture(0) # Es la camara por defecto del ordenador.

while (True): #Mientras la camara se encuentre abierta se realizará la lectura de los frames
     ret, frame = cap.read() # capturamos un frame
     frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
     fil = frame.shape[0]  #capturamos las dimensiones de l frame
     col = frame.shape[1]  #capturamos las dimensiones de l frame
     # las coordenas en x de las lineas usadas para los umbrales
     limit_right = int((col + 150) / 2)
     limit_left = int((col - 150) / 2)

     # Linea derecha
     cv2.line(frame, (limit_right, 0), (limit_right, fil), (255, 255, 255), 2)
     # Linea izquierda
     cv2.line(frame, (limit_left, 0), (limit_left, fil), (255, 255, 255), 2)
     
     #Se crea una mascara para dejar resaltado solo los colores que nos interesan
     mask = cv2.inRange(frameHSV, Low, High)
     
     #Se sacan los contornos de los objetos de nuestro color
     contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     
     #Se recorren los contornos para dibujar una linea alrededor del objeto que nos interesa
     for contor in contornos: #Recorremos todos los contornos azules encontrados
        area = cv2.contourArea(contor) #Obtenemos el area de los contornos
        
        if area > 1500: #Solo los mayores a 700
            # Buscamos las coordenadas del centro
            centros = cv2.moments(contor)
            
            if (centros["m00"] == 0): centros["m00"] = 1
            x = int(centros["m10"] / centros["m00"])
            y = int(centros["m01"] / centros["m00"])
            cordeX = x # coordenada x del contorno
            cordeY = y # coordenada y del contorno
            # Dibujamos un circulo con las coordenadas del contorno
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1) # 7 es el radio del circulo
            # Luego de eliminar los contorno menores a cierta area, vamos a suavizar los contornos
            contorSuavi = cv2.convexHull(contor) #suavizamos los contornos
            cv2.drawContours(frame, [contorSuavi], 0, (255, 0, 0), 3) #dibujamos los contornos
    
     if (cordeX > 0 and cordeX < limit_left):
        car_x_change = -0.7 #indica que la bolita se encuentra en el segmento izquierdo y por lo tanto el usuario desea mover el vehiculo en esta dirección
     if (cordeX >= limit_left and cordeX <= limit_right):
        car_x_change = 0 #indica que la bolita se encuentra en el segmento centro y por lo tanto el usuario desea no mover el vehiculo en ninguna dirección
     if (cordeX > limit_right and cordeX < col): #indica que la bolita se encuentra en el segmento derecho y por lo tanto el usuario desea mover el vehiculo en esta dirección
        car_x_change = 0.7
     
     cv2.imshow('frame',frame)#Mostramos el frame
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release() #Se cierra la camara
cv2.destroyAllWindows() #Se cierran todas las ventanas