import os
import json

from config import JSON_FOLDER

with open(os.path.join(JSON_FOLDER, "documents.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

new_documents = {}
for key, value in data.items():
    good_cat_set = set()
    new_value = value
    value["good_cat"] = []
    for x in value["goods"]:
        for y in x["has_category"]:
            good_cat_key = "__".join([f"{value}" for key, value in y.items()])
            good_cat_set.add(good_cat_key)
    for x in good_cat_set:
        good_cat_id, good_cat_name, good_cat_color = x.split("__")
        item = {
            "id": good_cat_id,
            "name": good_cat_name,
            "color": good_cat_color,
            "grocerist_id": f"good_cat__{good_cat_id}",
        }
        new_value["good_cat"].append(item)
    new_documents[key] = new_value

with open(os.path.join(JSON_FOLDER, "documents.json"), "w", encoding="utf-8") as f:
    json.dump(new_documents, f, ensure_ascii=False, indent=4)
