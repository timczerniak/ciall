import unittest

from ciall.utils.musas_tags import Tag, TagComparison, CompoundTag, MultiSenseTag


class TestMusasTag(unittest.TestCase):

    def test_tag_parsing(self):
        tag = Tag("S1.2.3mf-")
        self.assertEqual(tag.field, "S")
        self.assertEqual(tag.subdivisions_str, "1.2.3")
        self.assertEqual(tag.subdivisions, ["1", "2", "3"])
        self.assertEqual(tag.category, "S1.2.3")
        self.assertEqual(tag.symbols_str, "mf-")
        self.assertEqual(tag.symbols, {"m", "-", "f"})

        tag = Tag("A1.2fci++")
        self.assertEqual(tag.field, "A")
        self.assertEqual(tag.subdivisions_str, "1.2")
        self.assertEqual(tag.subdivisions, ["1", "2"])
        self.assertEqual(tag.category, "A1.2")
        self.assertEqual(tag.symbols_str, "fci++")
        self.assertEqual(tag.symbols, {"c", "++", "i", "f"})

    def test_tag_str_repr(self):
        tag_str = "S1.0.3mf-"
        tag = Tag(tag_str)
        self.assertEqual(str(tag), tag_str)
        self.assertEqual(repr(tag), "Tag(%s)" % tag_str)

    def test_tag_descriptions(self):
        tag = Tag("S1.2.3mf-")
        self.assertEqual(tag.field_description, "Social actions, states and processes")
        self.assertEqual(tag.category_description, "Egoism")

    def test_tag_eq(self):
        tag1 = Tag("S1.2.3mf-")
        tag2 = Tag("S1.2.3mf-")
        tag3 = Tag("Q3.4.5ni-")
        self.assertNotEqual(id(tag1), id(tag2))
        self.assertNotEqual(id(tag2), id(tag3))
        self.assertNotEqual(id(tag3), id(tag1))
        self.assertEqual(tag1, tag2)
        self.assertNotEqual(tag2, tag3)
        self.assertNotEqual(tag3, tag1)

    def test_tag_comparison(self):
        self.assertEqual(Tag("A1.2.3f+").compare(Tag("A1.2.3f+")), TagComparison.EQUAL)
        self.assertEqual(Tag("A1.2.3m+").compare(Tag("A1.2.3f+")), TagComparison.SAME_CATEGORY)
        self.assertEqual(Tag("A1.2.3").compare(Tag("A1.2.3f+")), TagComparison.SAME_CATEGORY)
        self.assertEqual(Tag("A1.2m+").compare(Tag("A1.2.3f+")), TagComparison.SUB_CATEGORY)
        self.assertEqual(Tag("A1.2").compare(Tag("A1.2.3f+")), TagComparison.SUB_CATEGORY)
        self.assertEqual(Tag("A1f+").compare(Tag("A1.2.3f+")), TagComparison.SUB_CATEGORY)
        self.assertEqual(Tag("A1.3f+").compare(Tag("A1.2.3f+")), TagComparison.SAME_1L_DIV)
        self.assertEqual(Tag("A1.3.5").compare(Tag("A1.2.3f+")), TagComparison.SAME_1L_DIV)
        self.assertEqual(Tag("A4.7n-").compare(Tag("A1.2.3f+")), TagComparison.SAME_FIELD)
        self.assertEqual(Tag("A4").compare(Tag("A1.2.3f+")), TagComparison.SAME_FIELD)
        self.assertEqual(Tag("Q4.5").compare(Tag("A1.2.3f+")), TagComparison.UNEQUAL)

    def test_tag_match(self):
        self.assertEqual(Tag("A1.2.3f+").match(Tag("A1.2.3f+")), 1.0)
        self.assertEqual(Tag("A1.2.3m+").match(Tag("A1.2.3f+")), 0.8)
        self.assertEqual(Tag("A1.2.3").match(Tag("A1.2.3f+")), 0.8)
        self.assertEqual(Tag("A1.2m+").match(Tag("A1.2.3f+")), 0.7)
        self.assertEqual(Tag("A1.2").match(Tag("A1.2.3f+")), 0.7)
        self.assertEqual(Tag("A1f+").match(Tag("A1.2.3f+")), 0.7)
        self.assertEqual(Tag("A1.3f+").match(Tag("A1.2.3f+")), 0.6)
        self.assertEqual(Tag("A1.3.5").match(Tag("A1.2.3f+")), 0.6)
        self.assertEqual(Tag("A4.7n-").match(Tag("A1.2.3f+")), 0.4)
        self.assertEqual(Tag("A4").match(Tag("A1.2.3f+")), 0.4)
        self.assertEqual(Tag("Q4.5").match(Tag("A1.2.3f+")), 0.0)


