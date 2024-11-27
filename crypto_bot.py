from openai import AzureOpenAI
import os
import requests
import json

client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview" 
)

messages = [
    {
        "role" : "system",
        "content" : "Respond to everything like a moody teenager"
    },
    {
        "role" : "user",
        "content" : "Find the coordinates of On the Hoof Sydenham"
    }
]

def crypto_price(crypto_name, fiat_currency):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={fiat_currency}"
    response = requests.get(url)
    data = response.json()
    current_price = [coin['current_price'] for coin in data if coin['id'] == crypto_name][0]
    return f"I think the current price of {crypto_name} in {fiat_currency} is {current_price} {fiat_currency}"

def directions(coords_1, coords_3):
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
    return f"Okay. You have to {total_steps}"

def coordinates(address):
    geo_url = f"https://geocode.maps.co/search?q={address}&api_key={geo_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    return f"Here are the coordinates of {address}: {lat}, {lon} "

functions = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_crypto_price",
            "description" : "Gets prices of crypto currency in a specified global currency",
            "parameters" : {
                "type" : "object", #tells chat-gpt to return key/value pairs
                "properties" : {
                    "crypto_name" : {
                        "type" : "string",
                        "description" : "The name of the crypto currency that I want to look at"
                    },
                    "fiat_currency" : {
                        "type" : "string",
                        "description" : "The fiat currency for defining the price of crypto. Use the official abbreviation"
                    }
                },
                "required" : ["crypto_name", "fiat_currency"]
            }
        }
    }
]

response = client.chat.completions.create(
    model = "gpt-4",
    messages=messages,
    tools = functions,
    tool_choice = "auto"
)

response_message = response.choices[0].message

gpt_tools = response.choices[0].message.tool_calls #list of tools/functions used by chatgpt

if gpt_tools:
    available_functions = {
        "get_crypto_price" : crypto_price
    }

    messages.append(response_message)
    for gpt_tool in gpt_tools:
        function_name = gpt_tool.function.name
        function_to_call = available_functions[function_name]
        function_parameters = json.loads(gpt_tool.function.arguments)
        function_response = function_to_call(function_parameters.get('crypto_name'), function_parameters.get('fiat_currency'))
        
        messages.append(
            {
                "tool_call_id" : gpt_tool.id,
                "role" : "tool",
                "name" : function_name,
                "content" : function_response
            }
        )
        second_response = client.chat.completions.create(
            model = "GPT-4",
            messages=messages
        )
        print(second_response.choices[0].message)

else:
    print(response.choices[0].message.content)