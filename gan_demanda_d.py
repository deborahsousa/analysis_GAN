import requests
import numpy as np

def get_historic_serie(id): #gets data from a pump (id) and returns a json file
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/seriehistorica/medias/{id}?tipoRegistro=CONSUMO")
    return r.json()

def get_interventions_list(): #gets data from the list of all pumps (intervenções) and returns a json file
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/list")
    return r.json()

if __name__ == "__main__":
    intervention_list = get_interventions_list() #

    interest_years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]
    interest_months = ["MAY", "JUNE", "JULY", "AUGUST"]
    #interest_months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
    for i in range(0,len(interest_months)):
        if interest_months[i] == "JUNE":
            interest_days = np.arange(1, 31, 1)
        else:
            interest_days = np.arange(1, 32, 1)

    with open('resultVazao.csv', 'w') as f: #returns a csv file

        header = f"id,rotulo" #header of the csv file
        for y in interest_years:
            for m in interest_months:
                for d in interest_days:
                    header += f",{d}/{m}/{y}" #date format dd/month/yyyy

        f.write(header + "\n")
        print(header)

        for pump in intervention_list: #dictionary functions to get specific data from each intervention (pump)
            id = pump["intervencao"]["id"]
            ativo = pump["intervencao"]["active"]
            rotulo = pump["intervencao"]["rotulo"]
            long = pump["intervencao"]["longitude"]
            lat = pump["intervencao"]["latitude"]
            area_irrig = pump["intervencao"]["propriedade"]["areaIrrigada"]
            tipo = pump["intervencao"]["tipo"]

            historic_serie = get_historic_serie(pump["intervencao"]["id"]) #access each pump data by using the "id" key
            vazao = historic_serie[0] #the index 0 of the historic serie
            volume = historic_serie[1]  #the index 1 of the historic serie

            resultsVazao = []
            resultsVolume = []

            for year in interest_years:
                if year not in vazao["yearsAvailable"]:
                   for _ in interest_months: # _ (lambda) represents any variable in the referred container
                       for _ in interest_days:
                        resultsVazao.append(-1) # adds -1 to each day if there is no available data in this year
                   continue
                data_by_month = next(y for y in vazao["dataByYear"] if y["year"] == year)

                for month in interest_months:
                    data_by_day = data_by_month["valuesByMonth"][month]["valorDiarios"]
                    resultsVazao += data_by_day

            out = f"{id},{rotulo}"
            for r in resultsVazao:
                out += f",{r}"

            f.write(out + "\n")
            print(out)