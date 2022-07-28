import os
from requests import *
from datetime import *
id = os.getenv('id')
token = os.getenv('TOKEN')
sheety_link= os.getenv('sheety')
sheety_endpoint = f'https://api.sheety.co/{sheety_link}/workoutsDatabase/workouts'
exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
header = {
    'x-app-id': id,
    'x-app-key': token,
    'x-remote-user-id': '0'
}
exercise_input = {
    'query': input('What did you do at the gym today ?\nAnswer:'),
}
data = post(url=exercise_endpoint, json=exercise_input, headers=header).json()['exercises']
data_dic = [{
    'name': i['user_input'],
    'duration': i['duration_min'],
    'calories': i['nf_calories']
} for i in data]
# --------- excel part ------------
sheety_header = {
    'Authorization': os.getenv('sheety_header')
}
today = datetime.now()
# ---------------updating table--------
for i in data_dic:
    sheety_input = {
        'workout': {
            'date': today.strftime('%d/%m/%Y'),
            'time': today.strftime('%H:%M:%S'),
            'exercise': i['name'].title(),
            'duration':i['duration'],
            'calories': i['calories'],
        }}
    post(url=sheety_endpoint,headers=sheety_header,json=sheety_input)
