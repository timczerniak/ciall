import csv
import io

import spacy

from ciall.utils.pos2par import pos2par, shorten_par_tag


VALID_FIELDS = [
    # Added by the pipeline
    "ID",               # The token ID (line number)

    # Input fields
    "TOKEN",            # The raw token text (word)
    "LEMMA",            # The lemma
    "MORPH_TAGS",       # The morphological tags
    "DEP_TAGS",         # The other dependency tags
    "DEPTREE_TAG"       # The dependency tree tag
    "POS",              # The UD POS tag
    "PAROLE",           # The full PAROLE tag
    "PAR_SHORT",        # The short PAROLE tag

    # Output fields
    "MWE",              # THE MWE index
    "USAS",             # The USAS semantic tags
    "USAS_DESCRIPTION", # The USAS semantic tags description
]


def doc_from_tuples(nlp: spacy.language.Language, lines: list[tuple]) -> spacy.tokens.doc.Doc:
    """
    Build a SpaCy Doc object from a list of tuples.

    The first tuple is treated as the names of each field,
    and subsequent tuples are treated as the values for each token in the document.
    """

    # The first row is expected to be the header row, containing all the field names
    fields = lines[0]
    for field in fields:
        if field not in VALID_FIELDS:
            raise TypeError("Field '%s' is not a valid field!" % field)

    if 'TOKEN' not in fields:
        raise TypeError("Must have at least a 'TOKEN' field specified!")

    # initialise data
    data = {'space': []}
    for f in VALID_FIELDS:
        if f in fields:
            data[f] = []

    for row in lines[1:]:
        if len(row) != len(fields):
            raise TypeError("Row doesn't match header length: %s" % (row,))
        for f, v in zip(fields, row):
            data[f].append(v)
        data['space'].append(True)  # TODO: something more intelligent?

    doc = spacy.tokens.doc.Doc(vocab=nlp.vocab, words=data['TOKEN'], spaces=data['space'])

    # read the other input fields (if they are present)
    for i in range(len(data['TOKEN'])):
        if 'LEMMA' in data:
            doc[i].lemma_ = data['LEMMA'][i]

        if 'MORPH_TAGS' in data:
            doc[i]._.morph_tags = data['MORPH_TAGS'][i].split(" ")

        if 'DEP_TAGS' in data:
            doc[i]._.dep_tags = data['DEP_TAGS'][i].split(" ")

        if 'DEPTREE_TAG' in data:
            doc[i]._.deptree_tag = data['DEPTREE_TAG'][i]

        if 'POS' in data:
            doc[i].pos_ = data['POS'][i]

        if 'PAROLE' in data:
            doc[i]._.par_long = data['PAROLE'][i]

        if 'PAR_SHORT' in data:
            doc[i]._.par_short = data['PAR_SHORT'][i]
        elif 'PAROLE' in data:
            doc[i]._.par_short = shorten_par_tag(doc[i]._.par_long)

    return doc


def doc_from_tsv(nlp: spacy.language.Language, tsv: str) -> spacy.tokens.doc.Doc:
    tsv_reader = csv.reader(tsv.splitlines(), delimiter="\t")
    tuples = [row for row in tsv_reader]
    return doc_from_tuples(nlp, tuples)

def output_tsv(doc: spacy.tokens.doc.Doc, fields: tuple[str]):
    for f in fields:
        if f not in VALID_FIELDS:
            raise TypeError("Invalid output field: '%s'" % f)

    outstr = io.StringIO()

    outstr.write("\t".join(fields) + "\n")

    for i in range(len(doc)):
        line_number = i + 1
        token = doc[i]
        token_text = token.text.replace('\n', '\\n')
        t = {
            'ID': str(line_number),
            'TOKEN': token_text,
            'LEMMA': token.lemma_,
            'MORPH_TAGS': token._.morph_tags_str(),
            'DEP_TAGS': token._.dep_tags_str(),
            'POS': token.pos_,
            'PAROLE': token._.par_long,
            'PAR_SHORT': token._.par_short,
            'MWE': token._.musas_mwe_indexes_str(),
            'USAS': token._.musas_tags_str(),
            'USAS_DESC': token._.musas_desc_str(),
            'DEPTREE_TAG': token._.deptree_tag,
        }
        outstr.write("\t".join([t[f] for f in fields]) + "\n")

    return outstr.getvalue()