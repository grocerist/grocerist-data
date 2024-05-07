import os
import json

from config import JSON_FOLDER

locations = ["nahiye", "quarter", "karye", "neighbourhoods", "address"]

for location in locations:
    with open(
        os.path.join(JSON_FOLDER, location + ".json"), "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
        for key, entry in data.items():
            for i in range(1, 5):
                if "upper_admin" + str(i) in entry:
                    unique_data = []
                    seen_values = set()

                    for item in entry["upper_admin" + str(i)]:
                        if item["value"] not in seen_values:
                            unique_data.append(item)
                            seen_values.add(item["value"])

                    entry["upper_admin" + str(i)] = unique_data
                    print(entry["upper_admin" + str(i)])

    with open(
        os.path.join(JSON_FOLDER, location + ".json"), "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
