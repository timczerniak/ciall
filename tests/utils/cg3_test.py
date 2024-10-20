import unittest

from ciall.utils.cg3 import CG3Document


CG3_TESTFILE = """"<Níl>"
	"bí" Verb VI PresInd Neg @FMV #1->0
"<aon>"
	"aon" Det Qty Idf @>N #2->3
"<scrúduithe>"
	"scrúdú" Noun Masc Com Pl Len @SUBJ #3->1
	"bí" Verb VI PresInd Neg @FMV #1->0
"<móra>"
	"mór" Adj Com NotSlen Pl @N< #4->3
"<agam>"
	"ag" Pron Prep 1P Sg @PP_HAS #5->1
"<.>"
	"." Punct Fin #6->6

"<Bhuail>"
	"buail" Verb VTI PastInd Len @FMV #1->0
"<mé>"
	"mé" Pron Pers 1P Sg @NP #2->2
"<leis>"
	"le" Prep Simp DefArt @PP_ADVL #3->1
"<an>"
	"an" Art Sg Def @>N #4->5
"<léachtóir>"
	"léachtóir" Noun Masc Com Sg Ecl @P< #5->3
"<inné>"
	"inné" Adj Base @ADVL #6->6
"<.>"
	"." Punct Fin #7->7

"""


class CG3DocumentTest(unittest.TestCase):
    def test_parsing(self):
        """
        Test that the parser parses correctly
        """
        cg3doc = CG3Document.from_string(CG3_TESTFILE)
        cg3doc.reorder_by_lemma_freq()
        self.assertEqual(cg3doc.tokens[0].token, "Níl")
        self.assertEqual(cg3doc.tokens[0].matches[0].lemma, "bí")
        self.assertEqual(cg3doc.tokens[0].matches[0].morph_tags, ["Verb", "VI", "PresInd", "Neg"])
        self.assertEqual(cg3doc.tokens[0].matches[0].par_tag_long, "Vmip---n")
        self.assertEqual(cg3doc.tokens[0].matches[0].par_tag_short, "Vm")
        self.assertEqual(cg3doc.tokens[0].matches[0].udep_tag, "VERB")
        self.assertEqual(cg3doc.tokens[0].matches[0].dep_tags, ["@FMV", "#1->0"])
    
    def test_freq_reorder(self):
        """
        Test that the lemmafreq reordering works
        """
        cg3doc = CG3Document.from_string(CG3_TESTFILE)
        self.assertEqual(cg3doc.tokens[2].matches[0].lemma, "scrúdú")
        self.assertEqual(cg3doc.tokens[2].matches[1].lemma, "bí")
        cg3doc.reorder_by_lemma_freq()
        self.assertEqual(cg3doc.tokens[2].matches[0].lemma, "bí")
        self.assertEqual(cg3doc.tokens[2].matches[1].lemma, "scrúdú")