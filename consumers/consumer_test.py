import pulsar
import json
import requests
from pprint import pprint
token="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"
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://pulsar_container:6650')
data={}
# Subscribe to a topic and subscription
consumer1 = client.subscribe('repositories_test1', subscription_name='question3')
while True:
    msg1= consumer1.receive()
    repo_name=json.loads(msg1.data().decode('utf-8'))
    spec_repo_contents=requests.get(f"https://api.github.com/repos/{repo_name}/contents").json()# without token
    spec_repo_contents=requests.get(f"https://api.github.com/repos/{repo_name}/contents",headers=token).json()
    test_driven_development= False
    for i in spec_repo_contents:
        if "test" in i['name'].lower():
            print(f"uses test based development.")
            test_driven_development= True
            

   
    
    ###############
    ##mongo code###
    ###############


    ###this is for checking that the connect
    data[f"{repo_name}"]=test_driven_development
    print(f"{repo_name} {data[f'{repo_name}']} ")
client.close()