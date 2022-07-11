#Programa que gera gráficos a partir de séries de oferta (estações telemétricas) x demanda de água (bombas)
#Déborah Santos de Sousa
#Mestrado PTARH/UnB

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import matplotlib.pyplot as plt # Plotagem de gráficos
from matplotlib import gridspec # combinação de plotagens
from matplotlib.pyplot import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
import statistics as sts # funções estatísticas
import sklearn
from sklearn.metrics import mean_squared_error # funções estatísticas
import calendar # package com funções de calendário
from datetime import timedelta, date # calendários
import math # funções matemáticas

def PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico):
    serie_oferta = serie_oferta[372:, 1]
    serie_oferta = [np.nan if i == "None" else float(i) for i in serie_oferta]
    matriz_demanda = matriz_demanda[372:,1:]
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37): #37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    ordem_nova = [32,35,36,0,1,2,3,4,5,6,7,9,8,10,11,12,13,34,14,16,15,17,18,19,20,21,22,33,23,26,25,24,27,31,28,29,30] # ordem das bombas de montante a jusante da bacia
    nova_matriz_demanda = np.empty([2232,37])
    i = 0
    for j in (ordem_nova):
        nova_matriz_demanda[:,i] = matriz_demanda[:,j]
        i+=1
    matriz_demanda = nova_matriz_demanda
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])  # plota vários gráficos numa mesma figura
    # Oferta
    ax2 = plt.subplot(gs[0])
    if tipo_dado == 'barra':
        ax2.bar(serie_datas, serie_oferta, 1, color='c',ec='blue',linestyle='solid',linewidth=1.0)
        ax2.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.set_ylim(0, np.nanmax(serie_oferta))
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.gcf().subplots_adjust(bottom=0.1)
        max_y2 = np.nanmax(serie_oferta)
        ax2.set_ylim(0, 1.2 * max_y2)
        ax2.invert_yaxis()
    elif tipo_dado == 'linha':
        ax2.plot(serie_datas, serie_oferta,linestyle='solid',color='blue', linewidth=0.75)
        ax2.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.set_ylim(0, np.nanmax(serie_oferta))
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.gcf().subplots_adjust(bottom=0.1)
        max_y2 = np.nanmax(list(serie_oferta))
        ax2.set_ylim(0, 1.2 * max_y2)
    ax2.set_ylabel(eixoy1, color='b')
    ax2.tick_params(axis='y', colors='b')

    # Demanda
    ax = plt.subplot(gs[1],sharex = ax2) # compartilham mesmo eixo x
    color = iter(cm.rainbow(np.linspace(0, 1, 37)))
    #max_y = 0.0
    for i in range(0,37):
        c = next(color)
        sc = plt.scatter(serie_datas, list(matriz_demanda[:, i]),cmap='rainbow',color=c,s=3,label='bomba nº '+str(1+i))  # Demanda
        max_y = np.nanmax(list(matriz_demanda[:, i]))
        current_max_y = np.nanmax(list(matriz_demanda[:, i]))
        if current_max_y >= max_y:
            max_y = current_max_y
    if eixoy2 == 'Volume consumido (m³) x 10$^7$':
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        ax.set_ylim(0, 1e7)
        ax.yaxis.offsetText.set_visible(False)
        #offset = ax.yaxis.get_major_formatter().get_offset()
        ax.yaxis.set_label_text(eixoy2 + "x 10$^7$",color='black')
    elif eixoy2 == "Volume consumido (m³)":
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        ax.set_ylim(0, 2.2*1e5)
        ax.yaxis.offsetText.set_visible(False)
        #offset = ax.yaxis.get_major_formatter().get_offset()
        ax.yaxis.set_label_text(eixoy2 + "x 10$^5$",color='black')
    else:
        ax.set_ylim(0, 2.8)
        ax.set_ylabel(eixoy2, color='black')
    ax.tick_params(axis='y', colors='black')
    ax.xaxis.grid(b=True, which='major', color='.9', linestyle='--') # linhas de grade do eixo x
    ax.yaxis.grid(b=True, which='major', color='.9', linestyle='--') # linhas de grade do eixo y
    if titulo_grafico == 'Tudo - Vazão do rio x Volume consumido':
        ax.legend(loc='upper center',ncol=14,fontsize='x-small',bbox_to_anchor=(0.47, -0.35))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('bottom',size="1%", pad=0.6)
        cbar = plt.colorbar(sc,orientation='horizontal',shrink=0.6,cax=cax)
        cbar.set_ticks([0,1])
        cbar.set_ticklabels(['Montante','Jusante'])  # horizontal colorbar
        sc.set_cmap('rainbow')
        plt.legend()
    plt.gcf().autofmt_xdate()
    ax.set_xticks(["","1/JULY/2017","1/JANUARY/2018","1/JULY/2018","1/JANUARY/2019","1/JULY/2019","1/JANUARY/2020","1/JULY/2020","1/JANUARY/2021","1/JULY/2021","1/JANUARY/2022","1/JULY/2022",""])
    ax2.set_xticks(ax.get_xticks())
    plt.subplots_adjust(hspace=.0)
    plt.show()
    #plt.savefig(str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close(fig)

def PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico):
    serie_oferta = serie_oferta[372:, 1]
    serie_oferta = [np.nan if i == "None" else float(i) for i in serie_oferta]
    matriz_demanda = matriz_demanda[372:,1:]

    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37): #37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])  # plota vários gráficos numa mesma figura
    # Oferta
    ax2 = plt.subplot(gs[0])
    if tipo_dado == 'barra':
        ax2.bar(serie_datas, serie_oferta, 1, color='c',ec='blue',linestyle='solid',linewidth=1.0)
        ax2.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.set_ylim(0, np.nanmax(serie_oferta))
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.gcf().subplots_adjust(bottom=0.1)
        max_y2 = np.nanmax(serie_oferta)
        ax2.set_ylim(0, 1.2 * max_y2)
        ax2.invert_yaxis()
    elif tipo_dado == 'linha':
        ax2.plot(serie_datas, serie_oferta,linestyle='solid',color='blue', linewidth=0.75)
        ax2.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
        ax2.set_ylim(0, np.nanmax(serie_oferta))
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.gcf().subplots_adjust(bottom=0.1)
        max_y2 = np.nanmax(list(serie_oferta))
        ax2.set_ylim(0, 1.2 * max_y2)
    ax2.set_ylabel(eixoy1, color='b')
    ax2.tick_params(axis='y', colors='b')

    # Demanda
    ax = plt.subplot(gs[1],sharex = ax2)
    vetor_media_d = []
    vetor_soma_d = []
    #vetor_media_a = []
    for i in range(0,len(matriz_demanda)):
        vetor_soma_d.append(np.nansum(matriz_demanda[i,0:36])) #considerando nan como zero
        vetor_media_d.append(np.nanmean(matriz_demanda[i,0:36])) #considerando nan como zero
        #vetor_media_an[i] = np.nanmean(matriz_demanda[i, 0:36]) a cada 12 'i'
    ax.scatter(serie_datas, vetor_media_d, color='darkgray', s=5,label='Média diária')  # Demanda
    ax.scatter(serie_datas, vetor_soma_d, color='black', s=3,label='Soma diária')  # Demanda
    # for k in range(): #media anual
    #     ax.axhline(vetor_media_anual, color, xmin, xmax, linestyle)(serie_datas, list(matriz_demanda[:, i]), color=c, s=3)  # Demanda
    ax.set_ylabel(eixoy2, color='black')
    ax.tick_params(axis='y', colors='black')
    ax.xaxis.grid(b=True, which='major', color='.9', linestyle='--') # linhas de grade do eixo x
    ax.yaxis.grid(b=True, which='major', color='.9', linestyle='--') # linhas de grade do eixo y
    max_y = np.nanmax(vetor_soma_d)
    if eixoy2 == 'Volume consumido (m³)':
        ax.set_yscale('log')
        ax.set_ylim(1, 10 * max_y)
    else:
        ax.set_ylim(0, 22)
    ax.legend(loc='upper left',fontsize='x-small')
    plt.gcf().autofmt_xdate()
    ax.set_xticks(["","1/JULY/2017","1/JANUARY/2018","1/JULY/2018","1/JANUARY/2019","1/JULY/2019","1/JANUARY/2020","1/JULY/2020","1/JANUARY/2021","1/JULY/2021","1/JANUARY/2022","1/JULY/2022",""])
    ax2.set_xticks(ax.get_xticks())
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(titulo_grafico)+'.1.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close(fig)

