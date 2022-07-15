#Programa que gera gráficos a partir de séries de oferta (estações telemétricas) x demanda de água (bombas)
#Déborah Santos de Sousa
#Mestrado PTARH/UnB

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import matplotlib.pyplot as plt # Plotagem de gráficos
from matplotlib import gridspec # combinação de plotagens
from matplotlib.pyplot import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

#Dados de entrada
##Oferta
matrix_oferta = pd.read_csv('oferta_urubu.csv', sep=";", decimal=".")
matrix_oferta = np.array(matrix_oferta)
serie_chuva2 = matrix_oferta[:,[0,1]] # data e precipitação #26798500
serie_nivel2 = matrix_oferta[:,[0,3]] # data e nível
serie_vazao2 = matrix_oferta[:,[0,5]] # data e vazão
serie_chuva1 = matrix_oferta[:,[0,2]] # data e precipitação #26795700
serie_nivel1 = matrix_oferta[:,[0,4]] # data e nível
serie_vazao1 = matrix_oferta[:,[0,6]] # data e vazão
## Demanda
###Vazão
info_vazao_dem = pd.read_csv('vazao_demanda_urubu.csv', sep=";", decimal=".")
info_vazao_dem = np.array(info_vazao_dem)
matrix_vazao_dem = info_vazao_dem[3:,:]
matriz_carac = info_vazao_dem[0:3,1:]
###Volume
matrix_volume_dem = pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal=".")
matrix_volume_dem = np.array(matrix_volume_dem)
#Serie de Datas
serie_datas = serie_chuva2[372:,0]
serie_datas = [m.replace('JANUARY', 'JAN') for m in serie_datas]
serie_datas = [m.replace('JULY', 'JUL') for m in serie_datas]

#Funções
def SubmatrizCategorias(matriz_carac,matriz_demanda):
    matriz_demanda = matriz_demanda[372:,1:]
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37): #37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    ordem_nova = [32, 35, 36, 0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 34, 14, 16, 15, 17, 18, 19, 20, 21, 22, 33,
                  23, 26, 25, 24, 27, 31, 28, 29, 30]  # ordem das bombas de montante a jusante da bacia
    # ordem dos rótulos original = [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42]
    nova_matriz_demanda = np.empty([2232,37])
    nova_matriz_carac = np.empty([3,37],dtype=object)
    i = 0
    for j in (ordem_nova):
        nova_matriz_demanda[:,i] = matriz_demanda[:,j]
        nova_matriz_carac[:, i] = matriz_carac[:, j]
        i+=1

    ix_NC = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'NC'] #índices da matriz original e ordenada com perfil NC
    m_NC = matriz_demanda[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
    ix_CI = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CI']
    m_CI = matriz_demanda[:,ix_CI]
    ix_CP = [i for i, v in enumerate(matriz_carac[0, :]) if v == 'CP']
    m_CP = matriz_demanda[:,ix_CP]
    ix_D1 = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'D1']
    m_D1 = matriz_demanda[:,ix_D1]
    ix_D2 = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'D2']
    m_D2 = matriz_demanda[:,ix_D2]
    ix_D3 = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'D3']
    m_D3 = matriz_demanda[:,ix_D3]

    return nova_matriz_demanda,m_NC,m_CI,m_CP,m_D1,m_D2,m_D3

