import requests
import json
import datetime
def getCovid():
    country="india"
    date=str(datetime.datetime.today() - datetime.timedelta(days=2)).split()
    print(date[0])
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'NbKjdyVi8IRjVrjdxnRRww==k1uFWWpUtPH0XYhG'})
    # response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        try:
            api = json.loads(response.content)
            print((api[0]['country']))
            print((api[0]['cases'][date[0]]))
            return api[0]['cases'][date[0]],date[0]
        except Exception as e:
            api = "oops! There was an error"
            print(e)
    else:
        print("Error:", response.status_code, response.text)

getCovid()