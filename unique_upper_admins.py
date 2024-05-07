import os
import json

from config import JSON_FOLDER

locations = ["nahiye", "quarter", "karye", "neighbourhoods", "address"]

for location in locations:
    with open(
        os.path.join(JSON_FOLDER, location + ".json"), "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
        for key, value in data.items():
            for i in range(1, 5):
                if "upper_admin" + str(i) in value:
                    # Use a set to store unique JSON objects
                    unique_data = set(
                        json.dumps(item, sort_keys=True)
                        for item in value["upper_admin" + str(i)]
                    )
                    # Convert each JSON object back to a dictionary
                    unique_data = [json.loads(item) for item in unique_data]
                    # Replace the value with unique_data
                    value["upper_admin" + str(i)] = unique_data

    with open(
        os.path.join(JSON_FOLDER, location + ".json"), "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
