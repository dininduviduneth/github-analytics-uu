import json 
import requests
from pprint import pprint

token="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"
token = {'Authorization': 'token ' + token}
for i in range (40):
    url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+archived:false&per_page=100&page=1"
    repositories = requests.get(url,headers=token).json()
    data={}
    for i in range(100):
        try:
            repo_name=repositories['items'][i]['full_name']
            spec_repo_url=requests.get(f"https://api.github.com/repos/{repo_name}/hooks",headers=token).json()
            pprint(spec_repo_url)  

        except:
            continue
print(data)
# print(repo_name)