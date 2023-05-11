import json 
import requests
from pprint import pprint
#access token from my github account 
token="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"
token = {'Authorization': 'token ' + token}
data={}
#iterate through the pages of the search repos api call
for i in range (5):
    url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+archived:false&per_page=100&page={i}"
    repositories = requests.get(url,headers=token).json()
    data={}
    for j in range(100):
        try:
            repo_name=repositories['items'][j]['full_name']
            #check if there exists runs if it return an empy json it means we dont have a github workflow which means no CICD
            spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=token).json()
            if spec_repo['total_count'] > 0:
                print(f"The repository {repo_name} uses continuous integration.")
            else:
                continue 
        except:
            continue
print(data)
# print(repo_name)