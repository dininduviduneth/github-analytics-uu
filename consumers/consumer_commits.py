import pulsar
import json
import requests
from pprint import pprint
token="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"
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
data={}
# Subscribe to a topic and subscription
consumer1 = client.subscribe('repositories_test1', subscription_name='question2')
while True:
    msg1= consumer1.receive()
    repo_name=json.loads(msg1.data().decode('utf-8'))
    commits=requests.get(f"https://api.github.com/repos/{repo_name}/commits?per_page=1&page=1",headers=token)
    num_commits=int(commits['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
    
    ###############
    ##mongo code###
    ###############

    
    ###this is for checking that the connect
    data[f'{repo_name}']=num_commits
    print(data)
client.close()