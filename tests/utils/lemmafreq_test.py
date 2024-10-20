import unittest

from ciall.utils.lemmafreq import lemmafreq


class TestLemmafreq(unittest.TestCase):
    def test_lemmafreq(self):
        # A very simple test to ensure that the lemmafreq() function works
        self.assertGreater(lemmafreq("agus"), lemmafreq("ciallaigh"))