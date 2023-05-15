import json 
import requests
from pprint import pprint
#access token from my github account 
token="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"
token = {'Authorization': 'token ' + token}
data={}
#iterate through the pages of the search repos api call
for i in range (1,2):
    url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+archived:false&per_page=100&page={i}"
    repositories = requests.get(url,headers=token).json()
    data={}
    for j in range(100):
        try:
            repo_name=repositories['items'][j]['full_name']
            #check if there exists runs if it return an empy json it means we dont have a github workflow which means no CICD
            spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=token).json()
            print(f"The repository {repo_name}")
            if spec_repo['total_count'] > 0:
                print(f"uses continuous integration.")
                ci_cd= True
            else:
                ci_cd= False
            
            # We check the name of each file and directory in the root directory of the repo and if it is named test or similar  
            # we assume they use test driven  development 
            spec_repo_contents=requests.get(f"https://api.github.com/repos/{repo_name}/contents",headers=token).json()
            test_driven_development= False
            for i in spec_repo_contents:
                if "test" in i['name'].lower():
                    print(f"uses test based development.")
                    test_driven_development= True
                    

            data[f"{repo_name}"]=[ci_cd,test_driven_development]
        except:
            continue
print(data)
# print(repo_name)