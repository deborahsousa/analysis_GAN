import requests


def get_historic_serie(id):
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/seriehistorica/medias/{id}?tipoRegistro=CONSUMO")
    return r.json()


def get_interventions_list():
    r = requests.get(f"https://gan.iacuft.org.br/api/intervencoes/list")
    return r.json()


if __name__ == "__main__":
    intervention_list = get_interventions_list()

    interest_years = [2016, 2017, 2018, 2019, 2020, 2021]
    interest_month = ["MAY", "JUNE", "JULY", "AUGUST"]

    with open('result.csv', 'w') as f:

        header = f"id,rotulo,long,lat"
        for y in interest_years:
            for m in interest_month:
                header += f",{m}/{y}"

        f.write(header + "\n")
        print(header)

        for pump in intervention_list:
            id = pump["intervencao"]["id"]
            rotulo = pump["intervencao"]["rotulo"]
            long = pump["intervencao"]["longitude"]
            lat = pump["intervencao"]["latitude"]

            historic_serie = get_historic_serie(pump["intervencao"]["id"])
            vazao = historic_serie[0]

            results = []
            for year in interest_years:
                if year not in vazao["yearsAvailable"]:
                    for _ in interest_month:
                        results.append(-1)
                    continue

                data_by_month = next(y for y in vazao["dataByYear"] if y["year"] == year)

                for month in interest_month:
                    data_by_day = data_by_month["valuesByMonth"][month]

                    days_without_data = len([d for d in data_by_day["valorDiarios"] if d is None])
                    results.append(days_without_data)

            out = f"{id},{rotulo},{long},{lat}"
            for r in results:
                out += f",{r}"

            f.write(out + "\n")
            print(out)
