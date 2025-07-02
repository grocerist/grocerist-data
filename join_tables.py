import json
import os
import copy

from config import JSON_FOLDER


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def join_tables(source_data, seed_data, key_name):
    for key, value in source_data.items():
        old_values = value[key_name]
        # Create deep copies of the items to avoid modifying the original data
        new_values = [copy.deepcopy(seed_data[f"{x['id']}"]) for x in old_values]
        # Remove documents from the deep-copied items
        for item in new_values:
            item.pop("documents", "")
        value[key_name] = new_values


def add_lat_long(source_data, docs_data):
    for key, value in source_data.items():
        if value["documents"]:
            for doc in value["documents"]:
                doc["lat"] = docs_data[str(doc["id"])].get("lat")
                doc["long"] = docs_data[str(doc["id"])].get("long")
                doc["iso_date"] = docs_data[str(doc["id"])].get("creation_date_ISO")
                doc["century"] = docs_data[str(doc["id"])].get("century")


def add_locations(source_data, documents_data):
    locations = ["district", "neighbourhood", "karye", "nahiye", "quarter", "address"]
    district_data = load_json(os.path.join(JSON_FOLDER, "districts.json"))
    neighbourhood_data = load_json(os.path.join(JSON_FOLDER, "neighbourhoods.json"))
    karye_data = load_json(os.path.join(JSON_FOLDER, "karye.json"))
    nahiye_data = load_json(os.path.join(JSON_FOLDER, "nahiye.json"))
    quarter_data = load_json(os.path.join(JSON_FOLDER, "quarter.json"))
    address_data = load_json(os.path.join(JSON_FOLDER, "address.json"))

    # Initialize "persons" field for each location
    for location_data in [
        district_data,
        neighbourhood_data,
        karye_data,
        nahiye_data,
        quarter_data,
        address_data,
    ]:
        for location in location_data.values():
            location.setdefault("persons", [])
            # add century to each document in the location
            for doc in location["documents"]:
                doc["century"] = documents_data[str(doc["id"])].get("century")

    # add district, neighbourhood, karye, nahiye, quarter and address to each person entry based on the documents they are associated with
    for person in source_data.values():
        for location_type in locations:
            person[location_type] = []
            locations_set = set()
            for doc in person["documents"]:
                doc_data = documents_data[str(doc["id"])]
                if doc_data[location_type]:
                    for location in doc_data[location_type]:
                        if location["value"] not in locations_set:
                            person[location_type].append(location)
                            locations_set.add(location["value"])
            # open the json file for the location type and add the poersons to the location
            for location in person[location_type]:
                location_data = locals()[f"{location_type}_data"]
                location_data[str(location["id"])]["persons"].append(person)
    save_json(district_data, os.path.join(JSON_FOLDER, "districts.json"))
    save_json(neighbourhood_data, os.path.join(JSON_FOLDER, "neighbourhoods.json"))
    save_json(karye_data, os.path.join(JSON_FOLDER, "karye.json"))
    save_json(nahiye_data, os.path.join(JSON_FOLDER, "nahiye.json"))
    save_json(quarter_data, os.path.join(JSON_FOLDER, "quarter.json"))
    save_json(address_data, os.path.join(JSON_FOLDER, "address.json"))


# Add categories to documents and vice versa
def join_documents_and_categories(docs_data, cat_data):
    new_documents = {}
    cat_dict = {}
    for key, value in docs_data.items():
        good_cat_set = set()
        doc_item = {k: value[k] for k in ["id", "shelfmark", "grocerist_id","century"]}
        new_value = value
        value["good_cat"] = []

        for good in value["goods"]:
            for cat in good["has_category"]:
                # Remove the "order" key if it exists
                cat.pop("order", None)
                good_cat_key = "__".join([f"{v}" for k, v in cat.items()])
                good_cat_set.add(good_cat_key)

        for cat in good_cat_set:
            if cat not in cat_dict:
                cat_dict[cat] = []
            cat_dict[cat].append(doc_item)
            good_cat_id, good_cat_name = cat.split("__")
            item = {
                "id": good_cat_id,
                "name": good_cat_name,
                "grocerist_id": f"good_cat__{good_cat_id}",
            }
            new_value["good_cat"].append(item)
        new_documents[key] = new_value

    new_categories = cat_data
    for key, value in cat_dict.items():
        cat_id, cat_name = key.split("__")
        new_value = cat_data[cat_id]
        new_value["documents"] = value
        new_categories[cat_id] = new_value

    return new_documents, new_categories


# Load JSON files
goods_data = load_json(os.path.join(JSON_FOLDER, "goods.json"))
persons_data = load_json(os.path.join(JSON_FOLDER, "persons.json"))
documents_data = load_json(os.path.join(JSON_FOLDER, "documents.json"))
categories_data = load_json(os.path.join(JSON_FOLDER, "categories.json"))
utensils_data = load_json(os.path.join(JSON_FOLDER, "utensils.json"))
price_data = load_json(os.path.join(JSON_FOLDER, "price_per_document.json"))

# Enrich documents with data from goods and persons, enrich documents and goods with price data
join_tables(documents_data, goods_data, "goods")
join_tables(documents_data, persons_data, "main_person")
join_tables(documents_data, price_data, "price_per_document")
join_tables(goods_data, price_data, "price_per_document")

# Add lat, long and date from documents
add_lat_long(goods_data, documents_data)
add_lat_long(utensils_data, documents_data)
add_lat_long(persons_data, documents_data)


add_locations(persons_data, documents_data)

# Process documents and categories
new_documents, new_categories = join_documents_and_categories(
    documents_data, categories_data
)

# Save updated documents and categories data
save_json(new_documents, os.path.join(JSON_FOLDER, "documents.json"))
save_json(new_categories, os.path.join(JSON_FOLDER, "categories.json"))
save_json(goods_data, os.path.join(JSON_FOLDER, "goods.json"))
save_json(utensils_data, os.path.join(JSON_FOLDER, "utensils.json"))
save_json(persons_data, os.path.join(JSON_FOLDER, "persons.json"))
