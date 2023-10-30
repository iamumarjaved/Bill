import requests
import pandas as pd
import datetime
import os

def logista()->pd.DataFrame:
    data = {
        "name":os.environ.get("LOGISTA_USERNAME"),
        "password":os.environ.get("LOGISTA_PASSWORD")
    }
    response = requests.post(url = "https://myteseo.logesta.com/signin",json=data)

    token = response.json()['token']

    header = {'Authorization': "Bearer "+token}

    allplates = requests.get(url="https://myteseo.logesta.com/integration/v1.4/client/numberplates/",headers=header)
    list_of_plates = allplates.json()['data']

    if(len(list_of_plates) == 0):
        return

    list_of_platedata = []
    for plate in list_of_plates:
        plate_data = requests.get(url="https://myteseo.logesta.com/integration/v1.4/position/lastposition/"+plate, headers = header)
        data = plate_data.json()['data']
        if(data != None):
            list_of_platedata.append(data)
    if (len(list_of_platedata) == 0):
        return

    df = pd.DataFrame(list_of_platedata)
    df.drop(["id","truck_plate","delivery_note"],axis=1,inplace=True)
    df.rename(columns={"timestamp" : "timefromterminal","number_plate":"vrn","route":"heading"},inplace=True)
    df["timefromterminal"] = pd.to_datetime(df["timefromterminal"])
    df["timefromterminal"] = df["timefromterminal"].apply(lambda row:str(row).split("+")[0])
    df["ignition"] = 0
    return df