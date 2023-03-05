# run through the json of measurements.json and convert the timestamp to a datetime object that goes from GMT to CST

import json
from datetime import datetime, timedelta

with open("measurements.json") as f:
    measurements = json.load(f)

for measurement in measurements:
    # check if the timestamp field exists and is already formatted
    if "timestamp" in measurement and isinstance(measurement["timestamp"], str):
        continue
    timestamp = measurement["timestamp"]["$date"]["$numberLong"]
    dt = datetime.utcfromtimestamp(int(timestamp) / 1000) - timedelta(hours=6)
    measurement["timestamp"] = dt.isoformat()


with open("measurements.json", "w") as f:
    json.dump(measurements, f)

with open("surveys.json") as f:
    surveys = json.load(f)

for survey in surveys:
    if "timestamp" in survey:
        timestamp = survey["timestamp"]["$date"]["$numberLong"]
        dt = datetime.utcfromtimestamp(int(timestamp) / 1000) - timedelta(hours=6)
        survey["timestamp"] = dt.isoformat()

with open("surveys.json", "w") as f:
    json.dump(surveys, f)
