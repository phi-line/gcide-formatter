#!/usr/bin/env python

import json
import os
import re

from gcide_parser import xml_to_objects


def __json_handler(obj):
    return obj.__dict__


def get_definitions_json():
    # get definitions
    print("Getting definitions")

    definitions = xml_to_objects()

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
