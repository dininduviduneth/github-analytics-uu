import json 
import requests
from pprint import pprint

token="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"
token = {'Authorization': 'token ' + token}
url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+archived:false&per_page=100"
repositories = requests.get(url,headers=token).json()
data={}
for i in range(100):
    try:
        repo_name=repositories['items'][i]['full_name']
        language=repositories['items'][i]['language']
        spec_repo_url=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1",headers=token)
        headers = spec_repo_url.headers
        # pprint(headers['Link'])
        commits=int(headers['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
        data[f'{repo_name}']=[language,commits]
    except:
        continue
print(data)
# print(repo_name)
