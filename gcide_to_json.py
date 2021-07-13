#!/usr/bin/env python

import gcide_to_json_converter

print("Writing to output.json")

with open("output.json", "w") as out:
    out.write(gcide_to_json_converter.get_definitions_json())