def PlotDemanda_categoria_unico(eixoy,serie_datas,matriz_demanda,matriz_carac,titulo_grafico):
    a = SubmatrizCategorias(matriz_carac, matriz_demanda)
    #matriz_demanda = a[0]
    m_NC = a[1]
    m_CI = a[2]
    m_CP = a[3]
    m_D1 = a[4]
    m_D2 = a[5]
    m_D3 = a[6]

    ms = 3
    c = 'm'
    categoria = 'NC'
    plt.plot(serie_datas, m_NC, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close()

    c = 'orange'
    categoria = 'CI'
    plt.plot(serie_datas, m_CI, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

    c = 'c'
    categoria = 'CP'
    plt.plot(serie_datas, m_CP, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

    c = 'm'
    categoria = 'D1'
    plt.plot(serie_datas, m_D1, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

    c = 'orange'
    categoria = 'D2'
    plt.plot(serie_datas, m_D2, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

    c = 'c'
    categoria = 'D3'
    plt.plot(serie_datas, m_D3, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.5e5)
        plt.ylabel(eixoy+"x 10$^5$", color='black')
    else:
        plt.ylim(0, 2.8)
        plt.ylabel(eixoy, color='black')
    plt.tick_params(axis='y', colors='black')
    plt.grid(axis='x', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    plt.grid(axis='y', b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().autofmt_xdate()
    plt.xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    plt.subplots_adjust(hspace=.0)
    #plt.show()
    plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

def Plot2OfertaDemanda_irrigante(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_carac,matriz_demanda,titulo_grafico):
    serie_oferta1 = serie_oferta1[372:, 1]
    serie_oferta1 = [np.nan if i == "None" else float(i) for i in serie_oferta1]
    serie_oferta2 = serie_oferta2[372:, 1]
    serie_oferta2 = [np.nan if i == "None" else float(i) for i in serie_oferta2]
    matriz_demanda = matriz_demanda[372:, 1:]
    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37): #37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan
    matriz_demanda = matriz_demanda.astype(np.float)
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])  # plota vários gráficos numa mesma figura
    # Oferta 1
    ax1 = plt.subplot(gs[0])
    ax1.bar(serie_datas, serie_oferta1, 1, color='c', ec='c', linestyle='solid', linewidth=1.0)
    ax1.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
    ax1.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
    ax1.set_ylim(0, np.nanmax(serie_oferta1))
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.gcf().subplots_adjust(bottom=0.1)
    ax1.set_ylim(0, 700)
    ax1.set_ylabel(eixoy1, color='b')
    ax1.tick_params(axis='y', colors='b')
    ax1.invert_yaxis()
    #Oferta 2
    ax3 = ax1.twinx()
    ax3.plot(serie_datas, serie_oferta2, linestyle='solid', color='navy', linewidth=0.75)
    ax3.xaxis.grid(b=True, which='major', color='0.9', linestyle='--')
    ax3.yaxis.grid(b=True, which='major', color='0.9', linestyle='--')
    ax3.set_ylim(0, np.nanmax(serie_oferta2))
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.gcf().subplots_adjust(bottom=0.1)
    ax3.set_ylim(0,700)
    ax3.set_ylabel(eixoy3, color='b')
    ax3.tick_params(axis='y', colors='b')
    xs = np.linspace(0,2322,1)
    ys = np.linspace(0,700,1)
    #ax3.axvline(x='1/AGO/2018', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.2,color='red')
    #ax3.vlines(x=['1/JUL/2018','1/JUL/2019','1/JUL/2020','1/JUL/2021','1/JUL/2022'], ymin=0.0, ymax=len(ys),linestyle='dashed',label='Atenção',linewidth=1.0,color='yellow')
    #ax3.vlines(x=['1/AGO/2018','1/AGO/2019','1/AGO/2020','1/AGO/2021'], ymin=0.0, ymax=700,linestyle='dashed',label='Restrição',linewidth=1.0,color='red')
    ax3.axhline(y=398, xmin=0, xmax=len(xs),linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax3.axhline(y=220, xmin=0, xmax=len(xs),linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    ax3.legend(loc='lower left', fontsize='x-small',ncol=1)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax3.legend(by_label.values(), by_label.keys())

    # Demanda
    col_f = [] # coluna cuja bomba é do fazendeiro 'i'
    for j in range(1,25):
        col_f.append([i for i, v in enumerate(matriz_carac[2, :]) if v == str(j)])
    ax2 = plt.subplot(gs[1], sharex=ax1)
    color = iter(cm.rainbow(np.linspace(0, 1, 24)))
    for i in range(0, 24):
        c = next(color)
        list = (col_f[i])
        m_f = matriz_demanda[:, list]
        ax2.plot(serie_datas,m_f, 'o', linestyle='None', label='Irrigante nº'+str(i+1),markerfacecolor="None",
            markeredgecolor=c, markeredgewidth=0.5, markersize=3)
    ax2.legend(loc='upper left', fontsize='x-small',ncol=11,bbox_to_anchor=(-0.1, -0.35))
    ax2.set_ylabel(eixoy2, color='black')
    ax2.tick_params(axis='y', colors='black')
    ax2.xaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    ax2.yaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    ax2.axvline(x='1/JUL/2018', ymin=0.0, ymax=700.0,linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2019', ymin=0.0, ymax=700.0,linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2020', ymin=0.0, ymax=700.0,linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2021', ymin=0.0, ymax=700.0,linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2022', ymin=0.0, ymax=700.0,linestyle='dashed',label='Atenção',linewidth=0.4,color='y')
    ax2.axvline(x='1/AUGUST/2018', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2019', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2020', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2021', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2022', ymin=0.0, ymax=700.0,linestyle='dashed',label='Restrição',linewidth=0.4,color='red')
    if eixoy2 == 'Volume consumido (m³)':
        ax2.set_ylim(1, 2.8e5)
    else:
        ax2.set_ylim(0, 5)
    plt.gcf().autofmt_xdate()
    ax2.set_xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                   "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    ax1.set_xticks(ax2.get_xticks())
    plt.subplots_adjust(hspace=.0)
    plt.show()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    #plt.savefig(str(titulo_grafico) + '.jpg', format='jpg', bbox_inches='tight', dpi=600)  # salva a figura em jpg
    plt.close(fig)
#Saída
##Individuais
###Vazão
matriz_demanda = matrix_vazao_dem
eixoy = 'Vazão consumida (m³/s)'
titulo_grafico = 'Vazão consumida'
#PlotDemanda_categoria_unico(eixoy, serie_datas, matriz_demanda, matriz_carac, titulo_grafico)
###Volume
matriz_demanda = matrix_volume_dem
eixoy = 'Volume consumido (m³)'
titulo_grafico = 'Volume consumido'
#PlotDemanda_categoria_unico(eixoy, serie_datas, matriz_demanda, matriz_carac, titulo_grafico)

##Duplos
###Chuva Vazao
###Chuva Volume
###Nivel Vazao
###Nivel Volume

##Triplos - Por irrigante
###Chuva x Vazao x Vazao
serie_oferta1 = serie_chuva2
eixoy1 = 'Chuva (mm)'
serie_oferta2 = serie_nivel2
eixoy3 = 'Nível (cm)'
matriz_demanda = matrix_vazao_dem
eixoy2 = 'Vazão consumida (m³/s)'
titulo_grafico = "Chuva x Nível x 26798500 x Vazão"
Plot2OfertaDemanda_irrigante(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_carac,matriz_demanda,titulo_grafico)
###Chuva x Vazao x Volume
serie_oferta1 = serie_chuva2
eixoy1 = 'Chuva (mm)'
serie_oferta2 = serie_nivel2
eixoy3 = 'Nível (cm)'
matriz_demanda = matrix_volume_dem
eixoy2 = 'Volume consumido (m³)'
titulo_grafico = "Chuva x Nível x 26798500 x Volume"
Plot2OfertaDemanda_irrigante(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_carac,matriz_demanda,titulo_grafico)

