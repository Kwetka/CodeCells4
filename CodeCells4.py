import pygame
import sys
import numpy as np
import keyboard
import random
import os
import tkinter as tk
from tkinter import *

Width, Height = 650, 650
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('CodeCells')

root = Tk()
root.title("CodeCells")
root.geometry("100x50")

clock = pygame.time.Clock()
FPS = 1

pygame.init()
a = 70

AN = 7 #Энергия фотосинтеза
BN = 0.8 #КПД поедания добычи
CN = 1 #Отходы от добычи
DN = 1
MaxEnergy = 100 #Максимальная энергия клетки
myt = 98 #Вероятность сохранения генов

GenC = 23 #Набор генов при мутации
G = 25 #Кол-во генов

colr = 0,0,0
Xg, Yg = 0, 0
s = 9
GenLine = np.zeros(a)
plat = np.zeros((a , a))
Genome = np.zeros((a, a, 64))
RGB = np.zeros((a, a, 4))
POS = np.zeros((a, a))
Ert = np.zeros((a, a))
Mom = np.zeros((a, a))
Energy = np.zeros((a, a))

Xd,Yd,Wall,M = 0,0,0,0
ModeView = 3
View = plat[1][1]

def Spawn():
     for i in range(3,30):
         for c in range(3,30):
              plat[c][i] = 1
              Energy[c][i] = MaxEnergy
              for b in range(1,G+1):
                  Genome[c][i][b]= random.randint(1,23)
                  RGB[c][i][1],RGB[c][i][2],RGB[c][i][3] = random.randint(1,255),random.randint(1,255),random.randint(1,255)                 
     for i in range(3,30):
         for c in range(3,30):
              Mom[c][i]= 1

def MyBio(MyX,MyY,r1,r2,r3): #моя клетка
 plat[MyX][MyY] = 1
 RGB[MyX][MyY][1] = r1
 RGB[MyX][MyY][2] = r2
 RGB[MyX][MyY][3] = r3
 for b in range(1,G):
     if b < len(GenLine)+1:
        Genome[MyX][MyY][b] = GenLine[b-1]
     else: Genome[MyX][MyY][b] = 9
 Energy[MyX][MyY] = MaxEnergy
 Mom[MyX][MyY] = 1

GenLine = (20,13,21,16,21,22,2,3,22,2,23,7,22,3,6,18,1,14,10,15,20,10,17,6,22)

Spawn()

