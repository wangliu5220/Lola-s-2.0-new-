import requests
from bs4 import BeautifulSoup
import json

walmart_url = "https://www.walmart.com/ip/Caribou-Coffee-Caramel-Hideaway-Flavored-Premium-Medium-Roast-Ground-Coffee-Arabica-11-oz/49679218?classType=VARIANT&from=/search"



Headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
    "referer": "https://www.walmart.com/",
}

response = requests.get(walmart_url, headers=Headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# print(soup)

script_tag = soup.find("script", id="__NEXT_DATA__")

data = json.loads(script_tag.string)

with open('rand_data.json', 'w') as f:
    json.dump(data, f, indent=4)

