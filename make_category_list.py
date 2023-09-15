import os
import json
from collections import defaultdict

from config import JSON_FOLDER

with open(os.path.join(JSON_FOLDER, "goods.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

goods = defaultdict(list)
for key, value in data.items():
    for x in value["has_category"]:
        cat_id = x["id"]
        cat_value = x["value"]
        cat_color = x["color"]
        goods[f"{cat_id}__{cat_value}__{cat_color}"].append(
            {
                "grocerist_id": value["grocerist_id"],
                "name": f'{value["name"]}__{value["id"]}',
                "documents": value["documents"],
            }
        )

category_list = []
for key, value in goods.items():
    item = {}
    item["id"], item["name"], item["color"] = key.split("__")
    item["goods"] = []
    item["documents"] = []
    goods_set = set()
    document_set = set()
    for x in value:
        goods_set.add(x["name"])
        for y in x["documents"]:
            doc_str = f'{y["id"]}##{y["value"]}'
            document_set.add(doc_str)
    for x in goods_set:
        good_name, good_id = x.split("__")
        item["goods"].append(
            {"id": good_id, "name": good_name, "grocerist_id": f"goods__{good_id}"}
        )
    for x in document_set:
        doc_id, doc_name = x.split("##")
        item["documents"].append(
            {"id": doc_id, "name": doc_name, "grocerist_id": f"document__{doc_id}"}
        )
        item["doc_count"] = len(item["documents"])
        item["good_count"] = len(item["goods"])
    category_list.append(item)


with open(os.path.join(JSON_FOLDER, "categories.json"), "w") as f:
    json.dump(category_list, f, ensure_ascii=False, indent=2)
