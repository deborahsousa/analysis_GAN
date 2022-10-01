import numpy as np # package de manipulação de listas e matrizes

my_perc = np.empty((22,8))
categoria = 'NC'
for j in range(8):
    my_list = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')

categoria = 'CI'
for j in range(8):
    my_list = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')

categoria = 'CP'
for j in range(8):
    my_list = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')