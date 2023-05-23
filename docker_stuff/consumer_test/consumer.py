import pulsar
import json
from pprint import pprint
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
data={}
# Subscribe to a topic and subscription
consumer1 = client.subscribe('Repos2', subscription_name='DE-sub')
consumer2= client.subscribe('Commits2', subscription_name='DE-sub')
while True:
    msg1= consumer1.receive()
    repository=json.loads(msg1.data().decode('utf-8'))
    repo_name=repository['full_name']
    language=repository['language']
    msg2 = consumer2.receive()
    commits =json.loads(msg2.data().decode('utf-8'))
    num_commits=int(commits['Link'].split('&page=')[-1].split(';')[0].split('>')[0])
    data[f'{repo_name}']=[language,num_commits]
    print(data)
client.close()