def MOVE_BIO():
    for i in range(1,a):
        for k in range(0,a):
            if plat[k][i] == 1:
                 Energy[k][i] -= 1
                 if Energy[k][i] <= 10 or Ert[k][i] >=50:
                     plat[k][i] = 0
                     if Ert[k][i] <= 60:
                         Ert[k][i] += 2
            else: RGB[k][i] = 0
            if Ert[k][i] >= 1:
                Ert[k][i] -= 0.01
            for P in range (1,3):            
             if plat[k][i] == 1 and POS[k][i] != 1:  #основные действия
                     global Xd,Yd,Wall
                     M = int(Mom[k][i])  
                     Wall = 0 
                     if (Genome[k][i][M] < 9 and Genome[k][i][M] >0) or (Genome[k][i][M] > 13 and Genome[k][i][M] <= 18):    
                      Wall = 0
                      if (Genome[k][i][M] == 1 or Genome[k][i][M] == 14 or Genome[k][i][M] == 5) and i!=a-1: #вниз
                        Xd = k 
                        Yd = i+1                       
                      if (Genome[k][i][M] == 1 or Genome[k][i][M] == 14 or Genome[k][i][M] == 5) and i==a-1: #вниз
                        Wall = 1  
                      elif (Genome[k][i][M] == 3 or Genome[k][i][M] == 16 or Genome[k][i][M] == 7) and i!=1: #вверх
                        Xd = k 
                        Yd = i-1
                      elif (Genome[k][i][M] == 3 or Genome[k][i][M] == 16 or Genome[k][i][M] == 7) and i==1: #вверх
                        Wall = 1
                      elif (Genome[k][i][M] == 2 or Genome[k][i][M] == 15 or Genome[k][i][M] == 6) and k!=a-1: #вправо
                        Xd = k+1
                        Yd = i
                      elif (Genome[k][i][M] == 2 or Genome[k][i][M] == 15 or Genome[k][i][M] == 6) and k==a-1: #вправо
                        Xd = 1
                        Yd = i
                      elif (Genome[k][i][M] == 4 or Genome[k][i][M] == 17 or Genome[k][i][M] == 8) and k==1: #влево
                        Xd = a-1
                        Yd = i
                      elif (Genome[k][i][M] == 4 or Genome[k][i][M] == 17 or Genome[k][i][M] == 8) and k!=1: #влево
                        Xd = k-1
                        Yd = i
                        #ХОЖДЕНИЕ
                      if plat[Xd][Yd] == 0 and Genome[k][i][M] < 5 and Wall != 1:                  
                                 plat[Xd][Yd] = 1
                                 plat[k][i] = 0
                                 POS[Xd][Yd] = 1
                                 Mom[Xd][Yd] = Mom[k][i]+1
                                 Energy[Xd][Yd] = Energy[k][i]- DN
                                 if int(Mom[k][i]) != G:
                                     Mom[Xd][Yd] = Mom[k][i]+1
                                 else: Mom[Xd][Yd] = 1
                                 Genome[Xd][Yd] = Genome[k][i]
                                 RGB[Xd][Yd] = RGB[k][i]
                                 Genome[k][i] = 0
                                 Genome[Xd][Yd][63]= 0 
                        #ПОЕДАНИЕ
                      elif plat[Xd][Yd] == 1 and (Genome[k][i][M] > 13 and Genome[k][i][M] < 18) and Wall != 1:   
                             Genome[Xd][Yd] = 0
                             POS[k][i] = 1
                             if int(Mom[k][i]) != G:                                 
                                 Mom[k][i] += 1
                             else:                                
                                 Mom[k][i] = 1
                             if Energy[k][i] < MaxEnergy:
                                Energy[k][i] += Energy[Xd][Yd]*BN
                             Energy[Xd][Yd] = 0
                             Genome[k][i][63]=2
                             Ert[Xd][Yd] += CN
                             plat[Xd][Yd] = 0
                      #СМОТРЕТЬ
                      elif (Genome[k][i][M] >4 and Genome[k][i][M] <9):
                           if Wall != 1:
                               if (RGB[Xd][Yd][1] == RGB[k][i][1]) and (RGB[Xd][Yd][2] == RGB[k][i][2]) and (RGB[Xd][Yd][3] == RGB[k][i][3]) and plat[k][i] == 1:
                                      View = 3
                               else:
                                      if Ert[Xd][Yd] >= 50:
                                          View = 5
                                      else: View = plat[Xd][Yd]                                     
                           else: 
                               View = 4
                           Mom[k][i]=Mom[k][i]+View
                           if Mom[k][i] >G:
                                 Mom[k][i] -= G-1
                      #ДЕЙСТВИЕ НЕ ОСУЩЕСТВИЛОСЬ
                      if POS[k][i] == 0:
                         if int(Mom[k][i]) != G:
                             Mom[k][i] = Mom[k][i]+1
                         else: Mom[k][i] = 1                                                                                               
                     elif Genome[k][i][M] >20 and Genome[k][i][M] <24:
                         if Energy[k][i] < MaxEnergy:
                             Energy[k][i] += AN
                             Genome[k][i][63]=1
                             POS[k][i] = 1
                         if int(Mom[k][i]) != G:
                            Mom[k][i] = Mom[k][i]+1
                         else: 
                            Mom[k][i] = 1              
                     elif Genome[k][i][M] >9 and Genome[k][i][M] <14:
                        if Genome[k][i][M] == 10:
                          if i!= a-1 and plat[k][i+1] == 0:        
                             Genome[k][i+1] = Genome[k][i]
                             Genome[k][i+1][63] = 4 
                             RGB[k][i+1] = RGB[k][i]
                             POS[k][i],POS[k][i+1] = 1, 1
                             if random.randint(1,100) > myt:
                                  b = random.randint(1,G)
                                  Genome[k][i+1][b] = random.randint(1,GenC)
                                  if b == GenC: Genome[k][i+1][b] = random.randint(GenC+1,GenC*2)
                                  b = random.randint(1,3)
                                  if random.randint(1,2) == 2: RGB[k][i+1][b] += 20
                                  else: RGB[k][i+1][b] -= 20
                                  if RGB[k][i+1][b] > 230: RGB[k][i+1][b] = 230
                                  if RGB[k][i+1][b] < 0: RGB[k][i+1][b] = 0
                             if int(Mom[k][i]) != G:
                                 Mom[k][i] += 1
                             else: 
                                 Mom[k][i] = 1
                             Mom[k][i+1] = 1
                             Energy[k][i] //= 2
                             Energy[k][i+1] = Energy[k][i]
                             plat[k][i+1] = 1
                          else: 
                             if int(Mom[k][i]) != G:
                                   Mom[k][i] = Mom[k][i]+1
                             else: 
                                 Mom[k][i] = 1
                        elif Genome[k][i][M] == 11:
                          if k!=a-1: 
                              if plat[k+1][i] == 0:       
                                     Genome[k+1][i] = Genome[k][i]
                                     Genome[k+1][i][63] = 4
                                     RGB[k+1][i] = RGB[k][i]
                                     POS[k][i],POS[k+1][i] = 1, 1
                                     if random.randint(1,100) > myt:
                                         b = random.randint(1,G)
                                         Genome[k+1][i][b] = random.randint(1,GenC)
                                         if b == GenC: Genome[k+1][i][b] = random.randint(GenC+1,GenC*2) 
                                         b = random.randint(1,3)
                                         if random.randint(1,2) == 2: RGB[k+1][i][b] += 20
                                         else: RGB[k+1][i][b] -= 20
                                         if RGB[k+1][i][b] > 230: RGB[k+1][i][b] = 230
                                         if RGB[k+1][i][b] < 0: RGB[k+1][i][b] = 0

                                     if int(Mom[k][i]) != G:
                                         Mom[k][i] += 1
                                     else: 
                                        Mom[k][i] = 1
                                     Mom[k+1][i] = 1
                                     Energy[k][i] //= 2
                                     Energy[k+1][i] = Energy[k][i]
                                     plat[k+1][i] = 1
                              else:
                                if int(Mom[k][i]) != G:
                                    Mom[k][i] = Mom[k][i]+1
                                else: 
                                 Mom[k][i] = 1
                          else: 
                              if plat[1][i] == 0:
                                Genome[1][i] = Genome[k][i]
                                Genome[1][i][63] = 4
                                RGB[1][i] = RGB[k][i]
                                POS[k][i],POS[1][i] = 1, 1
                                if random.randint(1,100) > myt:
                                     b = random.randint(1,G)
                                     Genome[1][i][b] = random.randint(1,GenC)
                                     if b == GenC: Genome[1][i][b] = random.randint(GenC+1,GenC*2)  
                                     b = random.randint(1,3)
                                     if random.randint(1,2) == 2: RGB[1][i][b] += 20
                                     else: RGB[1][i][b] -= 20
                                     if RGB[1][i][b] > 230: RGB[1][i][b] = 230
                                     if RGB[1][i][b] < 0: RGB[1][i][b] = 0

                                if int(Mom[k][i]) != G:
                                      Mom[k][i] += 1
                                else: 
                                     Mom[1][i] = 1
                                Mom[1][i] = 1
                                Energy[k][i] //= 2
                                Energy[1][i] = Energy[k][i]
                                plat[1][i] = 1
                              else:
                                if int(Mom[k][i]) != G:
                                    Mom[k][i] = Mom[k][i]+1
                                else: 
                                 Mom[k][i] = 1
                        elif Genome[k][i][M] == 12:
                          if i!= 1 and plat[k][i-1] == 0:        
                             Genome[k][i-1] = Genome[k][i]
                             Genome[k][i-1][63] = 4
                             RGB[k][i-1] = RGB[k][i]
                             POS[k][i],POS[k][i-1] = 1, 1
                             if random.randint(1,100) >myt:
                                  b = random.randint(1,G)
                                  Genome[k][i-1][b] = random.randint(1,GenC)
                                  if b == GenC: Genome[k][i-1][b] = random.randint(GenC+1,GenC*2)  
                                  b = random.randint(1,3)
                                  if random.randint(1,2) == 2: RGB[k][i-1][b] += 20
                                  else: RGB[k][i-1][b] -= 20
                                  if RGB[k][i-1][b] > 230: RGB[k][i-1][b] = 230
                                  if RGB[k][i-1][b] < 0: RGB[k][i-1][b] = 0

                             if int(Mom[k][i]) != G:
                                 Mom[k][i] += 1
                             else: 
                                 Mom[k][i] = 1
                             Mom[k][i-1] = 1
                             Energy[k][i] //= 2
                             Energy[k][i-1] = Energy[k][i]
                             plat[k][i-1] = 1
                          else: 
                             if int(Mom[k][i]) != G:
                                   Mom[k][i] = Mom[k][i]+1
                             else: 
                                 Mom[k][i] = 1     
                        elif Genome[k][i][M] == 13:
                          if k!=1: 
                              if plat[k-1][i] == 0:       
                                     Genome[k-1][i] = Genome[k][i]
                                     Genome[k-1][i][63] = 4
                                     RGB[k-1][i] = RGB[k][i]
                                     POS[k][i],POS[k-1][i] = 1, 1
                                     if random.randint(1,100) >myt:
                                         b = random.randint(1,G)
                                         Genome[k][i-1][b] = random.randint(1,GenC)
                                         if b == GenC: Genome[k][i-1][b] = random.randint(GenC+1,GenC*2)  
                                         b = random.randint(1,3)
                                         if random.randint(1,2) == 2: RGB[k-1][i][b] += 20
                                         else: RGB[k-1][i][b] -= 20
                                         if RGB[k-1][i][b] > 230: RGB[k-1][i][b] = 230
                                         if RGB[k-1][i][b] < 0: RGB[k-1][i][b] = 0

                                     if int(Mom[k][i]) != G:
                                         Mom[k][i] += 1
                                     else: 
                                        Mom[k][i] = 1
                                     Mom[k-1][i] = 1
                                     Energy[k][i] //= 2
                                     Energy[k-1][i] = Energy[k][i]
                                     plat[k-1][i] = 1
                              else:
                                if int(Mom[k][i]) != G:
                                    Mom[k][i] = Mom[k][i]+1
                                else: 
                                 Mom[k][i] = 1
                          else: 
                              if plat[a-1][i] == 0:
                                Genome[a-1][i] = Genome[k][i]
                                RGB[a-1][i] = RGB[k][i]
                                Genome[a-1][i][63] = 4
                                POS[k][i],POS[a-1][i] = 1, 1
                                if random.randint(1,100) >myt:
                                  b = random.randint(1,G)
                                  Genome[a-1][i][b] = random.randint(1,GenC)
                                  if b == GenC: Genome[a-1][i][b] = random.randint(GenC+1,GenC*2)  
                                  b = random.randint(1,3)
                                  if random.randint(1,2) == 2: RGB[a-1][i][b] += 20
                                  else: RGB[a-1][i][b] -= 20
                                  if RGB[a-1][i][b] > 230: RGB[a-1][i][b] = 230
                                  if RGB[a-1][i][b] < 0: RGB[a-1][i][b] = 0

                                if int(Mom[k][i]) != G:
                                      Mom[k][i] += 1
                                else: 
                                     Mom[1][i] = 1
                                Mom[a-1][i] = 1
                                Energy[k][i] //= 2
                                Energy[a-1][i] = Energy[k][i]
                                plat[a-1][i] = 1
                              else:
                                if int(Mom[k][i]) != G:
                                    Mom[k][i] = Mom[k][i]+1
                                else: 
                                 Mom[k][i] = 1
                     elif Genome[k][i][M] >17 and Genome[k][i][M] <21: #Корни
                             Genome[k][i][63]=3
                             POS[k][i] = 1 
                             if Ert[k][i] >= 10:
                                 Ert[k][i] -= 10 
                                 Energy[k][i] += 5
                             else: 
                                 Energy[k][i] += int(Ert[k][i])
                                 Ert[k][i] = 0 
                             if int(Mom[k][i]) != G:                                 
                                 Mom[k][i] += 1
                             else:                                
                                 Mom[k][i] = 1
                     elif Genome[k][i][M] == 9:
                         Mom[k][i] = 1
                     elif Genome[k][i][M] > GenC:
                         POS[k][i] = 1
                         Mom[k][i] = Genome[k][i][M]-GenC
            if Energy[k][i] <= 0:
                 plat[k][i] = 0
                             

