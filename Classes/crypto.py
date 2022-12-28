import requests

key = '87e27720-92d8-4e1a-814f-570061a395ec'

headers = {
    'X-CMC_PRO_API_KEY' : key,
    'Accepts' : 'application/json'
}

params = {
    'start' : '1',
    'limit' : '5',
    'convert' : 'EUR'
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

json = requests.get(url, params=params, headers=headers).json()

coins = json['data']

def GiveACoin():
    for x in coins:
        print(x['symbol'], x['quote']['EUR']['price'])
