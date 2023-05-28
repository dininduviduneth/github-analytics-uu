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

token_count = len(shared_data["consumer_commits"]['tokens'])
token_counter = 0
tokens = shared_data["consumer_commits"]['tokens']



mongoclient = pymongo.MongoClient("mongodb://root:example@192.168.2.51:27017/")
db = mongoclient[shared_data["mongodb"]["database"]]
collection = db[shared_data["mongodb"]["collection"]]

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.51:6650')

# Subscribe to a topic and subscription
consumer1 = client.subscribe(shared_data["pulsar"]["topic"], subscription_name=shared_data["consumer_commits"]["subscription_name"])

while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    # commits=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1") # without token
    headers = {'Authorization': 'token ' + tokens[token_counter]}
    r=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1",headers=headers)
    info = r.json()
    if 'message' in info:
        if 'API' in info['message']:
            print(info['message'] + " - Token: " + shared_data["consumer_commits"]['tokens'][token_counter])
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
        else:
            print(info['message'] + " - Token: " + shared_data["consumer_commits"]['tokens'][token_counter])
            break


           
    commits = r.headers                
    num_commits=int(commits['Link'].split('&page=')[-1].split(';')[0].split('>')[0])

    filter = {
        "full_name": repo_name
    }

    update = {
        "$set": {
            "commits": num_commits,
            "updated_commits": True
        }
    }

    db_response = collection.update_one(filter, update)

    print("Matched:", str(db_response.matched_count) + ", Modified:" + str(db_response.modified_count) + " - " + repo_name)
    consumer1.acknowledge(msg1)

client.close()