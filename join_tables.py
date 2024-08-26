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


def add_lat_long_to_goods(goods_data, docs_data):
    for key, value in goods_data.items():
        if value["documents"]:
            for doc in value["documents"]:
                doc["lat"] = docs_data[str(doc["id"])].get("lat")
                doc["long"] = docs_data[str(doc["id"])].get("long")
                doc["iso_date"] = docs_data[str(doc["id"])].get("creation_date_ISO")


# Add categories to documents and vice versa
def join_documents_and_categories(docs_data, cat_data):
    new_documents = {}
    cat_dict = {}
    for key, value in docs_data.items():
        good_cat_set = set()
        doc_item = {k: value[k] for k in ["id", "shelfmark", "grocerist_id"]}
        new_value = value
        value["good_cat"] = []

        for good in value["goods"]:
            for cat in good["has_category"]:
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


# Enrich documents with data from goods and persons
join_tables(documents_data, goods_data, "goods")
join_tables(documents_data, persons_data, "main_person")

# Add lat, long and date from documents
add_lat_long_to_goods(goods_data, documents_data)

# Process documents and categories
new_documents, new_categories = join_documents_and_categories(
    documents_data, categories_data
)

# Save updated documents and categories data
save_json(new_documents, os.path.join(JSON_FOLDER, "documents.json"))
save_json(new_categories, os.path.join(JSON_FOLDER, "categories.json"))
save_json(goods_data, os.path.join(JSON_FOLDER, "goods.json"))
