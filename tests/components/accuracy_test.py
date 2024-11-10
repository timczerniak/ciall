import unittest

from spacy.tokens import Token

import ciall.components.accuracy
from ciall.components.accuracy import AccuracyReport


class TestAccuracy(unittest.TestCase):

    def test_accuracy_report(self):
        tokens = [
            # Here are 10 words, which together give a particular set of results
            # par_short  pymusas_tags  expected_pymusas_tag
            ("Nc", ["A1"],       "A1"),  # Fully accurate content word: accuracy 1
            ("Nc", ["B2"],       "B2"),  # Fully accurate content word: accuracy 1
            ("Nc", ["A1", "C1"], "A1"),  # Partially accurate content word: 0 < accuracy < 1
            ("Nc", ["Z99"],      "A1"),  # Unmatched content word: accuracy 0
            ("Nc", ["Z99"],      "A1"),  # Unmatched content word: accuracy 0

            ("D",  ["Z5"],       "Z5"), # Fully accurate non-content word: accuracy 1
            ("Sp", ["Z8"],       "Z8"), # Fully accurate non-content word: accuracy 1
            ("Sp", ["Z8"],       "Z5"), # Partially accurate non-content word: 0 < accuracy < 1
            ("D",  ["Z99"],      "Z5"), # Unmatched non-content word: accuracy 0
            ("D",  ["Z99"],      "Z5"), # Unmatched non-content word: accuracy 0
        ]

        report = AccuracyReport()
        for par_short, pymusas_tags, expected_pymusas_tag in tokens:
            report.add_token(par_short=par_short,
                             pymusas_tags=pymusas_tags,
                             expected_pymusas_tag=expected_pymusas_tag)
        report.calculate_totals()

        print(report.all_match_values)
        self.assertAlmostEqual(report.lexical_coverage, 60.0)
        self.assertAlmostEqual(report.pc_all_fully_correct, 40.0)
        self.assertAlmostEqual(report.pc_cont_fully_correct, 40.0)
        self.assertGreater(report.pc_all_accuracy, 40.0)
        self.assertLess(report.pc_all_accuracy, 60.0)
        self.assertGreater(report.pc_cont_accuracy, 40.0)
        self.assertLess(report.pc_cont_accuracy, 60.0)