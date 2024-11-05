import csv

import spacy

from ciall.utils import pos2par
import ciall.components.token_attributes
import ciall.components.musas_tagger
import ciall.components.doc_tags
import ciall.components.year_detector
import ciall.components.prop_nouns
import ciall.components.accuracy
#import ga_nlp.sem_dis.frames


# For the tokenizer, which we only use during tests
# PREFIXES = ["mb'", "mB'", "MB'", "b'", "B'", "d'", "dh'", "D'", "Dh'", "m'", "M'",
#             "ana-", "an-", "dod'", "lem'", "s'", "S'", "ars'", "a'", "N'", "n'"]

# A list of valid components
# These names match the name in the @Language.component header decorator
COMPONENTS = (
    #"sentenciser",  # to be added from ga_sem_tag
    #"deptree",  # to be added from ga_sem_tag
    "ciall_musas_tagger",
    "ciall_doc_tags",
    "ciall_year_detector",
    "ciall_prop_nouns",
    #"ciall_frames",  # to be added from ga_sem_tag
)


def make_pipeline(conf: dict, accuracy: bool = False) -> spacy.language.Language:
    """
    Only used when feeding raw text into the pipeline
    """

    nlp = spacy.blank("ga")

    # insert tokenizer customizations
    # prefixes = list(nlp.Defaults.prefixes)
    # for pf in PREFIXES:
    #     prefixes.append(pf)
    # prefix_regex = spacy.util.compile_prefix_regex(prefixes)
    # nlp.tokenizer.prefix_search = prefix_regex.search

    if 'components' not in conf:
        raise TypeError("No 'components' key found in config!")
    components = conf['components']

    for cmp in components:
        if cmp not in COMPONENTS:
            raise TypeError("%s is not a valid component!" % cmp)
        if cmp in conf:
            nlp.add_pipe(cmp, config=conf[cmp])
        else:
            nlp.add_pipe(cmp)

    # If measuring accuracy, add the component for that
    if accuracy:
        nlp.add_pipe("ciall_accuracy")

    return nlp