import json


def __json_handler(obj):
    return obj.__dict__


def definitions_json(definitions):
    # Format json string based on entryObjects
    print("Formatting object list to json")

    json_str = json.dumps(definitions, default=__json_handler)

    # Check json validity
    print("Validating json")

    try:
        json.loads(json_str)
    except ValueError:
        print("Error: Json is invalid.")
        exit(-1)

    # Return json
    print("Done, returning")
    return json_str