class TestMusasCompoundTag(unittest.TestCase):

    def test_compound_tag_parsing(self):
        ctag = CompoundTag("Q1.2/S2mf")
        self.assertEqual(ctag.num_tags, 2)
        self.assertEqual(ctag.tags[0].category, "Q1.2")
        self.assertEqual(ctag.tags[1].category, "S2")

    def test_compount_tag_description(self):
        ctag = CompoundTag("Q1.2/S2mf")
        self.assertEqual(ctag.description, "Paper documents and writing / People")

    def test_compound_tag_match(self):
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("S2mf/Q1.2")), 1.0)
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("S2mf")), 0.5)
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("Q1.2")), 0.5)
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("S2")), 0.4)
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("S2mf/A1.2")), 0.25)
        self.assertEqual(CompoundTag("Q1.2/S2mf").match(CompoundTag("S2/A1.2")), 0.2)


class TestMusasMultiSenseTag(unittest.TestCase):

    def test_multisense_tag_parsing(self):
        mstag = MultiSenseTag("Q1.2/S2mf S7.2.5-")
        self.assertEqual(mstag.num_senses, 2)
        self.assertEqual(mstag.senses[0].num_tags, 2)
        self.assertEqual(mstag.senses[0].tags[0].category, "Q1.2")
        self.assertEqual(mstag.senses[0].tags[1].category, "S2")
        self.assertEqual(mstag.senses[1].num_tags, 1)
        self.assertEqual(mstag.senses[1].tags[0].category, "S7.2.5")
        mstag = MultiSenseTag("Q1.2/S2mf,S7.2.5-")  # same but with a comma instead of a space
        self.assertEqual(mstag.num_senses, 2)
        self.assertEqual(mstag.senses[0].num_tags, 2)
        self.assertEqual(mstag.senses[0].tags[0].category, "Q1.2")
        self.assertEqual(mstag.senses[0].tags[1].category, "S2")
        self.assertEqual(mstag.senses[1].num_tags, 1)
        self.assertEqual(mstag.senses[1].tags[0].category, "S7.2.5")

    def test_multisense_tag_match(self):
        tests = [
            # no match
            ("Q1.2/S2mf L7.2.5- A1.2 B5", "C3.6/N5mf-", 0.0),
            # exact compound tag matches
            ("Q1.2/S2mf", "Q1.2/S2mf", 1.0),  # position 1, num 1
            ("Q1.2/S2mf L7.2.5-", "Q1.2/S2mf", 0.85),  # position 1, num 2
            ("Q1.2/S2mf L7.2.5-", "L7.2.5-",   0.5 ),  # position 2, num 2
            ("Q1.2/S2mf L7.2.5- A1.2", "Q1.2/S2mf", 0.8  ),  # position 1, num 3
            ("Q1.2/S2mf L7.2.5- A1.2", "L7.2.5-",   0.45 ),  # position 2, num 3
            ("Q1.2/S2mf L7.2.5- A1.2", "A1.2",      0.333),  # position 3, num 3
            ("Q1.2/S2mf L7.2.5- A1.2 B5", "Q1.2/S2mf", 0.775),  # position 1, num 4
            ("Q1.2/S2mf L7.2.5- A1.2 B5", "L7.2.5-",   0.425),  # position 2, num 4
            ("Q1.2/S2mf L7.2.5- A1.2 B5", "A1.2",      0.308),  # position 3, num 4
            ("Q1.2/S2mf L7.2.5- A1.2 B5", "B5",        0.25 ),  # position 4, num 4
            # partial compound tag matches
            ("Q1.2/S2mf L7.2.5-", "S2mf", 0.425),  # half match with first position of 2
            ("Q1.2/S2mf L7.2.5-", "Q1.2", 0.425),  # half match with first position of 2
            ("Q1.2/S2mf L7.2.5-", "S2",   0.34),  # partial half match with first position of 2
        ]

        for mst, ct, mv in tests:
            self.assertEqual(round(MultiSenseTag(mst).match(CompoundTag(ct)), 3), mv)