import pulsar
import requests
import json
from pprint import pprint
from requests.structures import CaseInsensitiveDict
import pymongo
token="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" 

#Creating the database
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
mydb = myclient["mydatabase_test"]
mycol = mydb["repositories_test"]
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
# Create a producer on the topic that consumer can subscribe to
producer_1 = client.create_producer('repositories_test987')
data={}
for i in range(1,10):
    url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+created:<2022-05-10+archived:false&per_page=100&page={i}"
    repositories=requests.get(url,headers=token).json()
    for i in range(100):
        repo_name=repositories['items'][i]['full_name']
        language=repositories['items'][i]['language']
        mydict = {
        "full_name": repo_name,
        "language": language,
        "commits": 0,
        "has_unit_tests": False,
        "has_cicd": False
        }
        x = mycol.insert_one(mydict)
        print(x)
        producer_1.send(repo_name.encode('utf-8'))
        print(repo_name)

# Destroy pulsar
client.close()






example_id = 5


