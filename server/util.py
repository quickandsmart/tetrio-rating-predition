import json
import pickle
import numpy as np
import requests
import pandas as pd
import math
import time
from datetime import datetime, timedelta

__df_predict = None
__data_columns = None
__model = None
__last_api_request = 0

def calculate_level(xp):
    level = (xp/500)**0.6 + xp / (5000 + max(0, xp - 4*(10**6)) / 5000) + 1
    return math.floor(level)

def get_actual_TR():
    actual = round(__df_predict['league.rating'].iloc[0], 2)
    return actual

def get_player(user):
    global __df_predict
    global __last_api_request
    current_time = time.time()
    if current_time - __last_api_request < 1:
        time.sleep(1 - (current_time - __last_api_request))
    response = requests.get(f"https://ch.tetr.io/api/users/{user.lower()}")
    data_predict = response.json()
    df_predict = pd.DataFrame(data_predict)
    __df_predict = pd.json_normalize(df_predict['data'])

    __last_api_request = time.time()

    return user.lower()

def get_predicted_TR(user):

    x = pd.DataFrame(data=np.zeros((1, len(__data_columns))), columns=__data_columns)

    if (__df_predict['supporter_tier'].iloc[0] > 0):
        x['supporter'] = 1
    else:
        x['supporter'] = 0

    x['league.gamesplayed'] = __df_predict['league.gamesplayed'].iloc[0]
    x['league.gameswon'] = __df_predict['league.gameswon'].iloc[0]
    x['league.apm'] = __df_predict['league.apm'].iloc[0]
    x['league.pps'] = __df_predict['league.pps'].iloc[0]
    x['league.vs'] = __df_predict['league.vs'].iloc[0]
    x['league.winper'] = __df_predict['league.gameswon'].iloc[0] / __df_predict['league.gamesplayed'].iloc[0]
    x['level'] = calculate_level(__df_predict['xp'].iloc[0])

    rank = __df_predict['league.bestrank'].iloc[0]
    if ((rank != 'x')):
        x[rank] = 1

    rd = get_RD(__df_predict['_id'][0], __df_predict['league.rd'][0])

    predicted_glicko = __model.predict(x)[0]
    print(predicted_glicko)
    predicted = calculate_TR(predicted_glicko,rd)

    return predicted

def calculate_TR(glicko,rd):
    TR = round(25000/(1+np.power(10, (1500-glicko)*np.pi/(np.sqrt(3*np.log(10)*np.log(10)*rd*rd+2500*(64*np.pi*np.pi+147*np.log(10)*np.log(10)))))), 2)
    return TR

def get_RD(user_id, rd):
    response = requests.get(f"https://ch.tetr.io/api/streams/league_userrecent_{user_id}")
    user_data = response.json()
    df_user = pd.DataFrame(user_data)
    df_user1 = pd.json_normalize(df_user['data']).T
    df_user2 = pd.json_normalize(df_user1[0],sep =',')
    try:
        date = datetime.strptime(df_user2['ts'][0], '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return 70

    now = datetime.utcnow()
    week_ago = now - timedelta(weeks=1)

    if date < week_ago:
        day_difference = now - date
        rd_change = day_difference.days
        return rd-rd_change
    else:
        return rd



def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]

    global __model
    if __model is None:
        with open('./artifacts/tr_prediction_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    global __df_predict


    print("loading saved artifacts...done")

def compare_prediction(user):
    player = get_player(user)
    actual = get_actual_TR()
    predicted = get_predicted_TR(user)
    return f"{'Player:':<15} {player}   \n{'Actual TR:':<15} {actual}\n{'Predicted TR:':<15} {predicted}\n"

if __name__ == '__main__':
    load_saved_artifacts()
    print(compare_prediction('icly'))
    print(compare_prediction('quickandsmart'))
    print(compare_prediction('kiken'))
    print(compare_prediction('atombolders'))