def draw_bio():
    for i in range(1,a):
        for k in range(1,a):
            if plat[k][i] != 0:
                if Energy[k][i]*2 > 255:
                    colr = 0,255,0 
                else: colr = 0,Energy[k][i]*2,0
                if plat[k][i] == 2:
                    colr = 0,0,200
                pygame.draw.polygon(screen,colr,[[k*s+s/2,i*s+s/2],[k*s-s/2,i*s+s/2],[k*s-s/2,i*s-s/2],[k*s+s/2,i*s-s/2]])

def draw_bio3():
    for i in range(1,a):
        for k in range(1,a):
            if plat[k][i] != 0:
                colr = RGB[k][i][1],RGB[k][i][2],RGB[k][i][3]
                pygame.draw.polygon(screen,colr,[[k*s+s/2,i*s+s/2],[k*s-s/2,i*s+s/2],[k*s-s/2,i*s-s/2],[k*s+s/2,i*s-s/2]])

def draw_bio2():
    for i in range(1,a):
        for k in range(1,a):
            if plat[k][i] != 0:
                if Genome[k][i][63] == 1:
                    colr = 0,255,0
                if Genome[k][i][63] == 2:
                    colr = 255,0,0    
                if Genome[k][i][63] == 0:
                    colr = 0,0,0
                if Genome[k][i][63] == 3:
                    colr = 0,0,255
                if Genome[k][i][63] == 4:
                    colr = 255,255,0
                pygame.draw.polygon(screen,colr,[[k*s+s/2,i*s+s/2],[k*s-s/2,i*s+s/2],[k*s-s/2,i*s-s/2],[k*s+s/2,i*s-s/2]])

