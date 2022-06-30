import requests
import numpy as np

def get_historic_serie(id): #function that gets historic data of a specific id
    r = requests.get(f"https://gan.iacuft.org.br/api/estacoes/seriehistorica/medias/{id}")
    return r.json()
#134
#136
def get_stations_list(): #function that gets id list from the api
    r = requests.get(f"https://gan.iacuft.org.br/api/estacoes/list")
    return r.json()

if __name__ == "__main__": # get id list
    station_list = get_stations_list()

    interest_years = [2018, 2019, 2020, 2021, 2022]
    interest_months = ["MAY", "JUNE", "JULY", "AUGUST"]
    #interest_months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
    interest_days = np.arange(1, 32, 1)

    with open('resultsChuva.csv', 'w') as f:

        header = f"id,codigo"
        for y in interest_years:
            for m in interest_months:
                for d in interest_days:
                    header += f",{d}/{m}/{y}"  # date format dd/month/yyyy

        f.write(header + "\n")
        print(header)
#id 10 e 35
        for station in station_list:
            id = station["estacao"]["id"]
            codigo = station["estacao"]["codigo"]
            if id != 10 and id != 35:
                continue
            # long = station["estacao"]["longitude"]
            # lat = station["estacao"]["latitude"]
            # nome = station["estacao"]["nome"]
            # tipoLeitura = station["estacao"]["tipoLeitura"]
            # tipoEstacao = station["estacao"]["tipoEstacao"]
            historic_serie = get_historic_serie(station["estacao"]["id"])
            chuva = historic_serie[2]
            # vazao = historic_serie[0]
            # nivel = historic_serie[1]

            resultsChuva = []

            for year in interest_years:
                if year not in chuva["yearsAvailable"]:
                    for _ in interest_months:
                        for _ in interest_days:
                            resultsChuva.append(-1)
                    continue
                data_by_month = next(y for y in chuva["dataByYear"] if y["year"] == year)

                for month in interest_months:
                    data_by_day = data_by_month["valuesByMonth"][month]["valorDiarios"]
                    resultsChuva += data_by_day

            out = f"{id},{codigo}"
            for r in resultsChuva:
                out += f",{r}"

            f.write(out + "\n")
            print(out)

    with open('resultsVazao.csv', 'w') as f:

        header = f"id,codigo"
        for y in interest_years:
            for m in interest_months:
                for d in interest_days:
                    header += f",{d}/{m}/{y}"  # date format dd/month/yyyy

        f.write(header + "\n")
        print(header)
        # id 10 e 35
        for station in station_list:
            id = station["estacao"]["id"]
            codigo = station["estacao"]["codigo"]
            if id != 10 and id != 35:
                continue
            # long = station["estacao"]["longitude"]
            # lat = station["estacao"]["latitude"]
            # nome = station["estacao"]["nome"]
            # tipoLeitura = station["estacao"]["tipoLeitura"]
            # tipoEstacao = station["estacao"]["tipoEstacao"]
            else:
                historic_serie = get_historic_serie(station["estacao"]["id"])
                #chuva = historic_serie[0]
                vazao = historic_serie[1]
                # nivel = historic_serie[2]

                resultsVazao = []

                for year in interest_years:
                    if year not in vazao["yearsAvailable"]:
                        for _ in interest_months:
                            resultsVazao.append(-1)
                        continue
                    data_by_month = next(y for y in chuva["dataByYear"] if y["year"] == year)

                    for month in interest_months:
                        data_by_day = data_by_month["valuesByMonth"][month]["valorDiarios"]
                        resultsVazao += data_by_day

                out = f"{id},{codigo}"
                for r in resultsVazao:
                    out += f",{r}"

                f.write(out + "\n")
                print(out)

    with open('resultsNivel.csv', 'w') as f:

        header = f"id,codigo"
        for y in interest_years:
            for m in interest_months:
                for d in interest_days:
                    header += f",{d}/{m}/{y}"  # date format dd/month/yyyy

        f.write(header + "\n")
        print(header)
        # id 10 e 35
        for station in station_list:
            id = station["estacao"]["id"]
            codigo = station["estacao"]["codigo"]
            if id != 10 and id != 35:
                continue
            # long = station["estacao"]["longitude"]
            # lat = station["estacao"]["latitude"]
            # nome = station["estacao"]["nome"]
            # tipoLeitura = station["estacao"]["tipoLeitura"]
            # tipoEstacao = station["estacao"]["tipoEstacao"]
            else:
                historic_serie = get_historic_serie(station["estacao"]["id"])
                # chuva = historic_serie[0]
                #vazao = historic_serie[1]
                nivel = historic_serie[2]

                resultsNivel = []

                for year in interest_years:
                    if year not in vazao["yearsAvailable"]:
                        for _ in interest_months:
                            resultsNivel.append(-1)
                        continue
                    data_by_month = next(y for y in nivel["dataByYear"] if y["year"] == year)

                    for month in interest_months:
                        data_by_day = data_by_month["valuesByMonth"][month]["valorDiarios"]
                        resultsNivel += data_by_day

                out = f"{id},{codigo}"
                for r in resultsNivel:
                    out += f",{r}"

                f.write(out + "\n")
                print(out)
        # for station in station_list:
        #     id = station["estacao"]["id"]
        #     codigo = station["estacao"]["codigo"]
        #     # long = station["estacao"]["longitude"]
        #     # lat = station["estacao"]["latitude"]
        #     # nome = station["estacao"]["nome"]
        #     # tipoLeitura = station["estacao"]["tipoLeitura"]
        #     # tipoEstacao = station["estacao"]["tipoEstacao"]
        #
        #     historic_serie = get_historic_serie(station["estacao"]["id"])
        #     chuva = historic_serie[0]
        #     # vazao = historic_serie[1]
        #     # nivel = historic_serie[2]
        #
        #     resultsChuva = []
        #
        #     for year in interest_years:
        #         if year not in chuva["yearsAvailable"]:
        #            for _ in interest_months:
        #                resultsChuva.append(-1)
        #            continue
        #         data_by_month = next(y for y in chuva["dataByYear"] if y["year"] == year)
        #
        #         for month in interest_months:
        #             data_by_day = data_by_month["valuesByMonth"][month]["valorDiarios"]
        #             resultsChuva += data_by_day
        #
        #     out = f"{id},{codigo}"
        #     for r in resultsChuva:
        #         out += f",{r}"
        #
        #     f.write(out + "\n")
        #     print(out)

