import json
import os


def merge_entries(json_file, merge_into, entries_to_merge):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # first find the entry to merge into
    for value in data.values():
        if value["name"] == merge_into:
            merged_entry = value
            break
    # second find the entries to merge
    for value in data.values():
        if value["name"] in entries_to_merge:
            merged_entry["documents"].extend(value["documents"])
            # merged_entry["persons"].extend(value["persons"])

    # Remove the old entries
    data = {
        key: value
        for key, value in data.items()
        if value["name"] not in entries_to_merge
    }

    # Add the merged entry
    data[str(merged_entry["id"])] = merged_entry

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def replace_entries(json_file, entries_to_replace):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    for value in data.values():

        # case for documents.json (where there should only ever be one district entry)
        if (
            "district" in value
            and value["district"]
            and value["district"][0]["value"] in entries_to_replace
        ):
            value["district"] = [{"id": 4, "value": "Galata"}]
        # case for the location json files, where there can be multiple entries
        elif "upper_admin1" in value and value["upper_admin1"]:
            for district in value["upper_admin1"]:
                if district["value"] in entries_to_replace:
                    print("replacing", district["value"])
                    district["ids"] = {
                        "database_table_1488": 20,
                        "database_table_1492": 4,
                    }
                    district["value"] = "Galata"

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


merge_into = "Galata"
entries_to_merge = ["Galata Harici", "Galata Dahili"]
districts_file = os.path.join("json_dumps", "districts.json")
merge_entries(districts_file, merge_into, entries_to_merge)


files_linked_to_districts = [
    "documents.json",
    "karye.json",
    "nahiye.json",
    "address.json",
    "neighbourhoods.json",
    "quarter.json",
]
for file in files_linked_to_districts:
    replace_entries(os.path.join("json_dumps", file), entries_to_merge)
