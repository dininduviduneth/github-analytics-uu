import requests
import json
from datetime import date, timedelta

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