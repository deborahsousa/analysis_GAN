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
        for j in range(0, 38):  # 37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37):  # 37 columns, from 0 to 36
            if matriz_demanda[i, j] >= 2.5e5:
                matriz_demanda[i, j] = np.nan

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

    n3 = len(l_NC_nonan)
    my_range3 = float(max((l_NC_nonan)))
    n_interv3 = float(n3**(0.5))
    w_interv3 = float(my_range3/n_interv3)

    n1 = len(l_CP_nonan)
    my_range1 = float(max((l_CP_nonan)))
    n_interv1 = float(n1**(0.5))
    w_interv1 = float(my_range1/n_interv1)

    n2 = len(l_CI_nonan)
    my_range2 = float(max((l_CI_nonan)))
    n_interv2 = float(n2**(0.5))
    w_interv2 = float(my_range2/n_interv2)

    my_ranges = []
    my_ranges = [my_range1,my_range2,my_range3]
    my_range = max(my_ranges)
    w_intervs = []
    w_intervs = [w_interv1,w_interv2,w_interv3]
    w_interv = w_intervs[my_ranges.index(my_range)]

    return sorted_l_NC,sorted_l_CP,sorted_l_CI,my_range,w_interv

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

    # #Parâmetros do histograma
    # #ano 1
    # n11 = len(l_NC_nonan)
    # my_range11 = float(max((l_NC_nonan)))
    # n_interv11 = float(n11**(0.5))
    # w_interv11 = float(my_range11/n_interv11)
    #
    # n21 = len(l_CP_nonan)
    # my_range21 = float(max((l_CP_nonan)))
    # n_interv21 = float(n21**(0.5))
    # w_interv21 = float(my_range21/n_interv21)
    #
    # n31 = len(l_CI_nonan)
    # my_range31 = float(max((l_CI_nonan)))
    # n_interv31 = float(n31**(0.5))
    # w_interv31 = float(my_range31/n_interv31)
    #
    # my_ranges = [my_range11,my_range21,my_range31]
    # my_range1 = max(my_ranges)
    # w_intervs = [w_interv11,w_interv21,w_interv31]
    # w_interv1 = w_intervs[my_ranges.index(my_range1)]
    #
    # #ano 2
    # n12 = len(l_NC_nonan)
    # my_range12 = float(max((l_NC_nonan)))
    # n_interv12 = float(n12**(0.5))
    # w_interv12 = float(my_range12/n_interv12)
    #
    # n22 = len(l_CP_nonan)
    # my_range22 = float(max((l_CP_nonan)))
    # n_interv22 = float(n22**(0.5))
    # w_interv22 = float(my_range22/n_interv22)
    #
    # n32 = len(l_CI_nonan)
    # my_range32 = float(max((l_CI_nonan)))
    # n_interv32 = float(n32**(0.5))
    # w_interv32 = float(my_range32/n_interv32)
    #
    # my_ranges = [my_range12,my_range22,my_range32]
    # my_range2 = max(my_ranges)
    # w_intervs = [w_interv12,w_interv22,w_interv32]
    # w_interv2 = w_intervs[my_ranges.index(my_range2)]
    #
    # #ano 3
    # n13 = len(l_NC_nonan)
    # my_range13 = float(max((l_NC_nonan)))
    # n_interv13 = float(n13**(0.5))
    # w_interv13 = float(my_range13/n_interv13)
    #
    # n23 = len(l_CP_nonan)
    # my_range23 = float(max((l_CP_nonan)))
    # n_interv23 = float(n23**(0.5))
    # w_interv23 = float(my_range23/n_interv23)
    #
    # n33 = len(l_CI_nonan)
    # my_range33 = float(max((l_CI_nonan)))
    # n_interv33 = float(n33**(0.5))
    # w_interv33 = float(my_range33/n_interv33)
    #
    # my_ranges = [my_range13,my_range23,my_range33]
    # my_range3 = max(my_ranges)
    # w_intervs = [w_interv13,w_interv23,w_interv33]
    # w_interv3 = w_intervs[my_ranges.index(my_range3)]
    #
    # #ano 4
    # n14 = len(l_NC_nonan)
    # my_range14 = float(max((l_NC_nonan)))
    # n_interv14 = float(n14**(0.5))
    # w_interv14 = float(my_range14/n_interv14)
    #
    # n24 = len(l_CP_nonan)
    # my_range24 = float(max((l_CP_nonan)))
    # n_interv24 = float(n24**(0.5))
    # w_interv24 = float(my_range24/n_interv24)
    #
    # n34 = len(l_CI_nonan)
    # my_range34 = float(max((l_CI_nonan)))
    # n_interv34 = float(n34**(0.5))
    # w_interv34 = float(my_range34/n_interv34)
    #
    # my_ranges = [my_range14,my_range24,my_range34]
    # my_range4 = max(my_ranges)
    # w_intervs = [w_interv14,w_interv24,w_interv34]
    # w_interv4 = w_intervs[my_ranges.index(my_range4)]

    # return sorted_l_NC_1,sorted_l_CP_1,sorted_l_CI_1,my_range1,w_interv1,sorted_l_NC_2,sorted_l_CP_2,sorted_l_CI_2,\
    #        my_range2,w_interv2,sorted_l_NC_3,sorted_l_CP_3,sorted_l_CI_3,my_range3,w_interv3,sorted_l_NC_4,sorted_l_CP_4,\
    #        sorted_l_CI_4,my_range4,w_interv4
    return sorted_l_NC_1,sorted_l_CP_1,sorted_l_CI_1,sorted_l_NC_2,sorted_l_CP_2,sorted_l_CI_2,sorted_l_NC_3,\
           sorted_l_CP_3,sorted_l_CI_3,sorted_l_NC_4,sorted_l_CP_4,sorted_l_CI_4