# Oferta de água - estação 26798500
matrix_oferta = pd.read_csv('oferta_urubu.csv', sep=";", decimal=".")
matrix_oferta = np.array(matrix_oferta)
serie_chuva = matrix_oferta[:,[0,1]] # data e precipitação
serie_nivel = matrix_oferta[:,[0,3]] # data e nível
serie_vazao = matrix_oferta[:,[0,5]] # data e vazão

# Demanda de água - bombas
#Vazão
matrix_vazao_dem = pd.read_csv('vazao_demanda_urubu.csv', sep=";", decimal=".")
matrix_vazao_dem = np.array(matrix_vazao_dem)

#Volume
matrix_volume_dem = pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal=".")
matrix_volume_dem = np.array(matrix_volume_dem)

#Serie de Datas
serie_datas = serie_chuva[372:,0]

#Gráficos Volume com tudo
serie_oferta = serie_vazao
matriz_demanda = matrix_volume_dem
titulo_grafico = 'Tudo - Vazão do rio x Volume consumido'
tipo_dado = 'linha'
eixoy1 = 'Vazão do rio (m³/s)'
eixoy2 = 'Volume consumido (m³)'
PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)

# #Gráficos Volume
# serie_oferta = serie_vazao
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '1 - Vazão do rio x Volume consumido'
# tipo_dado = 'linha'
# eixoy1 = 'Vazão do rio (m³/s)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_nivel
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '2 - Nível x Volume consumido'
# tipo_dado = 'linha'
# eixoy1 = 'Nível (cm)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_chuva
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '3 - Chuva x Volume consumido'
# tipo_dado = 'barra'
# eixoy1 = 'Chuva (mm)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# eixoy2 = 'Volume consumido (m³) x 10$^7$'
# titulo_grafico = '3.0 - Chuva x Volume consumido valores altos'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# #Gráficos Vazão
# serie_oferta = serie_chuva
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '4 - Chuva x Vazão consumida'
# tipo_dado = 'barra'
# eixoy1 = 'Chuva (mm)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_vazao
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '5 - Vazão do rio x Vazão consumida'
# tipo_dado = 'linha'
# eixoy1 = 'Vazão do rio (m³/s)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_nivel
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '6 - Nível x Vazão consumida'
# tipo_dado = 'linha'
# eixoy1 = 'Nível (cm)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# # Oferta de água - estação 26795700
# matrix_oferta = pd.read_csv('oferta_urubu.csv', sep=";", decimal=".")
# matrix_oferta = np.array(matrix_oferta)
# serie_chuva = matrix_oferta[:,[0,2]] # data e precipitação
# serie_nivel = matrix_oferta[:,[0,4]] # data e nível
# serie_vazao = matrix_oferta[:,[0,6]] # data e vazão
#
# #Gráficos Volume
# serie_oferta = serie_vazao
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '7 - Vazão do rio x Volume consumido'
# tipo_dado = 'linha'
# eixoy1 = 'Vazão do rio (m³/s)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_nivel
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '8 - Nível x Volume consumido'
# tipo_dado = 'linha'
# eixoy1 = 'Nível (cm)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_chuva
# matriz_demanda = matrix_volume_dem
# titulo_grafico = '9 - Chuva x Volume consumido'
# tipo_dado = 'barra'
# eixoy1 = 'Chuva (mm)'
# eixoy2 = 'Volume consumido (m³)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# #Gráficos Vazão
# serie_oferta = serie_chuva
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '10 - Chuva x Vazão consumida'
# tipo_dado = 'barra'
# eixoy1 = 'Chuva (mm)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_vazao
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '11 - Vazão do rio x Vazão consumida'
# tipo_dado = 'linha'
# eixoy1 = 'Vazão do rio (m³/s)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
#
# serie_oferta = serie_nivel
# matriz_demanda = matrix_vazao_dem
# titulo_grafico = '12 - Nível x Vazão consumida'
# tipo_dado = 'linha'
# eixoy1 = 'Nível (cm)'
# eixoy2 = 'Vazão consumida (m³/s)'
# PlotOfertaDemanda(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)
# PlotOfertaDemanda_medsum(tipo_dado,eixoy1,eixoy2,serie_datas,serie_oferta,matriz_demanda,titulo_grafico)