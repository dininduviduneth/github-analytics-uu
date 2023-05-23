import pulsar
import json
import requests
from pprint import pprint
import pymongo
token="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"
headers = {'Authorization': 'token ' + token}
myclient = pymongo.MongoClient("mongodb://root:example@192.168.2.51:27017/")
mydb = myclient["mydatabase_test"]
mycol = mydb["repositories_test"]
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.51:6650')
data={}
# Subscribe to a topic and subscription
consumer1 = client.subscribe('repositories_testtest1', subscription_name='question4')
while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    #check if there exists runs if it return an empy json it means we dont have a github workflow which means no CICD
    #spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs").json() #without token 
    spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=headers).json()
    if spec_repo['total_count'] > 0:
        print(f"uses continuous integration.")
        ci_cd= True
    else:
        ci_cd= False
            
    if ci_cd:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "has_cicd": True
            }
        }

        result = mycol.update_one(filter, update)

        print("Matched:", result.matched_count)
        print("Modified:", result.modified_count)
    

    ###this is for checking that the connect
    data[f"{repo_name}"]=ci_cd
    print(f"{repo_name} {data[f'{repo_name}']} ")
client.close()