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
consumer1 = client.subscribe('repositories_testtest', subscription_name='question3')
while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    #spec_repo_contents=requests.get(f"https://api.github.com/repos/{repo_name}/contents").json()# without token
    spec_repo_contents=requests.get(f"https://api.github.com/repos/{repo_name}/contents",headers=headers).json()
    test_driven_development= False
    for i in spec_repo_contents:
        if "test" in i['name'].lower():
            print(f"uses test based development.")
            test_driven_development= True
            
    if test_driven_development:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "has_unit_tests": True
            }
        }

        result = mycol.update_one(filter, update)

        print("Matched:", result.matched_count)
        print("Modified:", result.modified_count)
    
    ###############
    ##mongo code###
    ###############


    ###this is for checking that the connect
    data[f"{repo_name}"]=test_driven_development
    print(f"{repo_name} {data[f'{repo_name}']} ")
client.close()