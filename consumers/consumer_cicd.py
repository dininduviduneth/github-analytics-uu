import pulsar
import json
import requests
from pprint import pprint
import pymongo

# Load the shared_data.json file
with open('shared_data.json', 'r') as json_file:
    # Load the JSON data
    shared_data = json.load(json_file)

token_count = len(shared_data["consumer_cicd"]['tokens'])
token_counter = 0

# Select the first token in the list
headers = {'Authorization': 'token ' + shared_data["consumer_cicd"]['tokens'][token_counter]}

mongoclient = pymongo.MongoClient("mongodb://root:example@192.168.2.51:27017/")
db = mongoclient[shared_data["mongodb"]["database"]]
collection = db[shared_data["mongodb"]["collection"]]

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.51:6650')

# Subscribe to a topic and subscription
consumer1 = client.subscribe(shared_data["pulsar"]["topic"], subscription_name=shared_data["consumer_cicd"]["subscription_name"])

def has_cicd(spec_repo):
    if spec_repo['total_count'] > 0:
        print("CICD : TRUE for " + repo_name)
        return True
    else:
        print("CICD : FALSE for " + repo_name)
        return False

while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    #check if there exists runs if it return an empy json it means we dont have a github workflow which means no CICD
    #spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs").json() #without token 
    spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=headers).json()
    if 'total_count' in spec_repo:
        ci_cd = has_cicd(spec_repo)
    else:
        if spec_repo['message'] == 'Bad credentials':
            print(spec_repo['message'] + " - Token: " + shared_data["consumer_cicd"]['tokens'][token_counter])
            token_counter+=1
            if token_counter < token_count:
                headers = {'Authorization': 'token ' + shared_data["consumer_cicd"]['tokens'][token_counter]}
                spec_repo=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=headers).json()
                ci_cd = has_cicd(spec_repo)
            else:
                print("We have run out of tokens")
                print("Last updated repo: " + repo_name)
                break
            
    if ci_cd:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "has_cicd": True,
                "updated_cicd": True
            }
        }

        result = collection.update_one(filter, update)

        print("Matched:", result.matched_count)
        print("Modified:", result.modified_count)
    else:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "updated_cicd": True
            }
        }
        
client.close()