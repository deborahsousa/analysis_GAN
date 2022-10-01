#Programa que gera histogramas a partir de uma matriz de demanda de água (bombas)
#Déborah Santos de Sousa
#Mestrado PTARH/UnB

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import matplotlib.pyplot as plt # Plotagem de gráficos
from scipy.stats import skew

#Dados de entrada
## Demanda
info_vazao_dem = pd.read_csv('vazao_demanda_urubu.csv', sep=";", decimal=".")
info_vazao_dem = np.array(info_vazao_dem)
matrix_vazao_dem = info_vazao_dem[3:,:]
matriz_carac = info_vazao_dem[0:3,1:]
###Volume
#matrix_volume_dem = pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal=".")
matrix_volume_dem = pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal=".")
matrix_volume_dem = np.array(matrix_volume_dem)

#Funções
def ListaCategoriasSeca(matriz_carac,matriz_demanda):
    ix_seca1a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2018'] #índice da linha da data inicial da seca do ano 1
    ix_seca1b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2018'] #índice da linha da data final da seca do ano 1
    ix_seca2a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2019'] #índice da linha da data inicial da seca do ano 2
    ix_seca2b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2019'] #índice da linha da data final da seca do ano 2
    ix_seca3a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2020'] #índice da linha da data inicial da seca do ano 3
    ix_seca3b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2020'] #índice da linha da data final da seca do ano 3
    ix_seca4a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2021'] #índice da linha da data inicial da seca do ano 4
    ix_seca4b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2021'] #índice da linha da data final da seca do ano 4
    a = ix_seca1a[0]
    b = 1 + ix_seca1b[0]
    c = ix_seca2a[0]
    d = 1 + ix_seca2b[0]
    e = ix_seca3a[0]
    f = 1 + ix_seca3b[0]
    g = ix_seca4a[0]
    h = 1 + ix_seca4b[0]
    matriz_demanda = np.concatenate((matriz_demanda[a:b],matriz_demanda[c:d],matriz_demanda[e:f],matriz_demanda[g:h]))
    matriz_demanda = matriz_demanda[:,1:]
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda[i, j] >= 2.5e5:
                matriz_demanda[i, j] = np.nan

    #desconsiderar as colunas das bombas 38, 42 e 1

    ix_NC = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'NC'] #índices da matriz original e ordenada com perfil NC
    m_NC = matriz_demanda[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    l_NC = m_NC.flatten()
    l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
    sorted_l_NC = sorted(l_NC_nonan)

    ix_CP = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CP']
    m_CP = matriz_demanda[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CP = m_CP.flatten()
    l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
    sorted_l_CP = sorted(l_CP_nonan)

    ix_CI = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CI']
    m_CI = matriz_demanda[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CI = m_CI.flatten()
    l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
    sorted_l_CI = sorted(l_CI_nonan)

    return sorted_l_NC,sorted_l_CP,sorted_l_CI

def ListaCategoriasSecaAnual(matriz_carac,matriz_demanda):
    ix_seca1a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2018'] #índice da linha da data inicial da seca do ano 1
    ix_seca1b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2018'] #índice da linha da data final da seca do ano 1
    ix_seca2a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2019'] #índice da linha da data inicial da seca do ano 2
    ix_seca2b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2019'] #índice da linha da data final da seca do ano 2
    ix_seca3a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2020'] #índice da linha da data inicial da seca do ano 3
    ix_seca3b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2020'] #índice da linha da data final da seca do ano 3
    ix_seca4a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2021'] #índice da linha da data inicial da seca do ano 4
    ix_seca4b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2021'] #índice da linha da data final da seca do ano 4
    a = ix_seca1a[0]
    b = 1 + ix_seca1b[0]
    c = ix_seca2a[0]
    d = 1 + ix_seca2b[0]
    e = ix_seca3a[0]
    f = 1 + ix_seca3b[0]
    g = ix_seca4a[0]
    h = 1 + ix_seca4b[0]
    matriz_demanda1 = matriz_demanda[a:b]
    matriz_demanda1 = matriz_demanda1[:, 1:]
    matriz_demanda2 = matriz_demanda[c:d]
    matriz_demanda2 = matriz_demanda2[:, 1:]
    matriz_demanda3 = matriz_demanda[e:f]
    matriz_demanda3 = matriz_demanda3[:, 1:]
    matriz_demanda4 = matriz_demanda[g:h]
    matriz_demanda4 = matriz_demanda4[:, 1:]

    for i in range(0, len(matriz_demanda1)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda1[i, j] == 'None':
                matriz_demanda1[i, j] = np.nan
    matriz_demanda1 = matriz_demanda1.astype(np.float)
    for i in range(0, len(matriz_demanda1)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda1[i, j] >= 2.5e5:
                matriz_demanda1[i, j] = np.nan

    for i in range(0, len(matriz_demanda2)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda2[i, j] == 'None':
                matriz_demanda2[i, j] = np.nan
    matriz_demanda2 = matriz_demanda2.astype(np.float)
    for i in range(0, len(matriz_demanda2)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda2[i, j] >= 2.5e5:
                matriz_demanda2[i, j] = np.nan

    for i in range(0, len(matriz_demanda3)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda3[i, j] == 'None':
                matriz_demanda3[i, j] = np.nan
    matriz_demanda3 = matriz_demanda3.astype(np.float)
    for i in range(0, len(matriz_demanda3)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda3[i, j] >= 2.5e5:
                matriz_demanda3[i, j] = np.nan

    for i in range(0, len(matriz_demanda4)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda4[i, j] == 'None':
                matriz_demanda4[i, j] = np.nan
    matriz_demanda4 = matriz_demanda4.astype(np.float)
    for i in range(0, len(matriz_demanda4)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda4[i, j] >= 2.5e5:
                matriz_demanda4[i, j] = np.nan

    ix_NC = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'NC'] #índices da matriz original e ordenada com perfil NC
    ix_CP = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CP']
    ix_CI = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CI']

    #2018
    m_NC = matriz_demanda1[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    l_NC = m_NC.flatten()
    l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
    sorted_l_NC_1 = sorted(l_NC_nonan)

    m_CP = matriz_demanda1[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CP = m_CP.flatten()
    l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
    sorted_l_CP_1 = sorted(l_CP_nonan)

    m_CI = matriz_demanda1[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CI = m_CI.flatten()
    l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
    sorted_l_CI_1 = sorted(l_CI_nonan)

    #2019
    m_NC = matriz_demanda2[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    l_NC = m_NC.flatten()
    l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
    sorted_l_NC_2 = sorted(l_NC_nonan)

    m_CP = matriz_demanda2[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CP = m_CP.flatten()
    l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
    sorted_l_CP_2 = sorted(l_CP_nonan)

    m_CI = matriz_demanda2[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CI = m_CI.flatten()
    l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
    sorted_l_CI_2 = sorted(l_CI_nonan)

    #2020
    m_NC = matriz_demanda3[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    l_NC = m_NC.flatten()
    l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
    sorted_l_NC_3 = sorted(l_NC_nonan)

    m_CP = matriz_demanda3[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CP = m_CP.flatten()
    l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
    sorted_l_CP_3 = sorted(l_CP_nonan)

    m_CI = matriz_demanda3[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CI = m_CI.flatten()
    l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
    sorted_l_CI_3 = sorted(l_CI_nonan)

    #2021
    m_NC = matriz_demanda4[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    l_NC = m_NC.flatten()
    l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
    sorted_l_NC_4 = sorted(l_NC_nonan)

    m_CP = matriz_demanda4[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CP = m_CP.flatten()
    l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
    sorted_l_CP_4 = sorted(l_CP_nonan)

    m_CI = matriz_demanda4[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
    l_CI = m_CI.flatten()
    l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
    sorted_l_CI_4 = sorted(l_CI_nonan)

    return sorted_l_NC_1,sorted_l_CP_1,sorted_l_CI_1,sorted_l_NC_2,sorted_l_CP_2,sorted_l_CI_2,sorted_l_NC_3,\
           sorted_l_CP_3,sorted_l_CI_3,sorted_l_NC_4,sorted_l_CP_4,sorted_l_CI_4

def ListaCategoriasSecaAnual15d(matriz_carac,matriz_demanda,categoria):
    # retirando os caracteres de 'ano' da coluna 'data'
    lista_demanda_sem_ano = matriz_demanda[:,0]
    for i in range(len(lista_demanda_sem_ano)):
        elemento_sem_ano = lista_demanda_sem_ano[i].split('/')
        elemento_todo = elemento_sem_ano[0] + "/" + elemento_sem_ano[1]
        lista_demanda_sem_ano[i] = elemento_todo
    matriz_demanda[:,0] = lista_demanda_sem_ano

    #retirando as colunas das bombas com mais de 70% de dados igual a zero na seca
    matriz_demanda[:,[6,7,25,26,27,28,29,33,34]] = np.nan

    ix_sem1a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY'] #índice da linha da data inicial da semana 1
    ix_sem1b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/MAY'] #índice da linha da data final da semana 1
    ix_sem2a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '16/MAY'] #índice da linha da data inicial da semana 2
    ix_sem2b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/MAY'] #índice da linha da data final da semana 2
    ix_sem3a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/MAY'] #índice da linha da data inicial da semana 3
    ix_sem3b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/JUNE'] #índice da linha da data final da semana 3
    ix_sem4a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/JUNE'] #índice da linha da data inicial da semana 4
    ix_sem4b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '29/JUNE'] #índice da linha da data final da semana 4
    ix_sem5a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/JUNE'] #índice da linha da data inicial da semana 5
    ix_sem5b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/JULY'] #índice da linha da data final da semana 5
    ix_sem6a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/JULY'] #índice da linha da data inicial da semana 6
    ix_sem6b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '29/JULY'] #índice da linha da data final da semana 6
    ix_sem7a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/JULY'] #índice da linha da data inicial da semana 7
    ix_sem7b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '13/AUGUST'] #índice da linha da data final da semana 7
    ix_sem8a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/AUGUST'] #índice da linha da data inicial da semana 8
    ix_sem8b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST'] #índice da linha da data final da semana 8

    #definindo em variáveis os índices onde se encontram as datas definidas
    a = ix_sem1a
    b = ix_sem1b
    c = ix_sem2a
    d = ix_sem2b
    e = ix_sem3a
    f = ix_sem3b
    g = ix_sem4a
    h = ix_sem4b
    q = ix_sem5a
    j = ix_sem5b
    k = ix_sem6a
    l = ix_sem6b
    m = ix_sem7a
    n = ix_sem7b
    o = ix_sem8a
    p = ix_sem8b

    matriz_demanda1 = np.concatenate((matriz_demanda[a[0]:b[0]],matriz_demanda[a[1]:b[1]],matriz_demanda[a[2]:b[2]],matriz_demanda[a[3]:b[3]],matriz_demanda[a[4]:b[4]],matriz_demanda[a[5]:b[5]],matriz_demanda[a[6]:b[6]]))
    matriz_demanda1 = matriz_demanda1[:, 1:]
    matriz_demanda2 = np.concatenate((matriz_demanda[c[0]:d[0]],matriz_demanda[c[1]:d[1]],matriz_demanda[c[2]:d[2]],matriz_demanda[c[3]:d[3]],matriz_demanda[c[4]:d[4]],matriz_demanda[c[5]:d[5]],matriz_demanda[c[6]:d[6]]))
    matriz_demanda2 = matriz_demanda2[:, 1:]
    matriz_demanda3 = np.concatenate((matriz_demanda[e[0]:f[0]],matriz_demanda[e[1]:f[1]],matriz_demanda[e[2]:f[2]],matriz_demanda[e[3]:f[3]],matriz_demanda[e[4]:f[4]],matriz_demanda[e[5]:f[5]],matriz_demanda[e[6]:f[6]]))
    matriz_demanda3 = matriz_demanda3[:, 1:]
    matriz_demanda4 = np.concatenate((matriz_demanda[g[0]:h[0]],matriz_demanda[g[1]:h[1]],matriz_demanda[g[2]:h[2]],matriz_demanda[g[3]:h[3]],matriz_demanda[g[4]:h[4]],matriz_demanda[g[5]:h[5]],matriz_demanda[g[6]:h[6]]))
    matriz_demanda4 = matriz_demanda4[:, 1:]
    matriz_demanda5 = np.concatenate((matriz_demanda[q[0]:j[0]],matriz_demanda[q[1]:j[1]],matriz_demanda[q[2]:j[2]],matriz_demanda[q[3]:j[3]],matriz_demanda[q[4]:j[4]],matriz_demanda[q[5]:j[5]],matriz_demanda[q[6]:j[6]]))
    matriz_demanda5 = matriz_demanda5[:, 1:]
    matriz_demanda6 = np.concatenate((matriz_demanda[k[0]:l[0]],matriz_demanda[k[1]:l[1]],matriz_demanda[k[2]:l[2]],matriz_demanda[k[3]:l[3]],matriz_demanda[k[4]:l[4]],matriz_demanda[k[5]:l[5]],matriz_demanda[k[6]:l[6]]))
    matriz_demanda6 = matriz_demanda6[:, 1:]
    matriz_demanda7 = np.concatenate((matriz_demanda[m[0]:n[0]],matriz_demanda[m[1]:n[1]],matriz_demanda[m[2]:n[2]],matriz_demanda[m[3]:n[3]],matriz_demanda[m[4]:n[4]],matriz_demanda[m[5]:n[5]],matriz_demanda[m[6]:n[6]]))
    matriz_demanda7 = matriz_demanda7[:, 1:]
    matriz_demanda8 = np.concatenate((matriz_demanda[o[0]:p[0]],matriz_demanda[o[1]:p[1]],matriz_demanda[o[2]:p[2]],matriz_demanda[o[3]:p[3]],matriz_demanda[o[4]:p[4]],matriz_demanda[o[5]:p[5]],matriz_demanda[o[6]:p[6]]))
    matriz_demanda8 = matriz_demanda8[:, 1:]

    for i in range(0, len(matriz_demanda1)):
        for j in range(len(matriz_demanda1[0])):
            if matriz_demanda1[i, j] == 'None':
                matriz_demanda1[i, j] = np.nan
    matriz_demanda1 = matriz_demanda1.astype(np.float)
    for i in range(0, len(matriz_demanda1)):
        for j in range(len(matriz_demanda1[0])):
            if matriz_demanda1[i, j] >= 2.5e5:
                matriz_demanda1[i, j] = np.nan

    for i in range(0, len(matriz_demanda2)):
        for j in range(len(matriz_demanda2[0])):
            if matriz_demanda2[i, j] == 'None':
                matriz_demanda2[i, j] = np.nan
    matriz_demanda2 = matriz_demanda2.astype(np.float)
    for i in range(0, len(matriz_demanda2)):
        for j in range(len(matriz_demanda2[0])):
            if matriz_demanda2[i, j] >= 2.5e5:
                matriz_demanda2[i, j] = np.nan

    for i in range(0, len(matriz_demanda3)):
        for j in range(len(matriz_demanda3[0])):
            if matriz_demanda3[i, j] == 'None':
                matriz_demanda3[i, j] = np.nan
    matriz_demanda3 = matriz_demanda3.astype(np.float)
    for i in range(0, len(matriz_demanda3)):
        for j in range(len(matriz_demanda3[0])):
            if matriz_demanda3[i, j] >= 2.5e5:
                matriz_demanda3[i, j] = np.nan

    for i in range(0, len(matriz_demanda4)):
        for j in range(len(matriz_demanda4[0])):
            if matriz_demanda4[i, j] == 'None':
                matriz_demanda4[i, j] = np.nan
    matriz_demanda4 = matriz_demanda4.astype(np.float)
    for i in range(0, len(matriz_demanda4)):
        for j in range(len(matriz_demanda4[0])):
            if matriz_demanda4[i, j] >= 2.5e5:
                matriz_demanda4[i, j] = np.nan

    for i in range(0, len(matriz_demanda5)):
        for j in range(len(matriz_demanda5[0])):  # 37 columns, from 0 to 36
            if matriz_demanda5[i, j] == 'None':
                matriz_demanda5[i, j] = np.nan
    matriz_demanda5 = matriz_demanda5.astype(np.float)
    for i in range(0, len(matriz_demanda5)):
        for j in range(len(matriz_demanda5[0])):  # 37 columns, from 0 to 36
            if matriz_demanda5[i, j] >= 2.5e5:
                matriz_demanda5[i, j] = np.nan

    for i in range(0, len(matriz_demanda6)):
        for j in range(len(matriz_demanda6[0])):  # 37 columns, from 0 to 36
            if matriz_demanda6[i, j] == 'None':
                matriz_demanda6[i, j] = np.nan
    matriz_demanda6 = matriz_demanda6.astype(np.float)
    for i in range(0, len(matriz_demanda6)):
        for j in range(len(matriz_demanda6[0])):  # 37 columns, from 0 to 36
            if matriz_demanda6[i, j] >= 2.5e5:
                matriz_demanda6[i, j] = np.nan

    for i in range(0, len(matriz_demanda7)):
        for j in range(len(matriz_demanda7[0])):
            if matriz_demanda7[i, j] == 'None':
                matriz_demanda7[i, j] = np.nan
    matriz_demanda7 = matriz_demanda7.astype(np.float)
    for i in range(0, len(matriz_demanda7)):
        for j in range(len(matriz_demanda7[0])):
            if matriz_demanda7[i, j] >= 2.5e5:
                matriz_demanda7[i, j] = np.nan

    for i in range(0, len(matriz_demanda8)):
        for j in range(len(matriz_demanda8[0])):
            if matriz_demanda8[i, j] == 'None':
                matriz_demanda8[i, j] = np.nan
    matriz_demanda8 = matriz_demanda8.astype(np.float)
    for i in range(0, len(matriz_demanda8)):
        for j in range(len(matriz_demanda8[0])):
            if matriz_demanda8[i, j] >= 2.5e5:
                matriz_demanda8[i, j] = np.nan

    ix_NC = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'NC'] #índices da matriz original e ordenada com perfil NC
    ix_CP = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CP']
    ix_CI = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CI']

    sorted_l_sem1 = []
    sorted_l_sem2 = []
    sorted_l_sem3 = []
    sorted_l_sem4 = []
    sorted_l_sem5 = []
    sorted_l_sem6 = []
    sorted_l_sem7 = []
    sorted_l_sem8 = []

    if categoria == 'NC':
        m_NC = matriz_demanda1[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_NC_nonan)
        m_NC = matriz_demanda2[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_NC_nonan)
        m_NC = matriz_demanda3[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_NC_nonan)
        m_NC = matriz_demanda4[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_NC_nonan)
        m_NC = matriz_demanda5[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_NC_nonan)
        m_NC = matriz_demanda6[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_NC_nonan)
        m_NC = matriz_demanda7[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_NC_nonan)
        m_NC = matriz_demanda8[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_NC_nonan)
    elif categoria == 'CP':
        m_CP = matriz_demanda1[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_CP_nonan)
        m_CP = matriz_demanda2[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_CP_nonan)
        m_CP = matriz_demanda3[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_CP_nonan)
        m_CP = matriz_demanda4[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_CP_nonan)
        m_CP = matriz_demanda5[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_CP_nonan)
        m_CP = matriz_demanda6[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_CP_nonan)
        m_CP = matriz_demanda7[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_CP_nonan)
        m_CP = matriz_demanda8[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_CP_nonan)
    elif categoria == 'CI':
        m_CI = matriz_demanda1[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_CI_nonan)
        m_CI = matriz_demanda2[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_CI_nonan)
        m_CI = matriz_demanda3[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_CI_nonan)
        m_CI = matriz_demanda4[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_CI_nonan)
        m_CI = matriz_demanda5[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_CI_nonan)
        m_CI = matriz_demanda6[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_CI_nonan)
        m_CI = matriz_demanda7[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_CI_nonan)
        m_CI = matriz_demanda8[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_CI_nonan)

    return sorted_l_sem1,sorted_l_sem2,sorted_l_sem3,sorted_l_sem4,sorted_l_sem5,sorted_l_sem6,sorted_l_sem7,sorted_l_sem8

def PlotHistCategoria(lista_demanda_categ,titulo_grafico):
    #list_bins = np.arange(500, 185001, 46125)
    list_bins = np.arange(1000, 191001, 10000)
    list_bins = np.insert(list_bins, 0,100)
    list_bins = np.insert(list_bins, 0,1)
    list_bins = np.insert(list_bins, 0,0)
    #list_bins = np.insert(list_bins, 0, 1.0)
    #list_bins = np.insert(list_bins, 0, 0)
    #my_total_comzero = len(lista_demanda_categ)
    # lista_demanda_categ_sem0 = [i for i in lista_demanda_categ if i != 0.0]  # lista sem número 0.0
    # lista_demanda_categ_0 = [i for i in lista_demanda_categ if i == 0.0]  # lista sem número 0.0
    # lista_demanda_categ_75p = np.percentile(lista_demanda_categ, 75, interpolation='midpoint')
    #my_skew = skew(lista_demanda_categ_sem0)
    # lista_demanda_categ_sem500 = [i for i in lista_demanda_categ if i >= 500.0]  # lista sem número 0.0
    # lista_demanda_categ_sem1000 = [i for i in lista_demanda_categ if i >= 1000.0]  # lista sem número 0.0
    #lista_demanda_categ = lista_demanda_categ_sem0
    #lista_demanda_categ = lista_demanda_categ_75p
    #my_total = len(lista_demanda_categ_sem500)
    my_total = len(lista_demanda_categ)
    # my_total_0 = len(lista_demanda_categ_0)
    # my_total_0p = len(lista_demanda_categ_0)/len(lista_demanda_categ)
    # my_total_1000 = len(lista_demanda_categ_sem1000)
    # my_skew = skew(lista_demanda_categ_sem1000)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    #fig2 = ax1.hist(lista_demanda_categ, bins=list_bins, weights=np.ones_like(lista_demanda_categ)*100/len(lista_demanda_categ),label = 'freq. rel.(%)',color='c')
    ax2.hist(lista_demanda_categ,density=True,bins=list_bins,histtype = 'step',cumulative = True,label = 'freq. acum.',color='lightgrey')
    fig2 = ax1.hist(lista_demanda_categ, bins=list_bins, histtype = 'bar',weights=np.ones_like(lista_demanda_categ)*100/len(lista_demanda_categ),label = 'freq. rel.(%)',color='b')
    my_bins = fig2[1]
    my_perc = fig2[0]
    np.savetxt('list_perc_sem9bombas' +str(titulo_grafico)+'.csv',my_perc)
    #np.savetxt('list_bins_sem9bombas' + str(titulo_grafico) + '.csv', my_bins)
    #ax2.hist(lista_demanda_categ,density=True,bins=list_bins, histtype = 'stepfilled',cumulative = True,label = 'freq. acum.',color='lightgrey')
    #plt.hist(lista_demanda_categ, bins=list_bins)
    #plt.hist(lista_demanda_categ, bins=list_bins,weights=np.ones_like(lista_demanda_categ)*100/len(lista_demanda_categ))
    #plt.hist(lista_demanda_categ, bins=list_bins,density=True)
    #plt.title(str(titulo_grafico) + ' freq. relativa (%) x freq. acumulada'+'\n skew sem 1000' + ' = '+ f'{my_skew:.3f}' + '(n tot= ' + str(my_total) + ')' + '(n skew = ' + str(my_total_1000) + ')')
    #plt.title(str(titulo_grafico) + ' freq. relativa (%) x freq. acumulada' + ' (n tot= ' + str(my_total)+ ') '+'\n (n tot0= ' + str(my_total_0)+ ', % 0 = ' + f'{my_total_0p:.3f}' + ')' )
    plt.title(str(titulo_grafico) + ' freq. relativa (%) x freq. acumulada' + '\n (n análise ' + str(my_total) + ')')
    ax1.set_ylim(0,110)
    ax2.set_ylim(0, 1.1)
    ax1.legend(loc=2)
    ax2.legend(loc=0)
    plt.savefig(str(titulo_grafico)+' HistogramaConsistido.jpg',format='jpg',dpi=600) # salva a figura em jpg
    #plt.show()
    plt.close()

def PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico):
    lista_demanda_categ = np.sort(lista_demanda_categ)[::-1]
    exceedence = np.arange(1., len(lista_demanda_categ) + 1) / len(lista_demanda_categ)
    total = len(lista_demanda_categ)
    plt.title(str(titulo_grafico)+ ' (n= ' + str(total) + ')')
    plt.plot(exceedence * 100, lista_demanda_categ)
    labels = [0,10,20,30,40,50,60,70,80,90,100]
    plt.xticks(labels)
    plt.xlabel("Excedência (%)")
    plt.ylabel("Volume consumido (m³)")
    plt.grid(True)
    #plt.savefig(str(titulo_grafico)+'- Permanência.jpg',format='jpg',dpi=600) # salva a figura em jpg
    #plt.show()
    plt.close()

#Saída
##Demanda = Volume
matriz_demanda = matrix_volume_dem
# #Número de dados 'none' para cada quinzena por categoria
# my_nones = np.empty((3,8))
# for i in range(1,9):
#     for categoria in("NC","CP","CI"):
#         if categoria == 'NC':
#             n_categ = 21
#             j = 0
#         elif categoria == 'CP':
#             n_categ = 6
#             j = 1
#         else:
#             n_categ = 10
#             j = 2
#         my_list = ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[i-1]
#         my_nones[j,i-1] = n_categ * 6 * 15 - len(my_list)
# print(my_nones)
#SEMANAL - SECA
# semanal NC
categoria = 'NC'
for z in range(1,9):
    titulo = str(categoria) + ' quinzena '+str(z)
    PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)
# semanal CP
categoria = 'CP'
for z in range(1,9):
    titulo = str(categoria) + ' quinzena '+str(z)
    PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)
# semanal CI
categoria = 'CI'
for z in range(1,9):
    titulo = str(categoria) + ' quinzena '+str(z)
    PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)
l = 1

# #total
# lista_NC = ListaCategoriasSeca(matriz_carac,matriz_demanda)[0]
# lista_CP = ListaCategoriasSeca(matriz_carac,matriz_demanda)[1]
# lista_CI = ListaCategoriasSeca(matriz_carac,matriz_demanda)[2]
# #total NC
# lista_NC = ListaCategoriasSeca(matriz_carac,matriz_demanda)[0]
# titulo_grafico = 'NC - histograma'
# lista_demanda_categ = lista_NC
# #PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# #total CP
# lista_CP = ListaCategoriasSeca(matriz_carac,matriz_demanda)[1]
# titulo_grafico = 'CP - histograma'
# lista_demanda_categ = lista_CP
# #PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# #total CI
# lista_CI = ListaCategoriasSeca(matriz_carac,matriz_demanda)[2]
# titulo_grafico = 'CI - histograma'
# lista_demanda_categ = lista_CI
#PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# #2018
# lista_NC_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[0]
# lista_CP_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[1]
# lista_CI_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[2]
# titulo_grafico = '1 NC - 2018'
# lista_demanda_categ = lista_NC_1
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '2 CP - 2018'
# lista_demanda_categ = lista_CP_1
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '3 CI - 2018'
# lista_demanda_categ = lista_CI_1
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# #2019
# lista_NC_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[3]
# lista_CP_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[4]
# lista_CI_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[5]
# titulo_grafico = '4 NC - 2019'
# lista_demanda_categ = lista_NC_2
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '5 CP - 2019'
# lista_demanda_categ = lista_CP_2
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '6 CI - 2019'
# lista_demanda_categ = lista_CI_2
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# #2020
# lista_NC_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[6]
# lista_CP_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[7]
# lista_CI_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[8]
# titulo_grafico = '7 NC - 2020'
# lista_demanda_categ = lista_NC_3
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '8 CP - 2020'
# lista_demanda_categ = lista_CP_3
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '9 CI - 2020'
# lista_demanda_categ = lista_CI_3
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# #2021
# lista_NC_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[9]
# lista_CP_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[10]
# lista_CI_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[11]
# titulo_grafico = '10 NC - 2021'
# lista_demanda_categ = lista_NC_4
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '11 CP - 2021'
# lista_demanda_categ = lista_CP_4
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# titulo_grafico = '12 CI - 2021'
# lista_demanda_categ = lista_CI_4
# PlotHistCategoria(lista_demanda_categ,titulo_grafico)
# PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
# l = 1


