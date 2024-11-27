import requests
import json
with open("openroute_key.txt", "r") as openroutekey_file:
    openroute_key = openroutekey_file.read()

openroutekey_file.close()

#needs lon first, then lat
# coords_1 = [-0.1022093, 51.5243278]
# coords_2 = [48.8582637, 2.2942401]
# coords_3 = [-1.028020, 51.320790]

def get_directions(coords_1, coords_3):
    body = {
        "coordinates":[
            coords_1,
            coords_3
        ]
    }

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization' : '5b3ce3597851110001cf62480b06e857f378414f9c410c1b4ab80066',
        'Content-Type' : 'application/json; charset=utf-8'
    }

    route_response = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=body, headers=headers) 
    meta_directions = route_response.json()

    steps = meta_directions['routes'][0]['segments'][0]['steps']
    total_steps = ''

    for direction in steps:
        total_steps += direction['instruction'] + '\n'
    #directions = [direction['instruction'] for direction in steps]
    return total_steps