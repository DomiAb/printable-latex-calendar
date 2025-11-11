import requests

from config import Holiday


def get_german_holidays(year) -> list[Holiday]:
    url = f"https://feiertage-api.de/api/?jahr={year}&nur_land=BY"
    response = requests.request("GET", url, headers={}, data={})

    result = []
    response = response.json()
    for key in response:
        date_parts = response[key]['datum'].split("-")
        month = int(date_parts[1])
        day = int(date_parts[2])
        name = key
        
        if response[key]["hinweis"] != "" and "Himmelfahrt" not in name:
            continue

        if "Mariä Himmelfahrt" in name:
            name = "Mariä HF."
        if "1. Weihnachtstag" in name:
            name = "Erster Weihnachtstag"
        if "2. Weihnachtstag" in name:
            name = "Zweiter Weihnachtstag"

        result.append(Holiday(month=month, day=day, name=name))

    return result


def get_public_holidays(year):
    return get_german_holidays(year)
