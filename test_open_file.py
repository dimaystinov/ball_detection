import json

hsv_filter_dict = {
    "low":[0, 0, 0],
    "high":[255, 255, 255],
}

hsv_filter_json = json.dumps(hsv_filter_dict)
print(type(hsv_filter_json))


with open("hsv_filter.json", "w") as f:
    f.write(hsv_filter_json)

with open("hsv_filter.json", "r") as f:
    hsv_filter_dict = json.loads(f.read())
    print(type(hsv_filter_dict))
    print(hsv_filter_dict["low"])
    print(hsv_filter_dict["high"])


