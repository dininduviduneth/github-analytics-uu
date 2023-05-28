import pulsar
import json
import requests
from pprint import pprint
import pymongo
import time
from helpers import index_nearest_reset, out_of_tokens_handler, index_first_available_token
# Load the shared_data.json file
with open('shared_data.json', 'r') as json_file:
    # Load the JSON data
    shared_data = json.load(json_file)

token_count = len(shared_data["consumer_cicd"]['tokens'])
token_counter = 0
tokens = shared_data["consumer_cicd"]['tokens']

server_error_sleep = 300
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
    headers = {'Authorization': 'token ' + tokens[token_counter]}
    r=requests.get(f"https://api.github.com/repos/{repo_name}/actions/runs",headers=headers)
    info = r.json()
    if 'message' in info:
        if 'API' in info['message']:
            print(info['message'] + " - Token: " + tokens[token_counter])
            token_counter = index_first_available_token(tokens)
            if token_counter != -1:
                print("Moving to different token")
                continue
            else:
                print("We have run out of tokens!")
                print("Last updated repository: " + repo_name)
                token_counter = index_nearest_reset(tokens)
                if out_of_tokens_handler(token=tokens[token_counter]):
                    continue
                else:
                    print("Couldn't query API")
                    break
        elif info['message'] == "Not Found":
            print(f"Encountered deleted repository {repo_name}")
            consumer1.acknowledge(msg1)
            continue
        elif info['message'] == "Server Error":
            print(f"Encountered server error, sleeping for  {server_error_sleep} seconds")
            time.sleep(server_error_sleep)
            continue                
        else:
            print(info['message'] + " - Token: " + tokens[token_counter])
            break
    ci_cd = has_cicd(r.json())        
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


    else:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "updated_cicd": True
            }
        }
    db_response = collection.update_one(filter, update)
    print("Matched:" + str(db_response.matched_count) + ", Modified:" + str(db_response.modified_count) + " - " + repo_name)
        
    consumer1.acknowledge(msg1)
client.close()