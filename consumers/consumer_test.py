import pulsar
import json
import requests
from pprint import pprint
import pymongo
from helpers import index_nearest_reset, out_of_tokens_handler

# Load the shared_data.json file
with open('shared_data.json', 'r') as json_file:
    # Load the JSON data
    shared_data = json.load(json_file)

token_count = len(shared_data["consumer_test"]['tokens'])
token_counter = 0
tokens = shared_data["consumer_test"]['tokens']
# Select the first token in the list
headers = {'Authorization': 'token ' + shared_data["consumer_test"]['tokens'][token_counter]}

mongoclient = pymongo.MongoClient("mongodb://root:example@192.168.2.51:27017/")
db = mongoclient[shared_data["mongodb"]["database"]]
collection = db[shared_data["mongodb"]["collection"]]

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://192.168.2.51:6650')

# Subscribe to a topic and subscription
consumer1 = client.subscribe(shared_data["pulsar"]["topic"], subscription_name=shared_data["consumer_test"]["subscription_name"])

def has_tests(spec_repo_contents):
    for i in spec_repo_contents:
        if "test" in i['name'].lower():
            print("UNIT TESTS : TRUE for " + repo_name)
            return True
        else:
            print("UNIT TESTS : FALSE for " + repo_name)
            return False

while True:
    msg1= consumer1.receive()
    repo_name=msg1.data().decode('utf-8')
    headers = {'Authorization': 'token ' + tokens[token_counter]}
    r=requests.get(f"https://api.github.com/repos/{repo_name}/contents",headers=headers)
    info = r.json()
    if 'message' in info:
        if 'API' in info['message']:
            print(info['message'] + " - Token: " + tokens[token_counter])
            token_counter+=1
            if token_counter < token_count:
                print("Moving to next token")
                continue
            else:
                print("We have run out of tokens!")
                print("Last updated repository: " + repo_name)
                token_counter = index_nearest_reset(tokens)
                if out_of_tokens_handler(token=tokens[token_counter]):
                    headers = {'Authorization': 'token ' + tokens[token_counter]}
                    r=requests.get(f"https://api.github.com/repos/{repo_name}/contents",headers=headers)
                else:
                    print("Couldn't query API")
                    break
        else:
            print(info['message'] + " - Token: " + tokens[token_counter])
            break

    spec_repo_contents = r.json()
    if has_tests(spec_repo_contents):
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "has_unit_tests": True,
                "updated_unit_tests": True
            }
        }

        db_response = collection.update_one(filter, update)
        print("Matched:" + str(db_response.matched_count) + ", Modified:" + str(db_response.modified_count) + " - " + repo_name)
    else:
        filter = {
            "full_name": repo_name
        }

        update = {
            "$set": {
                "updated_unit_tests": True
            }
        }
        db_response = collection.update_one(filter, update)
        print("Matched:" + str(db_response.matched_count) + ", Modified:" + str(db_response.modified_count) + " - " + repo_name)
    consumer1.acknowledge(msg1)

client.close()