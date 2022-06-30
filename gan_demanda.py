import requests

def get_historic_serie(id):
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/seriehistorica/medias/{id}?tipoRegistro=CONSUMO")
    return r.json()

def get_interventions_list():
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/list")
    return r.json()

if __name__ == "__main__":
    intervention_list = get_interventions_list()

    interest_years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]
    #interest_month = ["MAY", "JUNE", "JULY", "AUGUST"]
    interest_month = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

    with open('resultVazao.csv', 'w') as f:

        header = f"id,ativo,rotulo,long,lat,area_irrig,tipo"
        for y in interest_years:
            for m in interest_month:
                header += f",{m}/{y}"

        f.write(header + "\n")
        print(header)

        for pump in intervention_list:
            id = pump["intervencao"]["id"]
            ativo = pump["intervencao"]["active"]
            rotulo = pump["intervencao"]["rotulo"]
            long = pump["intervencao"]["longitude"]
            lat = pump["intervencao"]["latitude"]
            area_irrig = pump["intervencao"]["propriedade"]["areaIrrigada"]
            tipo = pump["intervencao"]["tipo"]

            historic_serie = get_historic_serie(pump["intervencao"]["id"])
            vazao = historic_serie[0]
            volume = historic_serie[1]
            cobranca = historic_serie[2]
            duracao = historic_serie[3]

            resultsVazao = []
            resultsVolume = []
            resultsDuracao = []
            #resultsCobranca = []

            for year in interest_years:
                if year not in vazao["yearsAvailable"]:
                   for _ in interest_month:
                       resultsVazao.append(-1)
                   continue
                data_by_month = next(y for y in vazao["dataByYear"] if y["year"] == year)

                for month in interest_month:
                    #data_by_day = data_by_month["valuesByMonth"][month]
                    vazaoMedia = data_by_month["valuesByMonth"][month]["aggregateValue"]
                    resultsVazao.append(vazaoMedia)
                    #days_without_data = len([d for d in data_by_day["valorDiarios"] if d is None])
                    #results.append(days_without_data)

            out = f"{id},{ativo},{rotulo},{long},{lat},{area_irrig},{tipo}"
            for r in resultsVazao:
                out += f",{r}"

            f.write(out + "\n")
            print(out)

    with open('resultVolume.csv', 'w') as f:

        header = f"id,ativo,rotulo"
        for y in interest_years:
            for m in interest_month:
                header += f",{m}/{y}"

        f.write(header + "\n")
        print(header)

        for pump in intervention_list:
            id = pump["intervencao"]["id"]
            ativo = pump["intervencao"]["active"]
            rotulo = pump["intervencao"]["rotulo"]

            historic_serie = get_historic_serie(pump["intervencao"]["id"])
            vazao = historic_serie[0]
            volume = historic_serie[1]
            cobranca = historic_serie[2]
            duracao = historic_serie[3]

            resultsVazao = []
            resultsVolume = []
            resultsDuracao = []
            #resultsCobranca = []

            for year in interest_years:
                if year not in volume["yearsAvailable"]:
                   for _ in interest_month:
                       resultsVolume.append(-1)
                   continue
                data_by_month = next(y for y in volume["dataByYear"] if y["year"] == year)

                for month in interest_month:
                    VolumeTotal = data_by_month["valuesByMonth"][month]["aggregateValue"]
                    resultsVolume.append(VolumeTotal)

            out = f"{id},{ativo},{rotulo}"
            for r in resultsVolume:
                out += f",{r}"

            f.write(out + "\n")
            print(out)

    with open('resultsDuracao.csv', 'w') as f:

        header = f"id,ativo,rotulo"
        for y in interest_years:
            for m in interest_month:
                header += f",{m}/{y}"

        f.write(header + "\n")
        print(header)

        for pump in intervention_list:
            id = pump["intervencao"]["id"]
            ativo = pump["intervencao"]["active"]
            rotulo = pump["intervencao"]["rotulo"]

            historic_serie = get_historic_serie(pump["intervencao"]["id"])
            vazao = historic_serie[0]
            volume = historic_serie[1]
            cobranca = historic_serie[2]
            duracao = historic_serie[3]

            resultsVazao = []
            resultsVolume = []
            resultsDuracao = []
            #resultsCobranca = []

            for year in interest_years:
                if year not in volume["yearsAvailable"]:
                   for _ in interest_month:
                       resultsDuracao.append(-1)
                   continue
                data_by_month = next(y for y in duracao["dataByYear"] if y["year"] == year)

                for month in interest_month:
                    DuracaoTotal = data_by_month["valuesByMonth"][month]["aggregateValue"]
                    resultsDuracao.append(DuracaoTotal)

            out = f"{id},{ativo},{rotulo}"
            for r in resultsDuracao:
                out += f",{r}"

            f.write(out + "\n")
            print(out)