def draw_ert():
    for i in range(1,a):
        for k in range(1,a):
            colr = 255,255-Ert[k][i]*5,255-Ert[k][i]*5
            if Ert[k][i] >= 50:
               colr = 0,0,255
            pygame.draw.polygon(screen,colr,[[k*s+s/2,i*s+s/2],[k*s-s/2,i*s+s/2],[k*s-s/2,i*s-s/2],[k*s+s/2,i*s-s/2]])
while True:
 for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
 screen.fill((200,200,200))
 if ModeView != 5: 
     MOVE_BIO()   
 draw_ert() 
 if ModeView == 1: draw_bio()
 elif ModeView == 2: draw_bio2() 
 elif ModeView == 3 or ModeView == 5: draw_bio3()
 if keyboard.is_pressed('1'):
    ModeView = 1
 if keyboard.is_pressed('2'):
    ModeView = 2
 if keyboard.is_pressed('3'):
    ModeView = 3
 if keyboard.is_pressed('4'):
    ModeView = 4
 if keyboard.is_pressed('7'):
    ModeView = 7
 if keyboard.is_pressed('5'):
    ModeView = 5
 if ModeView == 5:
     if keyboard.is_pressed('d'):
         Xg += 1
     if keyboard.is_pressed('s'):
         Yg += 1
     if keyboard.is_pressed('a'):
         Xg -= 1
     if keyboard.is_pressed('w'):
         Yg -= 1
     if keyboard.is_pressed('space'):
         ModeView = 3
         print(Genome[Xg][Yg])
 pygame.draw.polygon(screen,(123,255,2),[[Xg*s+s/3,Yg*s+s/3],[Xg*s-s/3,Yg*s+s/3],[Xg*s,Yg*s-s/3]]) 
 pygame.display.update()
 pygame.time.delay(100)
 root.update()
 POS = np.zeros((a, a))