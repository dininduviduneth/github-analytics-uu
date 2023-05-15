import json 
import requests
from pprint import pprint
#list of our personanl tokens
tokens=["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"]
#access token personal github account 
token = {'Authorization': 'token ' + tokens.pop()}
#api call to get the json which just returns the list of repositories 
url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+created:>2022-05-01+archived:false&per_page=100"
repositories = requests.get(url,headers=token).json()
data={}
#iterate through the repos 
for i in range(100):
    try:
        repo_name=repositories['items'][i]['full_name']
        language=repositories['items'][i]['language']
        #if the repo has no code we dont analyze
        if language==None:
            continue
        # api call to specific repo to find the number of commits
        # in order to do that we paginate to show one commit per page 
        # and from the metadata we can extact the number of the last page which would be the number of commits 
        spec_repo_url=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1",headers=token)
        headers = spec_repo_url.headers
        commits=int(headers['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
        data[f'{repo_name}']=[language,commits]
    except:
        continue
print(data)

