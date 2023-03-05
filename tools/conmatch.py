import json

with open("surveys.json") as f:
    surveys = json.load(f)

# Create a set of survey values as tuples, ignoring id and timestamp
survey_values_set = set()
for survey in surveys:
    survey_values = tuple(
        (k, v) for k, v in survey.items() if k not in ["_id", "timestamp"]
    )
    survey_values_set.add(survey_values)

# Filter out surveys with duplicate values
non_duplicate_surveys = []
for survey in surveys:
    survey_values = tuple(
        (k, v) for k, v in survey.items() if k not in ["_id", "timestamp"]
    )
    if survey_values in survey_values_set:
        non_duplicate_surveys.append(survey)
        survey_values_set.remove(survey_values)

with open("surveys.json", "w") as f:
    json.dump(non_duplicate_surveys, f)
