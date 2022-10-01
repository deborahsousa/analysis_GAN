import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import matplotlib.pyplot as plt # Plotagem de gráficos
from scipy.stats import skew

nivel_urubu = pd.read_csv('nivel_fozurubu.csv', sep=";", decimal=".")
nivel_urubu = np.array(nivel_urubu)
for i in range(len(nivel_urubu)):  # 37 columns, from 0 to 36
    if nivel_urubu[i, 1] == 'None':
        nivel_urubu[i, 1] = np.nan
nivel_urubu[:,1] = nivel_urubu[:,1].astype(np.float)

y_red = 220.0
y_yellow = 398.0
#d_red = 01/JULY
#d_yellow = 01/AUGUST

j = 169
for j in range(169,len(nivel_urubu)):
    if nivel_urubu[j,1] <= y_yellow:
        print('nivel amarelo atingido em '+str(nivel_urubu[j,0]))
    if nivel_urubu[j,1] <= y_red:
        print('nivel vermelho atingido em '+str(nivel_urubu[j,0]))


l = 1

#+' ('+str(-)+'dias do que a condição de data.'