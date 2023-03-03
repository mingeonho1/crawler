import json
import requests


def emotional_analysis(text):
    client_id = "id"
    client_secret = "key"
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json;charset=utf-8"
    }
    data = {
        "content": text
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    res = response.status_code
    if res == 200:
        senti = json.loads(response.text)['document']['sentiment']
        return senti
    else:
        print("Error : " + response.text)
        return "neutral"
