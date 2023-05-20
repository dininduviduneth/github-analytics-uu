import pulsar
import requests
import json
from pprint import pprint
from requests.structures import CaseInsensitiveDict
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
# Create a producer on the topic that consumer can subscribe to
producer_1 = client.create_producer('repositories_test')
data={}
url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+created:<2022-05-10+archived:false&per_page=100"
repositories = dict(requests.get(url).json())
for i in range(100):
    repo_name=repositories['items'][i]['full_name']
    # json.dumps makes the object to string so we can encode it and send it 
    producer_1.send(repo_name.encode('utf-8'))

# Destroy pulsar
client.close()