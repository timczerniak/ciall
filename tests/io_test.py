import unittest
import spacy

from ciall.io import doc_from_tuples, doc_from_tsv, output_tsv


class TestIO(unittest.TestCase):

    def test_doc_from_tuples(self):
        tuples = [
            ("TOKEN",      "LEMMA",  "PAROLE"),
            ("Níl",        "bí",     "Vmxx"  ),
            ("aon",        "aon",    "Dqxx"  ),
            ("scrúduithe", "scrúdú", "Ncxx"  ),
            ("móra",       "mór",    "Aqxx"  ),
            ("agam",       "ag",     "Spxx"  ),
            (".",          ".",      "Fxx"   ),
        ]

        nlp = spacy.blank("ga")
        doc = doc_from_tuples(nlp, tuples)

        self.assertIsInstance(doc, spacy.tokens.doc.Doc)

        self.assertEqual(doc[0].text, "Níl")
        self.assertEqual(doc[0].lemma_, "bí")
        self.assertEqual(doc[0]._.par_long, "Vmxx")
        self.assertEqual(doc[0]._.par_short, "Vm")

    def test_doc_from_tsv(self):
        tsv = "TOKEN\tLEMMA\tPAROLE\n" \
              "Níl\tbí\tVmxx\n" \
              "aon\taon\tDqxx\n" \
              "scrúduithe\tscrúdú\tNcxx\n" \
              "móra\tmór\tAqxx\n" \
              "agam\tag\tSpxx\n" \
              ".\t.\tFxx\n"

        nlp = spacy.blank("ga")
        doc = doc_from_tsv(nlp, tsv)

        self.assertIsInstance(doc, spacy.tokens.doc.Doc)

        self.assertEqual(doc[0].text, "Níl")
        self.assertEqual(doc[0].lemma_, "bí")
        self.assertEqual(doc[0]._.par_long, "Vmxx")
        self.assertEqual(doc[0]._.par_short, "Vm")

    def test_output_tsv(self):
        intsv = "TOKEN\tLEMMA\tPAROLE\n" \
                "Níl\tbí\tVmxx\n" \
                "aon\taon\tDqxx\n" \
                "scrúduithe\tscrúdú\tNcxx\n" \
                "móra\tmór\tAqxx\n" \
                "agam\tag\tSpxx\n" \
                ".\t.\tFxx\n"  # NOTE: must have the final \n

        nlp = spacy.blank("ga")
        doc = doc_from_tsv(nlp, intsv)
        outtsv = output_tsv(doc, ('TOKEN', 'LEMMA', 'PAROLE'))

        self.assertEqual(intsv, outtsv)