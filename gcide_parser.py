#!/usr/bin/env python

import re
import os
from bs4 import BeautifulSoup

tags = [
    ("<Cced/", "Ç"),
    ("<uum/", "ü"),
    ("<eacute/", "é"),
    ("<acir/", "â"),
    ("<aum/", "ä"),
    ("<agrave/", "à"),
    ("<aring/", "å"),
    ("<cced/", "ç"),
    ("<ecir/", "ê"),
    ("<eum/", "ë"),
    ("<egrave/", "è"),
    ("<ium/", "ï"),
    ("<icir/", "î"),
    ("<igrave/", "ì"),
    ("<Aum/", "Ä"),
    ("<Eacute/", "É"),
    ("<ae/", "æ"),
    ("<AE/", "Æ"),
    ("<ocir/", "ô"),
    ("<oum/", "ö"),
    ("<ograve/", "ò"),
    ("<ucir/", "û"),
    ("<ugrave/", "ù"),
    ("<yum/", "ÿ"),
    ("<Oum/", "Ö"),
    ("<Uum/", "Ü"),
    ("<pound/", "£"),
    ("<aacute/", "á"),
    ("<iacute/", "í"),
    ("<oacute/", "ó"),
    ("<uacute/", "ú"),
    ("<ntil/", "ñ"),
    ("<Ntil/", "Ñ"),
    ("<frac23/", "⅔"),
    ("<frac13/", "⅓"),
    ("<sec/", "˝"),
    ("<frac12/", "½"),
    ("<frac14/", "¼"),
    ("<?/", "?"),
    ("<hand/", "☞"),
    ("<bprime/", "˝"),
    ("<prime/", "´"),
    ("<rdquo/", "”"),
    ("<sect/", "§"),
    ("<ldquo/", "“"),
    ("<amac/", "ā"),
    ("<lsquo/", "‘"),
    ("<nsm/", "ṉ"),
    ("<sharp/", "♯"),
    ("<flat/", "♭"),
    ("<th/", "ð"),
    ("<imac/", "ī"),
    ("<emac/", "ē"),
    ("<dsdot/", "ḍ"),
    ("<nsdot/", "ṇ"),
    ("<tsdot/", "ṭ"),
    ("<ecr/", "ĕ"),
    ("<icr/", "ĭ"),
    ("<ocr/", "ŏ"),
    ("-", "‐"),
    ("--", "—"),
    ("<OE/", "Œ"),
    ("<oe/", "œ"),
    ("<omac/", "ō"),
    ("<umac/", "ū"),
    ("<ocar/", "ǒ"),
    ("<aemac/", "ǣ"),
    ("<oemac/", "ō"),
    ("<ucr/", "ŭ"),
    ("<acr/", "ă"),
    ("<cre/", "˘"),
    ("<ymac/", "ȳ"),
    ("<asl/", "a"),
    ("<esl/", "e"),
    ("<isl/", "i"),
    ("<osl/", "o"),
    ("<usl/", "u"),
    ("<adot/", "ȧ"),
    ("<th/", "ð"),
    ("<edh/", "ð"),
    ("<thorn/", "þ"),
    ("<atil/", "ã"),
    ("<ndot/", "ṅ"),
    ("<rsdot/", "ṛ"),
    ("<yogh/", "ȝ"),
    ("<mdash/", "—"),
    ("<divide/", "÷"),
    ("<deg/", "°"),
    ("<middot/", "•"),
    ("<root/", "√")
]


class Definition:
    def __init__(self, word, text, source, pos):
        self.word = word
        self.text = text
        self.source = source
        self.pos = pos


def xml_to_objects():
    definition_objects = []

    files = os.listdir("xml_files")
    files = sorted(files)
    files = filter(lambda name: re.match("^gcide.\\w.xml$", name), files)
    files = list(files)

    for file in files:
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
                    print(f"{definition_objects.__len__()} ({entry})")
                    definition_objects.append(
                        Definition(entry, definition, sources, part_of_speech)
                    )

    return definition_objects
