import requests
import os
import json 

k=requests.get("https://api.github.com/search/repositories?q=language:javascript+react")
k=k.json()
print(len(k['items']))
