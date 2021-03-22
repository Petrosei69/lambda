import json
from botocore.vendored import requests


def lambda_handler(event, context):
    print(event)
    # print (context)
    update = json.loads(event['body'])
    id2 = update['message']['chat']['id']
    if 'location' in update['message']:
        lon = update['message']['location']['longitude']
        lat = update['message']['location']['latitude']
        # print(lat)
        # print(lon)
        # lon = 30.345205
        # lat = 59.905793
        token = "0ee6eefdb5cc2a7cdfea1bdf123fd5502eccf999"
        response = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address', json={
            'lat': lat, 'lon': lon}, headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
        })
        if response:
            suggestions = response.json()['suggestions']
            if len(suggestions) != 0:
                text = ""
                for s in suggestions:
                    text += s['value'] + "\n"
            else:
                text = 'Ничего не найдено'

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(
                {
                    'method': 'sendMessage',
                    'chat_id': id2,
                    'text': text,
                }
            )
        }

    else:
        text = 'Отправьте пожалуйста геопозицию, ничего другого определять я не умею :('
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(
                {
                    'method': 'sendMessage',
                    'chat_id': id2,
                    'text': text,
                }
            )
        }