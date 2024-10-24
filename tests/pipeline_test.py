import unittest
import os

import spacy

from ciall.pipeline import make_pipeline


CURR_DIR = os.path.dirname(os.path.abspath(__file__))


class TestIO(unittest.TestCase):

    def test_make_pipeline(self):
        nlp = make_pipeline({
            'components': [
                "ciall_musas_tagger",
                "ciall_doc_tags",
                "ciall_year_detector",
                "ciall_prop_nouns"
            ],
            'ciall_musas_tagger': {
                'sw_lexicon': CURR_DIR + "/components/test_sw_lexicon.tsv",
                'mw_lexicon': CURR_DIR + "/components/test_mw_lexicon.tsv",
            },
        })
        self.assertIsInstance(nlp, spacy.language.Language)