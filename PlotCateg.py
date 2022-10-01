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
def SubmatrizCategorias(matriz_carac,matriz_demanda,serie_oferta):
    ix_seca1a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2018'] #índice da linha da data inicial da seca do ano 1
    ix_seca1b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2018'] #índice da linha da data final da seca do ano 1
    ix_seca2a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2019'] #índice da linha da data inicial da seca do ano 2
    ix_seca2b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2019'] #índice da linha da data final da seca do ano 2
    ix_seca3a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2020'] #índice da linha da data inicial da seca do ano 3
    ix_seca3b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2020'] #índice da linha da data final da seca do ano 3
    ix_seca4a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2021'] #índice da linha da data inicial da seca do ano 4
    ix_seca4b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2021'] #índice da linha da data final da seca do ano 4
    ix_seca5a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY/2022'] #índice da linha da data inicial da seca do ano 4
    ix_seca5b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST/2022'] #índice da linha da data final da seca do ano 4
    a = ix_seca1a[0]
    b = 1 + ix_seca1b[0]
    c = ix_seca2a[0]
    d = 1 + ix_seca2b[0]
    e = ix_seca3a[0]
    f = 1 + ix_seca3b[0]
    g = ix_seca4a[0]
    h = 1 + ix_seca4b[0]
    j = ix_seca5a[0]
    k = 1 + ix_seca5b[0]
    matriz_demanda = np.concatenate((matriz_demanda[a:b],matriz_demanda[c:d],matriz_demanda[e:f],matriz_demanda[g:h],matriz_demanda[j:k]))

    serie_datas_seca = matriz_demanda[:,0]
    serie_oferta_seca = matriz_demanda[:,0:1]
    serie_oferta_seca = np.concatenate((serie_oferta[a:b],serie_oferta[c:d],serie_oferta[e:f],serie_oferta[g:h],serie_oferta[j:k]))
    serie_oferta_seca[:,1] = [np.nan if i == "None" else float(i) for i in serie_oferta_seca[:,1]]

    matriz_demanda = matriz_demanda[:,1:] # retira colunas de datas

    for i in range(0, len(matriz_demanda)):
        for j in range(0, 37): #37 columns, from 0 to 36
            if matriz_demanda[i, j] == 'None':
                matriz_demanda[i, j] = np.nan

    # # excluindo bombas anômalas quanto a dados zerados
    # matriz_demanda[:,0] = np.nan
    # matriz_demanda[:,32] = np.nan
    # matriz_demanda[:,36] = np.nan

    matriz_demanda = matriz_demanda.astype(np.float)
    #np.savetxt('matriz_seca_bombas_ordemnormal.csv',matriz_demanda)

    ordem_nova = [32, 35, 36, 0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 34, 14, 16, 15, 17, 18, 19, 20, 21, 22, 33,
                  23, 26, 25, 24, 27, 31, 28, 29, 30]  # ordem das bombas de montante a jusante da bacia
    # ordem dos rótulos original = [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42]
    nova_matriz_demanda = np.empty((len(matriz_demanda),len(matriz_demanda[0])))
    nova_matriz_carac = np.empty([3,37],dtype=object)
    i = 0
    j = 0
    for j in (ordem_nova):
        nova_matriz_demanda[:,i] = matriz_demanda[:,j]
        nova_matriz_carac[:, i] = matriz_carac[:, j]
        i = i + 1
    matriz_carac = nova_matriz_carac
    matriz_demanda = nova_matriz_demanda

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
    #np.savetxt('serie_datas_seca.csv',serie_datas_seca,fmt='%s')
    #np.savetxt('serie_oferta_seca.csv',serie_oferta_seca,fmt='%s')

    return matriz_demanda,m_NC,m_CI,m_CP,m_D1,m_D2,m_D3,serie_datas_seca,serie_oferta_seca

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
    for i in range(len(m_NC[0])):
        plt.plot(serie_datas, m_NC[:,i], 'o', linestyle='None',label=str(categoria)+" "+str(i+1),markerfacecolor="None",
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
    #plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close()

    c = 'brown'
    categoria = 'CI'
    for i in range(len(m_CI[0])):
        plt.plot(serie_datas, m_CI[:, i], 'o', linestyle='None', label=str(categoria) + " " + str(i + 1),
                 markerfacecolor="None",
                 markeredgecolor=c, markeredgewidth=0.25, markersize=ms)
        if eixoy == "Volume consumido (m³)":
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            plt.ylim(0, 2.5e5)
            plt.ylabel(eixoy + "x 10$^5$", color='black')
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
        plt.xticks(
            ["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
             "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
        plt.subplots_adjust(hspace=.0)
        #plt.show()
    # plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close()

    c = 'c'
    categoria = 'CP'
    for i in range(len(m_CP[0])):
        plt.plot(serie_datas, m_CP[:, i], 'o', linestyle='None', label=str(categoria) + " " + str(i + 1),
                 markerfacecolor="None",
                 markeredgecolor=c, markeredgewidth=0.25, markersize=ms)
        if eixoy == "Volume consumido (m³)":
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            plt.ylim(0, 2.5e5)
            plt.ylabel(eixoy + "x 10$^5$", color='black')
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
        plt.xticks(
            ["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
             "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
        plt.subplots_adjust(hspace=.0)
        plt.show()
    # plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg
    plt.close()

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
    #plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

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
    #plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

    c = 'c'
    categoria = 'D3'
    plt.plot(serie_datas, m_D3, 'o', linestyle='None',label=str(categoria),markerfacecolor="None",
         markeredgecolor=c, markeredgewidth=0.25,markersize=ms)
    if eixoy == "Volume consumido (m³)":
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.ylim(0, 2.8e5)
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
    #plt.savefig(str(categoria)+str(titulo_grafico)+'.jpg',format='jpg',bbox_inches='tight',dpi=600) # salva a figura em jpg

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
    ax2.xaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    ax2.yaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    ax2.axvline(x='1/JUL/2018', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2019', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2020', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2021', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2022', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/AUGUST/2018', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2019', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2020', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2021', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2022', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.tick_params(axis='y', colors='black')
    if eixoy2 == 'Volume consumido (m³)':
        ax2.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        ax2.yaxis.set_label_text(eixoy2 + "x 10$^5$",color='black')
        ax2.yaxis.offsetText.set_visible(False)
        ax2.set_ylim(1, 2.8e5)
    else:
        ax2.set_ylabel(eixoy2, color='black')
        ax2.set_ylim(0, 5)
    plt.gcf().autofmt_xdate()
    ax2.set_xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                   "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    ax1.set_xticks(ax2.get_xticks())
    plt.subplots_adjust(hspace=.0)
    ax2.legend()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax2.legend(by_label.values(), by_label.keys(),loc='upper left', fontsize='x-small',ncol=8,bbox_to_anchor=(0, -0.25))
    plt.show()
    plt.savefig(str(titulo_grafico) + '.jpg', format='jpg', bbox_inches='tight', dpi=600)  # salva a figura em jpg
    plt.close(fig)

def Plot2OfertaDemanda_bomba(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_demanda,titulo_grafico):
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
    ordem_nova = [32,35,36,0,1,2,3,4,5,6,7,9,8,10,11,12,13,34,14,16,15,17,18,19,20,21,22,33,23,26,25,24,27,31,28,29,30] # ordem das bombas de montante a jusante da bacia
    # ordem dos rótulos original = [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42]
    nova_matriz_demanda = np.empty([2232,37])
    i = 0
    for j in (ordem_nova):
        nova_matriz_demanda[:,i] = matriz_demanda[:,j]
        i+=1
    matriz_demanda = nova_matriz_demanda
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
    ax2 = plt.subplot(gs[1], sharex=ax1)
    color = iter(cm.rainbow(np.linspace(0, 1, 37)))
    for i in range(0,37):
        c = next(color)
        ax2.plot(serie_datas,list(matriz_demanda[:, i]), 'o', linestyle='None', label='bomba nº '+str(1+i),markerfacecolor="None",
            markeredgecolor=c, markeredgewidth=0.5, markersize=3)
    ax2.xaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo x
    ax2.yaxis.grid(b=True, which='major', color='.9', linestyle='--')  # linhas de grade do eixo y
    ax2.axvline(x='1/JUL/2018', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2019', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2020', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2021', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/JUL/2022', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='y')
    ax2.axvline(x='1/AUGUST/2018', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2019', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2020', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2021', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.axvline(x='1/AUGUST/2022', ymin=0.0, ymax=700.0,linestyle='dashed',linewidth=0.4,color='red')
    ax2.tick_params(axis='y', colors='black')
    if eixoy2 == 'Volume consumido (m³)':
        ax2.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        ax2.yaxis.set_label_text(eixoy2 + "x 10$^5$",color='black')
        ax2.yaxis.offsetText.set_visible(False)
        ax2.set_ylim(1, 2.8e5)
    else:
        ax2.set_ylabel(eixoy2, color='black')
        ax2.set_ylim(0, 5)
    plt.gcf().autofmt_xdate()
    ax2.set_xticks(["", "1/JUL/2017", "1/JAN/2018", "1/JUL/2018", "1/JAN/2019", "1/JUL/2019", "1/JAN/2020", "1/JUL/2020",
                   "1/JAN/2021", "1/JUL/2021", "1/JAN/2022", "1/JUL/2022", ""])
    ax1.set_xticks(ax2.get_xticks())
    plt.subplots_adjust(hspace=.0)
    ax2.legend()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax2.legend(by_label.values(), by_label.keys(),loc='upper left', fontsize='x-small',ncol=12,bbox_to_anchor=(0, -0.25))
    plt.show()
    plt.savefig(str(titulo_grafico) +'por_bomba.jpg', format='jpg', bbox_inches='tight', dpi=600)  # salva a figura em jpg
    plt.close(fig)

def PlotBombaRegrasSeca(matriz_categ,categoria,serie_datas_seca,serie_oferta_seca,titulo_grafico):
    for i in range(len(matriz_categ[0])):
        fig, ax1 = plt.subplots()
        # Demanda
        eixoy = "Volume consumido (m³)"
        ms = 6
        c = 'b'
        if categoria == 'NC':
            c = 'm'
        elif categoria == 'CI':
            c = 'brown'
        elif categoria == 'CP':
            c = 'c'
        y = matriz_categ[:,i]
        ax1.plot(serie_datas_seca, y, 'o', linestyle='None', label=str(categoria) + " " + str(i + 1),
                 markerfacecolor="None",
                 markeredgecolor=c, markeredgewidth=1.0, markersize=ms)
        ax1.set_ylim(0, 2.5e5)
        ax1.set_ylabel(eixoy + "x 10$^5$", color='black')
        ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        # Oferta
        ax3 = ax1.twinx()
        ax3.plot(serie_datas_seca, serie_oferta_seca[:, 1], linestyle='solid', color='navy',linewidth=0.75)
        plt.tight_layout()
        ax3.set_ylim(0, 700)
        ax3.set_ylabel('Nível (cm)', color='b')
        ax3.tick_params(axis='y', colors='b')
        ax1.set_xticks(ax1.get_xticks()[::31])
        plt.gcf().autofmt_xdate()
        xs = np.linspace(0, len(serie_datas_seca), 1)
        ys = np.linspace(0, 700, 1)
        # ax3.set_xticklabels(["1/MAY/2018", "1/JUNE/2018", "1/JULY/2018",
        #             "1/AUGUST/2018", "1/MAY/2019", "1/JUNE/2019", "1/JULY/2019", "1/AUGUST/2019", "1/MAY/2020",
        #             "1/JUNE/2020","1/JULY/2020", "1/AUGUST/2020", "1/MAY/2021", "1/JUNE/2021", "1/JULY/2021", "1/AUGUST/2021",
        #             "1/MAY/2022","1/JUNE/2022", "1/JULY/2022", "1/AUGUST/2022"])
        # regras do biênio
        y_yellow = 398
        y_red = 220
        d11 = '1/JULY/2018'
        d21 = '1/AUGUST/2018'
        d12 = '1/JULY/2019'
        d22 = '1/AUGUST/2019'
        d13 = '1/JULY/2020'
        d23 = '1/AUGUST/2020'
        d14 = '1/JULY/2021'
        d24 = '1/AUGUST/2021'
        d15 = '1/JULY/2022'
        d25 = '1/AUGUST/2022'
        ax3.axhline(y=y_yellow, xmin=0, xmax=len(xs), linestyle='dashed', label='Atenção', linewidth=0.4, color='y')
        ax3.axhline(y=y_red, xmin=0, xmax=len(xs), linestyle='dashed', label='Restrição', linewidth=0.4, color='red')
        ax1.axvline(x=d11, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
        ax1.axvline(x=d12, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
        ax1.axvline(x=d13, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
        ax1.axvline(x=d14, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
        ax1.axvline(x=d15, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
        ax1.axvline(x=d21, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
        ax1.axvline(x=d22, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
        ax1.axvline(x=d23, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
        ax1.axvline(x=d24, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
        ax1.axvline(x=d25, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')

        ax1.axvline(x='1/MAY/2018', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
        ax1.axvline(x='1/MAY/2019', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
        ax1.axvline(x='1/MAY/2020', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
        ax1.axvline(x='1/MAY/2021', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
        ax1.axvline(x='1/MAY/2022', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')

        ax3.fill_between(serie_datas_seca, y_yellow, y_red,color='yellow', alpha=0.1)
        ax3.fill_between(serie_datas_seca, 0, y_red, color='red', alpha=0.1)
        ax1.fill_betweenx(y, d11, d21, color='yellow', alpha=0.1)
        ax1.fill_betweenx(y, d21, '31/AUGUST/2018', color='red', alpha=0.1)
        ax1.fill_betweenx(y, d12, d22, color='yellow', alpha=0.1)
        ax1.fill_betweenx(y, d22, '31/AUGUST/2019', color='red', alpha=0.1)
        ax1.fill_betweenx(y, d13, d23, color='yellow', alpha=0.1)
        ax1.fill_betweenx(y, d23, '31/AUGUST/2020', color='red', alpha=0.1)
        ax1.fill_betweenx(y, d14, d24, color='yellow', alpha=0.1)
        ax1.fill_betweenx(y, d24, '31/AUGUST/2021', color='red', alpha=0.1)
        ax1.fill_betweenx(y, d15, d25, color='yellow', alpha=0.1)
        ax1.fill_betweenx(y, d25, '31/AUGUST/2022', color='red', alpha=0.1)
        plt.legend()
        plt.tight_layout()
        #plt.show()
        plt.savefig(str(categoria) + str(i + 1) + str(titulo_grafico) + '.jpg', format='jpg', bbox_inches='tight',dpi=600)  # salva a figura em jpg
        plt.close()

#Saída
##Individuais
###Vazão
# matriz_demanda = matrix_vazao_dem
# eixoy = 'Vazão consumida (m³/s)'
# titulo_grafico = 'Vazão consumida'
#PlotDemanda_categoria_unico(eixoy, serie_datas, matriz_demanda, matriz_carac, titulo_grafico)
###Volume
matriz_demanda = matrix_volume_dem
serie_oferta = serie_nivel2
a = SubmatrizCategorias(matriz_carac,matriz_demanda,serie_oferta)
# matriz_demanda = a[0]
m_NC = a[1]
m_CI = a[2]
m_CP = a[3]
m_D1 = a[4]
m_D2 = a[5]
m_D3 = a[6]
serie_datas_seca = a[7]
serie_oferta_seca = a[8]
#np.savetxt('serie_oferta_seca.txt',serie_oferta_seca)

a = SubmatrizCategorias(matriz_carac,matriz_demanda,serie_oferta)
# matriz_demanda = a[0]
m_NC = a[1]
m_CI = a[2]
m_CP = a[3]
m_D1 = a[4]
m_D2 = a[5]
m_D3 = a[6]
serie_datas_seca = a[7]
serie_oferta_seca = a[8]
xs = np.linspace(0, len(serie_datas_seca), 1)
ys = np.linspace(0, 700, 1)
# regras do biênio
y_yellow = 398
y_red = 220
d11 = '1/JULY/2018'
d21 = '1/AUGUST/2018'
d12 = '1/JULY/2019'
d22 = '1/AUGUST/2019'
d13 = '1/JULY/2020'
d23 = '1/AUGUST/2020'
d14 = '1/JULY/2021'
d24 = '1/AUGUST/2021'
d15 = '1/JULY/2022'
d25 = '1/AUGUST/2022'
plt.axhline(y=y_yellow, xmin=0, xmax=len(xs), linestyle='dashed', label='Atenção', linewidth=0.4, color='y')
plt.axhline(y=y_red, xmin=0, xmax=len(xs), linestyle='dashed', label='Restrição', linewidth=0.4, color='red')
# plt.axvline(x=d11, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
# plt.axvline(x=d12, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
# plt.axvline(x=d13, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
# plt.axvline(x=d14, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
# plt.axvline(x=d15, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='y')
# plt.axvline(x=d21, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
# plt.axvline(x=d22, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
# plt.axvline(x=d23, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
# plt.axvline(x=d24, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
# plt.axvline(x=d25, ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=0.4, color='red')
# plt.axvline(x='1/MAY/2018', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
# plt.axvline(x='1/MAY/2019', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
# plt.axvline(x='1/MAY/2020', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
# plt.axvline(x='1/MAY/2021', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
# plt.axvline(x='1/MAY/2022', ymin=0.0, ymax=len(ys), linestyle='dashed', linewidth=1.0, color='black')
# y = serie_oferta_seca[:,1]
plt.fill_between(serie_datas_seca, y_yellow, y_red, color='yellow', alpha=0.1)
plt.fill_between(serie_datas_seca, 0, y_red, color='red', alpha=0.1)
# plt.fill_betweenx(y, d11, d21, color='yellow', alpha=0.1)
# plt.fill_betweenx(y, d21, '31/AUGUST/2018', color='red', alpha=0.1)
# plt.fill_betweenx(y, d12, d22, color='yellow', alpha=0.1)
# plt.fill_betweenx(y, d22, '31/AUGUST/2019', color='red', alpha=0.1)
# plt.fill_betweenx(y, d13, d23, color='yellow', alpha=0.1)
# plt.fill_betweenx(y, d23, '31/AUGUST/2020', color='red', alpha=0.1)
# plt.fill_betweenx(y, d14, d24, color='yellow', alpha=0.1)
# plt.fill_betweenx(y, d24, '31/AUGUST/2021', color='red', alpha=0.1)
# plt.fill_betweenx(y, d15, d25, color='yellow', alpha=0.1)
# plt.fill_betweenx(y, d25, '31/AUGUST/2022', color='red', alpha=0.1)

plt.plot(serie_datas_seca,serie_oferta_seca[:,1])
labels = serie_datas_seca
plt.gcf().autofmt_xdate()
# plt.xticks(labels[::1])
plt.show()



# titulo_grafico = "Volume da bomba com regras"
# categoria = 'NC'
# matriz_categ = m_NC
# PlotBombaRegrasSeca(matriz_categ,categoria,serie_datas_seca,serie_oferta_seca,titulo_grafico)
# categoria = 'CI'
# matriz_categ = m_CI
# PlotBombaRegrasSeca(matriz_categ,categoria,serie_datas_seca,serie_oferta_seca,titulo_grafico)
# categoria = 'CP'
# matriz_categ = m_CP
# PlotBombaRegrasSeca(matriz_categ,categoria,serie_datas_seca,serie_oferta_seca,titulo_grafico)
# l = 1

# eixoy = 'Volume consumido (m³)'
# titulo_grafico = 'Volume consumido'
# PlotDemanda_categoria_unico(eixoy, serie_datas, matriz_demanda, matriz_carac, titulo_grafico)

##Duplos
###Chuva Vazao
###Chuva Volume
###Nivel Vazao
###Nivel Volume

# ##Triplos - Por irrigante
# ###Chuva x Vazao x Vazao
# serie_oferta1 = serie_chuva2
# eixoy1 = 'Chuva (mm)'
# serie_oferta2 = serie_nivel2
# eixoy3 = 'Nível (cm)'
# matriz_demanda = matrix_vazao_dem
# eixoy2 = 'Vazão consumida (m³/s)'
# titulo_grafico = "Chuva x Nível x 26798500 x Vazão"
# #Plot2OfertaDemanda_irrigante(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_carac,matriz_demanda,titulo_grafico)
# ###Chuva x Vazao x Volume
# serie_oferta1 = serie_chuva2
# eixoy1 = 'Chuva (mm)'
# serie_oferta2 = serie_nivel2
# eixoy3 = 'Nível (cm)'
# matriz_demanda = matrix_volume_dem
# eixoy2 = 'Volume consumido (m³)'
# titulo_grafico = "Chuva x Nível x 26798500 x Volume"
# #Plot2OfertaDemanda_irrigante(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_carac,matriz_demanda,titulo_grafico)

# ##Triplos - Por bomba
# ###Chuva x Vazao x Vazao
# serie_oferta1 = serie_chuva2
# eixoy1 = 'Chuva (mm)'
# serie_oferta2 = serie_nivel2
# eixoy3 = 'Nível (cm)'
# matriz_demanda = matrix_vazao_dem
# eixoy2 = 'Vazão consumida (m³/s)'
# titulo_grafico = "Chuva x Nível x 26798500 x Vazão"
# Plot2OfertaDemanda_bomba(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_demanda,titulo_grafico)
# ###Chuva x Vazao x Volume
# serie_oferta1 = serie_chuva2
# eixoy1 = 'Chuva (mm)'
# serie_oferta2 = serie_nivel2
# eixoy3 = 'Nível (cm)'
# matriz_demanda = matrix_volume_dem
# eixoy2 = 'Volume consumido (m³)'
# titulo_grafico = "Chuva x Nível x 26798500 x Volume"
# Plot2OfertaDemanda_bomba(eixoy1,eixoy2,eixoy3,serie_datas,serie_oferta1,serie_oferta2,matriz_demanda,titulo_grafico)
