#!/usr/bin/env python

import re
import os
from bs4 import BeautifulSoup

"""
Parses gcide directory and returns python objects
"""


class Definition:
    def __init__(self, word, text, source, pos):
        self.word = word
        self.text = text
        self.source = source
        self.pos = pos


def __get_cide_files():
    files = os.listdir("xml_files")
    files_sorted = sorted(files)
    files_filtered = filter(lambda name: re.match("^gcide.\\w.xml$", name), files_sorted)
    files_list = list(files_filtered)
    return files_list


def get_definitions():
    definition_objects = []

    for file in __get_cide_files():
        xml = open(f"xml_files/{file}", "r")
        xml = xml.read()
        xml = "<root>" + xml + "</root>"
        parser = BeautifulSoup(markup=xml, features="lxml-xml")
        p_list = parser.find_all("p")
        p_groups = []
        for p in p_list:
            if p.find("ent") is not None:
                p_group = [p]
                p_groups.append(p_group)
            elif p_groups.__len__() < 1:
                pass
            else:
                p_groups[p_groups.__len__() - 1].append(p)

        for p_group in p_groups:
            entry = p_group[0].find("ent")
            for p in p_group:
                definitions = p.find_all("def")  # TODO could be preceded by <sn>
                part_of_speech = p.find_all("pos", recursive=False)  # TODO could be preceded by (n)
                sources = p.find_all("source")
                # TODO <pr> pronunciation
                # TODO other <tags>

                # TODO don't get first source and first POS, pass list instead
                part_of_speech = part_of_speech[0].text if part_of_speech.__len__() >= 1 else None
                sources = sources[0].text if sources.__len__() >= 1 else None

                for definition in definitions:
                    print(f"{definition_objects.__len__()} ({entry.text})")
                    definition_objects.append(
                        Definition(entry.text, definition.text, sources, part_of_speech)
                    )

    return definition_objects

