import unittest

from ciall.utils.pos2par import pos2par


class TestPos2Par(unittest.TestCase):

    TEST_CASES = [
        # English
        ("Foreign English Noun", "Xfen", "Xf", "X"),

        # Nouns
        ("Noun Masc Gen Pl",     "Ncmpg", "Nc", "NOUN"),
        ("Noun Masc Com Sg",     "Ncmsc", "Nc", "NOUN"),
        ("Noun Fem Com Pl Ecl",  "Ncfpc", "Nc", "NOUN"),
        ("Prop Noun Fem Dat Sg", "Npfsd", "Np", "NOUN"),
        ("Verbal Noun",          "Nv",    "Nv", "NOUN"),
        ("Subst Noun Sg",        "Ns-s",  "Ns", "NOUN"),

        # Verbs
        ("Verb VI PresInd Neg",     "Vmip---n", "Vm", "VERB"),
        ("Verb VI FutInd",          "Vmif",     "Vm", "VERB"),
        ("Verb VD FutInd Auto",     "Vmif0",    "Vm", "VERB"),
        ("Verb VTI PastInd Len",    "Vmis",     "Vm", "VERB"),
        ("Verb VI PastInd Dep Ecl", "Vmis---d", "Vm", "VERB"),

        # Adjectives
        ("Adj Com NotSlen Pl", "Aqp-pc", "Aq", "ADJ"),
        ("Adj Base",           "Aqp",    "Aq", "ADJ"),
        ("Adj Masc Com Sg",    "Aqpmsc", "Aq", "ADJ"),
        ("Adj Verbal",         "Avp",    "Av", "ADJ"),

        # Pronouns
        ("Pron Prep 1P Sg",          "Pr1-s",  "Pr", "PRON"),
        ("Pron Pers 3P Sg Masc Sbj", "Pp3msn", "Pp", "PRON"),
        ("Pron Pers 3P Sg Masc",     "Pp3ms",  "Pp", "PRON"),
        ("Pron Pers 1P Sg",          "Pp1-s",  "Pp", "PRON"),
        ("Pron Dem",                 "Pd",     "Pd", "PRON"),

        # Determiners
        ("Det Dem",     "Dd", "Dd", "DET"),
        ("Det Qty Idf", "Dq", "Dq", "DET"),

        # Copula
        ("Cop Pres",    "Wp-i", "W", "AUX"),
        ("Cop Pro Dem", "W",    "W", "AUX"),

        # Adverb
        ("Adv Dir", "Rd", "R", "ADV"),
        ("Adv Loc", "Rl", "R", "ADV"),

        # Prepositions
        ("Prep Poss 3P Sg Fem", "Spp-s", "Sp", "ADP"),
        ("Prep Cmpd",           "Spc",   "Sp", "ADP"),
        ("Prep Simp Vow",       "Sp",    "Sp", "ADP"),
        ("Prep Simp",           "Sp",    "Sp", "ADP"),
        #("Pron Prep 1P Sg", "S", "S"), # Pronoun, not Preposition
        #("Pron Prep 3P Sg Masc", "S", "S"), # Pronoun, not Preposition?

        # Articles
        ("Art Sg Def",     "Td-s",  "Td", "DET"),
        ("Art Pl Def",     "Td-p",  "Td", "DET"),
        ("Art Sg Fem Gen", "Tdfsg", "Td", "DET"),

        # Conjunctions
        ("Conj Coord",  "Cc", "C", "CCONJ"),
        ("Conj Subord", "Cs", "C", "CCONJ"),
        #("Conj Cop", "C-w", "C"), # Copula, not Conjunction

        # Numeral
        ("Num Card", "Mc", "Mc", "NUM"),
        ("Num Ord",  "Mo", "Mo", "NUM"),
        ("Num Pers", "Mp", "Mp", "NUM"),
        ("Num Rom",  "Mr", "Mr", "NUM"),
        ("Num Op",   "Ms", "Ms", "NUM"),

        # Interjections
        ("Itj", "I", "I", "INTJ"),

        # Verbal Particles
        ("Part Vb Rel Direct", "Q-r",  "Q", "PART"),
        ("Part Vb Neg",        "Qn",   "Q", "PART"),
        ("Part Vb Neg Q Past", "Qnqs", "Q", "PART"),
        #("Part Vb Cmpl",       "Q",    "Q", "PART"), # what is Cmpl?
        #("Part Vb Cond",       "Q",    "Q", "PART"), # Cond isn't covered yet
    ]

    def test_pos2par(self):
        for pos_tags, long_tag, short_tag, udep_tag in self.TEST_CASES:
            pos_tags = pos_tags.split()
            lpt, spt, ut = pos2par(pos_tags)
            self.assertEqual(lpt, long_tag, "%s (long) == %s" % (lpt, long_tag))
            self.assertEqual(spt, short_tag, "%s (short) == %s" % (spt, short_tag))
            self.assertEqual(ut, udep_tag, "%s (short) == %s" % (ut, udep_tag))