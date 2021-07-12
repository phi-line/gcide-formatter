#!/usr/bin/env python

import gcide_to_json_converter as json

print("Writing to output.json")

with open("output.json", "w") as out:
    out.write(json.get_json())
