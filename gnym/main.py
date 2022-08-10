import json
from logging import getLogger
from typing import Dict
from urllib.request import urlopen
import sys


def uniquify(seq):
    seen: set = set()
    seen_add = seen.add

    return [x for x in seq if not (x in seen or seen_add(x))]


def retrieve_synonyms(search_term: str) -> Dict[str, object]:
    with urlopen(
        f"https://www.openthesaurus.de/synonyme/search?q={search_term}&format=application/json"
    ) as r:
        data = json.load(r)

    return data["synsets"]


def make_alfred_item(term):
    return {"title": term, "subtitle": "-", "arg": term}


def make_alfred_output(terms):
    return json.dumps({"items": [make_alfred_item(term) for term in terms]})


def main(argv):
    if len(argv) != 1:
        getLogger().error("Invalid number of arguments.")
        return 1

    search_term: str = argv[0]

    synsets = retrieve_synonyms(search_term)

    term_lists = [synset["terms"] for synset in synsets]

    terms = [term.get("term", None) for term_list in term_lists for term in term_list]

    sorted_terms = uniquify(sorted(terms, key=terms.count, reverse=True))

    alfred_output = make_alfred_output(sorted_terms)

    print(alfred_output)


if __name__ == "__main__":
    main(sys.argv[1:])
