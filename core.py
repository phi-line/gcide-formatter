import re
import os
from bs4 import BeautifulSoup
import lxml
import click


class Definition:
    def __init__(self, word, text, source, pos):
        self.word = word
        self.text = text
        self.source = source
        self.pos = pos


def xml_to_objects(gcide_dir):
    definition_objects = []

    files = os.listdir(gcide_dir)
    files = sorted(files)
    files = filter(lambda name: re.match("^gcide.\\w.xml$", name), files)
    files = list(files)

    with click.progressbar(files, length=len(files), label="Parsing files") as files:
        for file in files:
            xml = open(f"{gcide_dir}/{file}", "r")
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
                entry = entry.text
                for p in p_group:
                    definitions = p.find_all("def")
                    definitions = map(lambda d: d.text, definitions)
                    definitions = list(definitions)

                    part_of_speech = p.find("pos", recursive=False)
                    part_of_speech = part_of_speech.text if part_of_speech is not None else ""

                    sources = p.find_all("source")
                    sources = map(lambda s: s.text, sources)
                    sources = list(sources)
                    sources = " ".join(sources)

                    for definition in definitions:
                        definition_objects.append(
                            Definition(entry, definition,
                                       sources, part_of_speech)
                        )

    return definition_objects
