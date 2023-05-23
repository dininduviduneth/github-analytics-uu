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
consumer1 = client.subscribe('repositories_testtest2', subscription_name='question2')
while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    # commits=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1") # without token 
    commits=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1",headers=headers)
    commits = commits.headers
    num_commits=int(commits['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
    filter = {
        "full_name": repo_name
    }

    update = {
        "$set": {
            "commits": num_commits
        }
    }

    result = mycol.update_one(filter, update)

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)


    
    ###this is for checking that the connect
    data[f'{repo_name}']=num_commits
    print(f"{repo_name} {data[f'{repo_name}']} ")
client.close()