def PlotHistCategoria(lista_demanda_categ,titulo_grafico):
    #list_bins = np.arange(0.1,my_range,w_interv)
    list_bins = np.arange(500, 185000, 500)
    lista_demanda_categ_sem0 = [i for i in lista_demanda_categ if i != 0.0]  # lista sem número 0.0
    my_skew = skew(lista_demanda_categ_sem0)
    lista_demanda_categ_sem500 = [i for i in lista_demanda_categ if i >= 500.0]  # lista sem número 0.0
    my_total = len(lista_demanda_categ_sem500)
    #plt.hist(lista_demanda_categ, bins=list_bins,normed=True)
    #plt.hist(lista_demanda_categ, bins=list_bins,weights=np.ones_like(lista_demanda_categ)*100/len(lista_demanda_categ))
    plt.hist(lista_demanda_categ, bins=list_bins,density=True,histtype = 'step',cumulative = True)
    #plt.yaxis.set_major_formatter(PercentFormatter())
    plt.title(str(titulo_grafico) + ' (%)'+' - skew sem zeros' + ' = '+ f'{my_skew:.3f}' + ' (n= ' + str(my_total) + ')')
    #plt.ylim(0,2)
    #plt.savefig(str(titulo_grafico)+'Hist. relativo.jpg',format='jpg',dpi=600) # salva a figura em jpg
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
    plt.savefig(str(titulo_grafico)+'- Permanência.jpg',format='jpg',dpi=600) # salva a figura em jpg
    #plt.show()
    plt.close()
#Saída
##Volume
matriz_demanda = matrix_volume_dem
# #total
# lista_NC = ListaCategoriasSeca(matriz_carac,matriz_demanda)[0]
# lista_CP = ListaCategoriasSeca(matriz_carac,matriz_demanda)[1]
# lista_CI = ListaCategoriasSeca(matriz_carac,matriz_demanda)[2]
# my_range = ListaCategoriasSeca(matriz_carac,matriz_demanda)[3]
# w_interv = ListaCategoriasSeca(matriz_carac,matriz_demanda)[4]
# titulo_grafico = 'NC - histograma'
# lista_demanda_categ = lista_NC
# PlotHistCategoria(lista_demanda_categ,titulo_grafico,my_range,w_interv)
# titulo_grafico = 'CP - histograma'
# lista_demanda_categ = lista_CP
# PlotHistCategoria(lista_demanda_categ,titulo_grafico,my_range,w_interv)
# titulo_grafico = 'CI - histograma'
# lista_demanda_categ = lista_CI
# PlotHistCategoria(lista_demanda_categ,titulo_grafico,my_range,w_interv)
#2018
lista_NC_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[0]
lista_CP_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[1]
lista_CI_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[2]
# my_range_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[3]
# w_interv_1 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[4]
titulo_grafico = '1 NC - 2018'
lista_demanda_categ = lista_NC_1
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '2 CP - 2018'
lista_demanda_categ = lista_CP_1
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '3 CI - 2018'
lista_demanda_categ = lista_CI_1
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
#2019
lista_NC_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[3]
lista_CP_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[4]
lista_CI_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[5]
# my_range_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[8]
# w_interv_2 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[9]
titulo_grafico = '4 NC - 2019'
lista_demanda_categ = lista_NC_2
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '5 CP - 2019'
lista_demanda_categ = lista_CP_2
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '6 CI - 2019'
lista_demanda_categ = lista_CI_2
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
#2020
lista_NC_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[6]
lista_CP_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[7]
lista_CI_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[8]
# my_range_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[13]
# w_interv_3 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[14]
titulo_grafico = '7 NC - 2020'
lista_demanda_categ = lista_NC_3
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '8 CP - 2020'
lista_demanda_categ = lista_CP_3
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '9 CI - 2020'
lista_demanda_categ = lista_CI_3
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
#2021
lista_NC_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[9]
lista_CP_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[10]
lista_CI_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[11]
# my_range_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[18]
# w_interv_4 = ListaCategoriasSecaAnual(matriz_carac,matriz_demanda)[19]
titulo_grafico = '10 NC - 2021'
lista_demanda_categ = lista_NC_4
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '11 CP - 2021'
lista_demanda_categ = lista_CP_4
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
titulo_grafico = '12 CI - 2021'
lista_demanda_categ = lista_CI_4
PlotHistCategoria(lista_demanda_categ,titulo_grafico)
PlotCurvaPermCategoria(lista_demanda_categ,titulo_grafico)
l = 1


