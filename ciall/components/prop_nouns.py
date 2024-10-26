import spacy
from spacy.language import Language


PAR_TAG_PROP_NOUN = "Np"
MORPH_TAG_PERS = "Pers"
MORPH_TAG_PNAME = "PName"
MORPH_TAG_PERSNAME = "PersName"
MORPH_TAG_FAM = "Fam"
MORPH_TAG_PLACE = "Place"
PERS_NAME_USAS_TAG = "Z1"
PLACE_USAS_TAG = "Z2"


# Proper Noun disambiguator
@Language.component("ciall_prop_nouns")
def prop_nouns_function(doc):
    """
    Unmatched proper nouns receive the USAS tag Z0. This component uses Morphological tags assigned by the FST
    pipeline to re-assign tokens with Z0 tags to either Z1 (Personal names) or Z2 (Geographical names) where it can.
    """

    for token in doc:
        if token._.par_short == PAR_TAG_PROP_NOUN:
            #print(token.text, token._.morph_tags)
            tag_to_assign = None
            if MORPH_TAG_PERS in token._.morph_tags:  # Personal name - Z1
                # This is an old way of tagging Personal names
                tag_to_assign = PERS_NAME_USAS_TAG
            elif MORPH_TAG_PNAME in token._.morph_tags:  # Personal name - Z1
                # This is the new way of tagging Personal names
                tag_to_assign = PERS_NAME_USAS_TAG
            elif MORPH_TAG_PERSNAME in token._.morph_tags:  # Personal name - Z1
                # This is the new way of tagging Personal names
                tag_to_assign = PERS_NAME_USAS_TAG
            elif MORPH_TAG_FAM in token._.morph_tags:  # Family name - Z1
                tag_to_assign = PERS_NAME_USAS_TAG
            elif MORPH_TAG_PLACE in token._.morph_tags:  # Placename - Z2
                tag_to_assign = PLACE_USAS_TAG

            if tag_to_assign != None:
                token._.pymusas_tags = [tag_to_assign]

    return doc