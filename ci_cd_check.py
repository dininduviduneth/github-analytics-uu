import json 
import requests
from pprint import pprint

token="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"
token = {'Authorization': 'token ' + token}
for i in range (10):
    url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+archived:false&per_page=100&page=1"
    repositories = requests.get(url,headers=token).json()
    data={}
    for i in range(100):
        try:
            repo_name=repositories['items'][i]['full_name']
            spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=token).json()
            if spec_repo['total_count'] > 0:
                print(f"The repository {repo_name} uses continuous integration.")
            else:
                continue 
        except:
            continue
print(data)
# print(repo_name)