import os
import csv
from io import StringIO

import spacy
from spacy.language import Language
from spacy.tokens import Token, Doc

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rule_based import RuleBasedTagger
# from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger as SpacyRuleBasedTagger  # Not used directly

from ciall.utils.musas_tags import MultiSenseTag


# This is a duplicate of 'pymusas_tags' set by pymusas' spacy RuleBasedTagger.__init__() function
Token.set_extension("musas_tags", default=None)
def musas_tags_str(token):
    if token._.musas_tags is None:
        tags_str = ""
    else:
        tags_str = " ".join(token._.musas_tags)
    return tags_str
Token.set_extension("musas_tags_str", method=musas_tags_str)

# USAS_Description
def pymusas_desc_str(token):
    if token._.musas_tags is None:
        desc_str = ""
    else:
        mst = MultiSenseTag(token._.musas_tags[0])
        desc_str = mst.senses[0].description
    return desc_str
Token.set_extension("musas_desc_str", method=pymusas_desc_str)

# This is a duplicate of 'pymusas_mwe_indexes' set by pymusas' spacy RuleBasedTagger.__init__() function
Token.set_extension("musas_mwe_indexes", default=None)
def musas_mwe_indexes_str(token):
    if token._.musas_mwe_indexes is None:
        mwe_index_str = ""
    else:
        # NOTE: This only prints out the first mwe index
        start, end = token._.musas_mwe_indexes[0]
        mwe_index_str = "(%s, %s)" % (start, end)
    return mwe_index_str
Token.set_extension("musas_mwe_indexes_str", method=musas_mwe_indexes_str)


WILDCARD_LEXICON = {
    'Mn': "N1",
    'Mo': "N1",
    'Mc': "N5",
    'Ms': "Z5",
    'Np': "Z0",
    'C':  "Z5",
    'Cc': "Z5",
    'Cs': "Z5",
    'Dd': "Z5",
    'Dp': "Z5",
    'Dq': "Z5",
    'Dw': "Z5",
    'F':  "Z9",
    'Fe': "Z9",
    'Fi': "Z9",
    'Fa': "Z9",
    'Fz': "Z9",
    'Fb': "Z9",
    'Fq': "Z9",
    'Fc': "I1",
    'Pp': "Z8",
    'Px': "Z5",
    'Pq': "Z5",
    'Pi': "Z5",
    'Pr': "Z8",
    'Pd': "Z5",
    'Q':  "Z5",
    'Qq': "Z5",
    'Qn': "Z6",
    'Sp': "Z5",
    'Td': "Z5",
    'Xfp': "Z0",
    'Xfenp': "Z0",
    'Y':  "Z0",
    'U':  "Z5",
    'Uv': "Z5",
    'Uc': "Z5",
    'Ua': "Z5",
    'Um': "Z5",
    'Ud': "Z5",
    'Up': "Z1",
    'Uw': "Z5",
    'W':  "Z5",
    'X*': "Z9",
    'Xa': "Z9",
}


# The PyMUSAS component factory
@Language.factory("ciall_musas_tagger", default_config={"sw_lexicon": None, "mw_lexicon": None})
def create_musas_tagger_component(nlp: Language, name: str, sw_lexicon: str, mw_lexicon: str):
    return MUSASTagger(nlp, sw_lexicon, mw_lexicon)


# The PyMUSAS pipeline component
class MUSASTagger:

    def __init__(self, nlp: Language, sw_lexicon = None, mw_lexicon = None):
        if sw_lexicon is None:
            raise TypeError("sw_lexicon must be a file path")
        elif os.path.isfile(sw_lexicon):
            self.sw_lexicon = sw_lexicon
        else:
            raise FileExistsError("Cannot find sw_lexicon file: %s" % sw_lexicon)

        if mw_lexicon is None:
            raise TypeError("mw_lexicon must be either a full file path or the lexicon contents")
        elif os.path.isfile(mw_lexicon):
            self.mw_lexicon = mw_lexicon
        else:
            raise FileExistsError("Cannot find mw_lexicon file: %s" % mw_lexicon)

        # self.wc_lexicon = ""

    def __call__(self, doc: Doc):
        """
        This PyMUSAS component is re-implemented here because:
        - Spacy doesn't allow assigning the 'pos_' attribute to be a PAROLE tag (it must be a universal deps tag).
        - pymusas.spacy_api.taggers.rule_based.RuleBasedTagger) uses the 'pos_' tag by default, and it's not simple
        to override it to use the 'par_tag_short' attribute instead.
        - We want to do a second pass to tag all of the less likely senses.

        A note about the Wildcard lemma lexicon:
        The wildcard lexicon file is formatted like the single-word
        lexicon, but with wildcards in the lemma position like so:
        *   <POSTAG>  <SEMTAGS>
        Here we'll assign the SEMTAGS listed for any token in the doc that
        matches that POSTAG and has an 'unmatched' result after PyMUSAS (i.e. Z99 tag)
        This exists because PyMUSAS doesn't do this by default
        """

        # Single-word lexicon
        single_lexicon = LexiconCollection.from_tsv(self.sw_lexicon)
        single_lemma_lexicon = LexiconCollection.from_tsv(self.sw_lexicon, include_pos=False)
        single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon, pos_mapper=None)

        # Multi-word lexicon
        mwe_lexicon = MWELexiconCollection.from_tsv(self.mw_lexicon)
        mwe_rule = MWERule(mwe_lexicon, pos_mapper=None)

        # Build the tagger
        rules = [single_rule, mwe_rule]  # single and multi word rules
        ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        tagger = RuleBasedTagger(rules, ranker)

        # Run the tagger
        tokens = ["" for token in doc]  # remove the token because the pymusas rankers put tokens above lemmas
        lemmas = [token.lemma_ for token in doc]
        par_tags = [token._.par_short for token in doc]
        tagger_results = tagger(tokens, lemmas, par_tags)

        # Store results
        for (token, result) in zip(doc, tagger_results):
            if token.text.strip() == "":  # do nothing for blank tokens, newlines etc
                continue
            token._.musas_tags = result[0]
            token._.musas_mwe_indexes = result[1]
            #print("%s\t%s\t%s\t%s\t%s" % (token.text, token.lemma_, token._.par_long, token._.par_short, token._.musas_tags))

        # # Read wildcard lemma lexicon
        # wildcards = {}
        # wc_lexicon_file = open(self.wc_lexicon, "r", encoding="utf8")
        # tsv_reader = csv.reader(wc_lexicon_file, delimiter="\t")
        # next(tsv_reader)  # Skip the first row, which is the header
        # for row in tsv_reader:
        #     (lemma, par_short, semantic_tags) = row
        #     if lemma == "*":  # this should always be true
        #         #print(par_short, semantic_tags)
        #         wildcards[par_short] = semantic_tags.split(" ")

        # Run wildcard lemma lexicon
        for token in doc:
            #print(token, token._.par_short, token._.musas_tags)
            if token._.par_short in WILDCARD_LEXICON and token._.musas_tags[0] == "Z99":
                #print(token.text, token._.musas_tags, wildcards[token._.par_short])
                token._.musas_tags = [WILDCARD_LEXICON[token._.par_short]]

        return doc