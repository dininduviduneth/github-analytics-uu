import requests
import json
from datetime import date, timedelta
import time

def get_limits(token):
    headers = {'Authorization': 'token ' + token}
    url=f"https://api.github.com/rate_limit"
    rate_limits = requests.get(url,headers=headers).json()

    remaining_resources = {
        "core_remaining": rate_limits["resources"]["core"]["remaining"],
        "search_remaining": rate_limits["resources"]["search"]["remaining"],
        "rate_remaining": rate_limits["rate"]["remaining"],
    }

    return remaining_resources

def generate_dates_array(start_date, end_date):
    # Calculate the total number of days
    total_days = (end_date - start_date).days + 1

    # Generate the array of dates
    dates_array = [start_date + timedelta(days=i) for i in range(total_days)]
    return dates_array

def index_nearest_reset(tokens):
    times_left = []
    for i in range(len(tokens)):
        headers = {'Authorization': 'token ' + tokens[i]}
        r = requests.get('https://api.github.com/rate_limit', headers=headers)
        reset = r.json()['resources']['core']['reset']
        times_left.append(reset - time.time())
    return times_left.index(min(times_left))
    
def out_of_tokens_handler(token):
    headers = {'Authorization': 'token ' + token}
    r = requests.get('https://api.github.com/rate_limit', headers=headers)
    if r.status_code == 200:
        info = r.json()
        reset = info['resources']['core']['reset']
        seconds_left = reset - time.time()
        if seconds_left > 0:
            print(f"Sleeping for {seconds_left} seconds")
            time.sleep(seconds_left)
        print("starting again")
        return True
    return False    