# with open('resultsVazao.csv', 'w') as f:
#
#     header = f"id,codigo,long,lat,nome,tipoLeitura,tipoEstacao"
#     for y in interest_years:
#         for m in interest_months:
#             header += f",{m}/{y}"
#
#     f.write(header + "\n")
#     print(header)
#
#     for station in station_list:
#         id = station["estacao"]["id"]
#         codigo = station["estacao"]["codigo"]
#         long = station["estacao"]["longitude"]
#         lat = station["estacao"]["latitude"]
#         nome = station["estacao"]["nome"]
#         tipoLeitura = station["estacao"]["tipoLeitura"]
#         tipoEstacao = station["estacao"]["tipoEstacao"]
#
#         historic_serie = get_historic_serie(station["estacao"]["id"])
#         chuva = historic_serie[0]
#         vazao = historic_serie[1]
#         nivel = historic_serie[2]
#
#         for year in interest_years:
#             if year not in vazao["yearsAvailable"]:
#                for _ in interest_months:
#                    resultsVazao.append(-1)
#                continue
#             data_by_month = next(y for y in vazao["dataByYear"] if y["year"] == year)
#
#             for month in interest_months:
#                 vazaoMedia = data_by_month["valuesByMonth"][month]["aggregateValue"]
#                 resultsVazao.append(vazaoMedia)
#
#         out = f"{id},{codigo},{long},{lat},{nome},{tipoLeitura},{tipoEstacao}"
#         for r in resultsVazao:
#             out += f",{r}"
#
#         f.write(out + "\n")
#         print(out)
#
# with open('resultsNivel.csv', 'w') as f:
#
#     header = f"id,codigo,long,lat,nome,tipoLeitura,tipoEstacao"
#     for y in interest_years:
#         for m in interest_months:
#             header += f",{m}/{y}"
#
#     f.write(header + "\n")
#     print(header)
#
#     for station in station_list:
#         id = station["estacao"]["id"]
#         codigo = station["estacao"]["codigo"]
#         long = station["estacao"]["longitude"]
#         lat = station["estacao"]["latitude"]
#         nome = station["estacao"]["nome"]
#         tipoLeitura = station["estacao"]["tipoLeitura"]
#         tipoEstacao = station["estacao"]["tipoEstacao"]
#
#         historic_serie = get_historic_serie(station["estacao"]["id"])
#         chuva = historic_serie[0]
#         vazao = historic_serie[1]
#         nivel = historic_serie[2]
#
#         for year in interest_years:
#             if year not in nivel["yearsAvailable"]:
#                for _ in interest_months:
#                    resultsNivel.append(-1)
#                continue
#             data_by_month = next(y for y in nivel["dataByYear"] if y["year"] == year)
#
#             for month in interest_months:
#                 nivelMedio = data_by_month["valuesByMonth"][month]["aggregateValue"]
#                 resultsNivel.append(nivelMedio)
#
#         out = f"{id},{codigo},{long},{lat},{nome},{tipoLeitura},{tipoEstacao}"
#         for r in resultsNivel:
#             out += f",{r}"
#
#         f.write(out + "\n")
#         print(out)