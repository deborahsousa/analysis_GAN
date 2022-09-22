import numpy as np # package de manipulação de listas e matrizes
from numpy import random
import matplotlib.pyplot as plt
import PlotFrequenciaDemanda
from matplotlib.pyplot import cm

a = [0,0]
b = [1000,5000]
c = [5000,10000]
d = [10000,45000]
e = [45000,80000]
#probabilidades de cada intervalo a,b,c,d,e
p_CP = [0.74,0.01,0.035,0.155,0.06]
intervals_vector = [a,b,c,d,e] # vetor com os intervalos
intervals = [0,1,2,3,4] # vetor com número a ser selecionado aleatoriamente
dias_sim = 2000 # dias de simulação na estação seca
num_farmers = 20
vol_retirada = np.zeros((dias_sim,num_farmers)) # vetor de volume retirado a cada dia

for k in range(num_farmers):
    for i in range(dias_sim):
        index = np.random.choice(intervals, p=p_CP)
        my_interval = intervals_vector[index]
        vol_retirada[i,k] = np.random.uniform(my_interval[0],my_interval[1])

x = np.arange(0,dias_sim)


for j in range(num_farmers):
    plt.plot(x,vol_retirada[:,j])

plt.show()
f = 1.0


titulo_grafico = 'CP - histograma'
l_CP = vol_retirada.flatten()
sorted_l_CP = sorted(l_CP)
PlotFrequenciaDemanda.PlotHistCategoria(l_CP, titulo_grafico)