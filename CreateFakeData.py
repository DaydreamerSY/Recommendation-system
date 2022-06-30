import random

FIELDS = {
    "id": {"type": "id", "MIN": 00, "MAX": 9999},
    "region": {
        "type": "list",
        "items": [
            "Đà Lạt",
            "Bảo Lộc",
            "Bảo Lâm",
            "Cát Tiên",
            "Di Linh",
            "Đạ Huoai",
            "Đạ Tẻh",
            "Đam Rông",
            "Đơn Dương",
            "Đức Trọng",
            "Lạc Dương",
            "Lâm Hà",
        ],
    },
    "area_by_m2": {"type": "int", "MIN": 50, "MAX": 250},
    "width_of_facade": {"type": "int", "MIN": 5, "MAX": 15},
    "width_of_road": {"type": "int", "MIN": 5, "MAX": 15},
    "is_legal": {"type": "int", "MIN": 0, "MAX": 1},
    "price": {"type": "float", "MIN": 0.8, "MAX": 15},
}
NUMBER_OF_RECORDS = 5000

id = 0
with open("fake-data.csv", "w", encoding="utf-8") as w:
    w.write(",".join(FIELDS))
    w.write("\n")
    for i in range(NUMBER_OF_RECORDS):
        for field in FIELDS:
            if field == "id":
                w.write(f"{id:05d}")
                continue
            if not FIELDS[field]["type"] == "list":
                if FIELDS[field]["type"] == "int":
                    result = random.randint(FIELDS[field]["MIN"], FIELDS[field]["MAX"])
                    w.write(f",{result}")
                if FIELDS[field]["type"] == "float":
                    result = round(
                        random.uniform(FIELDS[field]["MIN"], FIELDS[field]["MAX"]), 2
                    )
                    w.write(f",{result}")
            else:
                result = random.choice(FIELDS[field]["items"])
                w.write(f",{result}")
        w.write("\n")
        id += 1
    w.close()
