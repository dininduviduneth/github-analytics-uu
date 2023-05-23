import pulsar
import requests
import json
from pprint import pprint
from requests.structures import CaseInsensitiveDict
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
# Create a producer on the topic that consumer can subscribe to
producer_1 = client.create_producer('Repos2')
producer_2 = client.create_producer('Commits2')
# producer_3 = client.create_producer('Ci_cd')
# producer_4 = client.create_producer('Test_dev')
data={}
url=f"https://api.github.com/search/repositories?q=created:>2022-05-01+created:<2022-05-10+archived:false&per_page=100"
repositories = dict(requests.get(url).json())
# json.dumps makes the object to string so we can encode it and send it 
producer_1.send((json.dumps(repositories['items'][0])).encode('utf-8'))
# for i in range(5):
#     repo_name=repositories['items'][i]['full_name']
repo_name=repositories['items'][0]['full_name']

repo_comits=dict(requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1").headers)
producer_2.send((json.dumps(repo_comits)).encode('utf-8'))

#These are to check that they are the same 
language=repositories['items'][0]['language']
commits=int(repo_comits['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
data[f'{repo_name}']=[language,commits]
pprint(data)
# Destroy pulsar
client.close()