"Group by Time Block"

import json
from datetime import datetime, timedelta


# get all the unique dates from the measurements.json file, and put them in a list
# create a dictionary with elements for each date, and each element has a element containing all the measurements for that date and an element containing all the surveys for that date. count the number of measurements that aren't given a date :( poor guys

with open("measurements.json") as f:
    measurements = json.load(f)

days = set()

for measurement in measurements:
    # after converting from iso to datetime, add the  This will remove duplicates days.
    time = datetime.fromisoformat(measurement["timestamp"])
    date_string = time.strftime("%Y-%m-%d")

    days.add(date_string)

data = {}

for day in days:
    data[day] = {"measurements": [], "surveys": []}

for measurement in measurements:
    time = datetime.fromisoformat(measurement["timestamp"])
    date_string = time.strftime("%Y-%m-%d")
    # if the "room_location" key is present, remove it
    try:
        measurement.pop("room_location")
    except KeyError:
        pass
    data[date_string]["measurements"].append(measurement)

with open("surveys.json") as f:
    surveys = json.load(f)

surveys_without_timestamp = []

for survey in surveys:
    # if the survey doesn't have a timestamp, skip it, and add it to the list of surveys without a timestamp
    if "timestamp" not in survey:
        surveys_without_timestamp.append(survey)
        continue
    time = datetime.fromisoformat(survey["timestamp"])
    date_string = time.strftime("%Y-%m-%d")
    data[date_string]["surveys"].append(survey)

# now we have a dictionary with all the measurements and surveys for each day

print("obfuscating emails...")

# obfuscate the emails by replacing them with SHA256 Hash of the email address. make a dictionary with the email as the key and the hash as the value for just me. print it to the console so I can copy it and paste it into the code.

import hashlib

email_hash_dict = {}

for day, day_data in data.items():
    for survey in day_data["surveys"]:
        email = survey["email_address"]
        if email not in email_hash_dict and email != None:
            new_string = hashlib.sha256(email.encode()).hexdigest()
            email_hash_dict[email] = new_string
        if email != None:
            new_string = hashlib.sha256(email.encode()).hexdigest()
            survey["email_address"] = new_string


import pprint

pprint.pprint(email_hash_dict)

# sort days by date
from collections import OrderedDict

data = OrderedDict(
    sorted(data.items(), key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"))
)


print("done!")
print("exporting into data.json...")

# export the data into a json file

with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
