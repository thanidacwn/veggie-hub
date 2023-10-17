import requests

url = "https://github.com/thanidacwn/veggie-data/blob/master/last_data.csv"
response = requests.get(url)
print(response.json())