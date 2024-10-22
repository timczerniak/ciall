import os
import unittest
import spacy

import ciall.components.token_attributes
import ciall.components.musas_tagger


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_SW_LEXICON = CURR_DIR + "/test_sw_lexicon.tsv"
TEST_MW_LEXICON = CURR_DIR + "/test_mw_lexicon.tsv"


def process_test_text(test_text):
    nlp = spacy.blank("ga")
    nlp.add_pipe("ciall_musas_tagger", config={'sw_lexicon': TEST_SW_LEXICON, 'mw_lexicon': TEST_MW_LEXICON})

    words = [t[0] for t in test_text]
    spaces = [True for t in test_text]
    lemmas = [t[1] for t in test_text]
    par_shorts = [t[2] for t in test_text]
    doc = spacy.tokens.doc.Doc(vocab=nlp.vocab, words=words, spaces=spaces)
    for token, lemma, par_short in zip (doc, lemmas, par_shorts):
        token.lemma_ = lemma
        token._.par_short = par_short

    return nlp(doc)


class TestMUSASTagger(unittest.TestCase):

    def test_simple_input(self):
        test_text = [
            ("Níl",        "bí",        "Vm"),
            ("aon",        "aon",       "Dq"),
            ("scrúduithe", "scrúdú",    "Nc"),
            ("móra",       "mór",       "Aq"),
            ("agam",       "ag",        "Sp"),
            (".",          ".",         "F" ),
            ("\n",         "\n",        ""  ),
            ("Bhuail",     "buail",     "Vm"),
            ("mé",         "mé",        "Pp"),
            ("leis",       "le",        "Sp"),
            ("an",         "an",        "Td"),
            ("léachtóir",  "léachtóir", "Nc"),
            ("inné",       "inné",      "Aq"),
            (".",          ".",         "F" ),
        ]
        #expected_lemmas = [
        #    "bí", "aon", "scrúdú", "mór", "ag", ".", "",
        #    "buail", "mé", "le", "an", "léachtóir", "inné", "."
        #]
        expected_sem_tags = [
            # Níl aon scrúduithe móra agam.\n
            ["Z5", "A3+"], "Z5", "X2.4", ["N3.2", "A5.1+"], "Z5", "Z9", None,
            # Bhuail mé leis an léachtóir inné.
            ["A1.1.2"], "Z8", "Z5", "Z5", "P1", "T1.1.1", "Z9"
        ]

        doc = process_test_text(test_text)

        for token, sem_tags in zip (doc, expected_sem_tags):
            if isinstance(sem_tags, str):
                sem_tags = [sem_tags]
            self.assertEqual(sem_tags, token._.musas_tags, "For '%s' expected %s, got %s" % \
                             (token.text, sem_tags, token._.musas_tags))

    def test_multi_word_expressions(self):
        test_text = [
            ("Níl",      "bí",       "Vm"),
            ("aon",      "aon",      "Dq"),
            ("ainm",     "ainm",     "Nc"),
            ("cleite",   "cleite",   "Nc"),
            ("agam",     "ag",       "Sp"),
            (".",        ".",        "F" ),
            ("\n",       "\n",       ""  ),
            ("Rith",     "rith",     "Vm"),
            ("mé",       "mé",       "Pp"),
            ("ó",        "ó",        "Sp"),
            ("Bhaile",   "Baile",    "Np"),
            ("Átha",     "Átha",     "Np"),
            ("Cliath",   "Cliath",   "Np"),
            ("go",       "go",       "Sp"),
            ("Corcaigh", "Corcaigh", "Np"),
            (".",        ".",        "F" ),
            ("\n",       "\n",       ""  ),
            ("Tá",       "bí",       "Vm"),
            ("sé",       "sé",       "Pp"),
            ("ceathrú",  "ceathrú",  "Nc"),
            ("tar",      "tar",      "Sp"),
            ("éis",      "éis",      "Sp"),
            ("a",        "a",        "Q" ),
            ("trí",      "trí",      "Mc"),
            (".",        ".",        "F" ),
        ]

        expected_result = {
            # 'text': ("lemma", "sem_tag")
            'ainm':   ("ainm",   "Q2.2"),
            'cleite': ("cleite", "Q2.2"),

            'Bhaile': ("Baile",  "Z2"),
            'Átha':   ("Átha",   "Z2"),
            'Cliath': ("Cliath", "Z2"),

            'tar': ("tar", "Z5"),
            'éis': ("éis", "Z5"),
        }

        doc = process_test_text(test_text)

        result = {}
        for token in doc:
            #print("%s\t%s\t%s\t%s" % (token.text, token.lemma_, token._.par_short, token._.musas_tags))
            if token.text in expected_result:
                result[token.text] = (token.lemma_, token._.musas_tags[0])

        for text in expected_result.keys():
            self.assertEqual(result[text], expected_result[text],
                             "For '%s' expected %s, got %s" %
                             (text, expected_result[text], result[text]))

    def test_wildcard_lemmas(self):
        # 'Siberia' is purposfully not in the lexicon, and it should be caught by the following wildcard entry:
        #  *   Np   Z0
        test_text = [
            ("Chuaigh", "téigh",   "Vm"),
            ("mé",      "mé",      "Pp"),
            ("go",      "go",      "Sp"),
            ("dtí",     "dtí",     "Nc"),
            ("Siberia", "Siberia", "Np"),
            ("inné",    "inné",    "Aq"),
            (".",       ".",       "F" ),
        ]
        expected_sem_tags = [
            "M1", "Z8", "Z5", "Z5", "Z0", "T1.1.1"
        ]

        doc = process_test_text(test_text)

        for token, sem_tags in zip (doc, expected_sem_tags):
            if isinstance(sem_tags, str):
                sem_tags = [sem_tags]
            self.assertEqual(sem_tags, token._.musas_tags, "For '%s' expected %s, got %s" % \
                             (token.text, sem_tags, token._.musas_tags))