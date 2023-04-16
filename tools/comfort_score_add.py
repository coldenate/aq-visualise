"""File to add comfort score to the dataset.json file"""
import json

# load the dataset.json file
with open("dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# iterate through each day in the data
for date, day_data in data.items():
    measurements = day_data.get("measurements", [])
    surveys = day_data.get("surveys", [])

    # calculate comfort score for each measurement
    for measurement in measurements:
        temperature = measurement.get("temperature")
        humidity = measurement.get("humidity")
        co2 = measurement.get("co2")
        tvoc = measurement.get("tvoc")

        # calculate the comfort score
        comfort_score = (
            100
            - (0.5 * abs(temperature - 22))
            - (0.25 * abs(humidity - 40))
            - (0.05 * abs(co2 - 800))
            - (0.1 * abs(tvoc - 50))
        )
        # add the comfort score to the measurement entry
        measurement["comfort_score"] = comfort_score

    # calculate performance score for each survey
    for survey in surveys:
        reaction_time_ms = survey.get("reaction_time_ms")
        visual_mem_level = survey.get("visual_mem_level")
        aiming_reaction_ms = survey.get("aiming_reaction_ms")
        chimp_score = survey.get("chimp_score")

        # normalize each factor to a value between 0 and 1
        reaction_time_norm = max(0, 1 - (reaction_time_ms / 1000))
        visual_mem_norm = visual_mem_level / 11
        aiming_reaction_norm = max(0, 1 - (aiming_reaction_ms / 1000))
        chimp_score_norm = min(1, chimp_score / 10)

        performance_score = (
            (
                reaction_time_norm
                + visual_mem_norm
                + aiming_reaction_norm
                + chimp_score_norm
            )
            / 4
            * 100
        )

        # add the performance score to the survey entry
        survey["performance_score"] = performance_score


# save the updated data to a new file
with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
