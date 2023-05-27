import pulsar
import requests
import json
import pymongo
from datetime import date, timedelta

from helpers import generate_dates_array

# Load the shared_data.json file
with open('shared_data.json', 'r') as json_file:
    # Load the JSON data
    shared_data = json.load(json_file)

token_count = len(shared_data["producer"]['tokens'])
token_counter = -1

#Creating the database
mongoclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
db = mongoclient[shared_data["mongodb"]["database"]]
collection = db[shared_data["mongodb"]["collection"]]

# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')
# Create a producer on the topic that consumer can subscribe to
producer_1 = client.create_producer(shared_data["pulsar"]["topic"])

# Generate dates array
# start_date = date(2022, 1, 1)
# end_date = date(2022, 12, 31)

# # Calculate the total number of days
# total_days = (end_date - start_date).days + 1

# # Generate the array of dates
# dates_array = [start_date + timedelta(days=i) for i in range(total_days)]
dates_array = generate_dates_array(date(2022, 1, 1), date(2022, 12, 31))
hours = shared_data["hours"]
output_file = "last_day_observed.txt"
with open(output_file, 'r') as file:
    last_day_observed = int(file.read())
    file.close()


for day in range(last_day_observed, 50):
    with open(output_file, 'w') as file:
        file.write(str(day))
        file.close()
    for hour in hours:
        if token_counter == token_count - 1:
            token_counter = 0
        else:
            token_counter += 1
        
        headers = {'Authorization': 'token ' + shared_data["producer"]['tokens'][token_counter]}
        for i in range(1):
            url=f"https://api.github.com/search/repositories?q=pushed:{dates_array[day]}T{hour}+archived:false&per_page=100&page={i+1}"
            repositories = requests.get(url,headers=headers).json()
            if 'message' in repositories:
                if repositories['message'] == 'Bad credentials':
                    print(repositories['message'] + " - Token: " + shared_data["producer"]['tokens'][token_counter])
                    token_counter+=1
                    if token_counter < token_count:
                        headers = {'Authorization': 'token ' + shared_data["producer"]['tokens'][token_counter]}
                        repositories=requests.get(url,headers=headers).json()
                    else:
                        print("We have run out of tokens!")
                        print("Last updated day: " + day)
                        break
            try:
                for item in repositories['items']:
                    if(item["language"] is not None):
                        filtered_item = {key: item[key] for key in ["full_name", "created_at", "pushed_at", "updated_at", "language"]}
                        filtered_item["commits"] = 0
                        filtered_item["has_unit_tests"] = False
                        filtered_item["has_cicd"] = False
                        filtered_item["updated_commits"] = False
                        filtered_item["updated_unit_tests"] = False
                        filtered_item["updated_cicd"] = False

                        if collection.find_one({"full_name": filtered_item["full_name"]}):
                            print("Repository already exists in the DB, moving to next")
                            continue
                        else:
                            db_response = collection.insert_one(filtered_item)
                            if db_response.acknowledged:
                                print("Repository " + filtered_item["full_name"] + " inserted successfully!")
                                producer_1.send(filtered_item["full_name"].encode('utf-8'))
                            else:
                                print("Insertion failed for " + filtered_item["full_name"])
            except:
                print("Repository doesn't have an items object!")
                continue

# Destroy pulsar
client.close()