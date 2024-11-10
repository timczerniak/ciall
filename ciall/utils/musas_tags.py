"""
musas_tags.py

This file contains utilities for dealing with the (M)USAS tagset

"""

import re
from enum import Enum


DESCRIPTIONS = {
    # A: GENERAL AND ABSTRACT TERMS
    'A': "General and abstract terms",
    'A1': "General",
    'A1.1.1': "General actions, making etc.",
    'A1.1.2': "Damaging and destroying",
    'A1.2': "Suitability",
    'A1.3': "Caution",
    'A1.4': "Chance, luck",
    'A1.5': "Use",
    'A1.5.1': "Using",
    'A1.5.2': "Usefulness",
    'A1.6': "Physical/mental",
    'A1.7': "Constraint",
    'A1.8': "Inclusion/Exclusion",
    'A1.9': "Avoiding",
    'A2': "Affect",
    'A2.1': "Affect: Modify, change",
    'A2.2': "Affect: Cause/Connected",
    'A3': "Being",
    'A4': "Classification",
    'A4.1': "Generally kinds, groups, examples",
    'A4.2': "Particular/general; detail",
    'A5': "Evaluation",
    'A5.1': "Evaluation: Good/bad",
    'A5.2': "Evaluation: True/false",
    'A5.3': "Evaluation: Accuracy",
    'A5.4': "Evaluation: Authenticity",
    'A6': "Comparing",
    'A6.1': "Comparing: Similar/different",
    'A6.2': "Comparing: Usual/unusual",
    'A6.3': "Comparing: Variety",
    'A7': "Definite (+ modals)",
    'A8': "Seem",
    'A9': "Getting and giving; possession",
    'A10': "Open/closed; Hiding/Hidden; Finding; Showing",
    'A11': "Importance",
    'A11.1': "Importance: Important",
    'A11.2': "Importance: Noticeability",
    'A12': "Easy/difficult",
    'A13': "Degree",
    'A13.1': "Degree: Non-specific",
    'A13.2': "Degree: Maximizers",
    'A13.3': "Degree: Boosters",
    'A13.4': "Degree: Approximators",
    'A13.5': "Degree: Compromisers",
    'A13.6': "Degree: Diminishers",
    'A13.7': "Degree: Minimizers",
    'A14': "Exclusivizers/particularizers",
    'A15': "Safety/Danger",

    # B: THE BODY AND THE INDIVIDUAL
    'B': "The body and the individual",
    'B1': "Anatomy and physiology",
    'B2': "Health and disease",
    'B3': "Medicines and medical treatment",
    'B4': "Cleaning and personal care",
    'B5': "Clothes and personal belongings",

    # C: ARTS AND CRAFTS
    'C': "Arts and crafts",
    'C1': "Arts and crafts",

    # E: EMOTIONAL ACTIONS, STATES AND PROCESSES
    'E': "Emotional actions, states and processes",
    'E1': "General",
    'E2': "Liking",
    'E3': "Calm/Violent/Angry",
    'E4': "Happy/sad",
    'E4.1': "Happy/sad: Happy",
    'E4.2': "Happy/sad: Contentment",
    'E5': "Fear/bravery/shock",
    'E6': "Worry, concern, confident",

    # F: FOOD AND FARMING
    'F': "Food and farming",
    'F1': "Food",
    'F2': "Drinks",
    'F3': "Cigarettes and drugs",
    'F4': "Farming & Horticulture",

    # G: GOVERNMENT AND THE PUBLIC DOMAIN
    'G': "Government and the public domain",
    'G1': "Government, Politics & elections",
    'G1.1': "Government etc.",
    'G1.2': "Politics",
    'G2': "Crime, law and order",
    'G2.1': "Crime, law and order: Law & order",
    'G2.2': "General ethics",
    'G3': "Warfare, defence and the army; Weapons",

    # H: ARCHITECTURE, BUILDINGS, HOUSES AND THE HOME
    'H': "Architecture, buildings, houses and the home",
    'H1': "Architecture, kinds of houses & buildings",
    'H2': "Parts of buildings",
    'H3': "Areas around or near houses",
    'H4': "Residence",
    'H5': "Furniture and household fittings",

    # I: MONEY AND COMMERCE
    'I': "Money and commerce",
    'I1': "Money generally",
    'I1.1': "Money: Affluence",
    'I1.2': "Money: Debts",
    'I1.3': "Money: Price",
    'I2': "Business",
    'I2.1': "Business: Generally",
    'I2.2': "Business: Selling",
    'I3': "Work and employment",
    'I3.1': "Work and employment: Generally",
    'I3.2': "Work and employment: Professionalism",
    'I4': "Industry",

    # K: ENTERTAINMENT, SPORTS AND GAMES
    'K': "Entertainment, sports and games",
    'K1': "Entertainment generally",
    'K2': "Music and related activities",
    'K3': "Recorded sound etc.",
    'K4': "Drama, the theatre & show business",
    'K5': "Sports and games generally",
    'K5.1': "Sports",
    'K5.2': "Games",
    'K6': "Children's games and toys",

    # L: LIFE AND LIVING THINGS
    'L': "Life and living things",
    'L1': "Life and living things",
    'L2': "Living creatures generally",
    'L3': "Plants",

    # M: MOVEMENT, LOCATION, TRAVEL AND TRANSPORT
    'M': "Movement, location, travel and transport",
    'M1': "Moving, coming and going",
    'M2': "Putting, taking, pulling, pushing, transporting &c.",
    'M3': "Movement/transportation: land",
    'M4': "Movement/transportation: water",
    'M5': "Movement/transportation: air",
    'M6': "Location and direction",
    'M7': "Places",
    'M8': "Remaining/stationary",

    # N: NUMBERS AND MEASUREMENT
    'N': "Numbers and measurement",
    'N1': "Numbers",
    'N2': "Mathematics",
    'N3': "Measurement",
    'N3.1': "Measurement: General",
    'N3.2': "Measurement: Size",
    'N3.3': "Measurement: Distance",
    'N3.4': "Measurement: Volume",
    'N3.5': "Measurement: Weight",
    'N3.6': "Measurement: Area",
    'N3.7': "Measurement: Length & height",
    'N3.8': "Measurement: Speed",
    'N4': "Linear order",
    'N5': "Quantities",
    'N5.1': "Entirety; maximum",
    'N5.2': "Exceeding; waste",
    'N6': "Frequency etc.",

    # O: SUBSTANCES, MATERIALS, OBJECTS AND EQUIPMENT
    'O': "Substances, materials, objects and equipment",
    'O1': "Substances and materials generally",
    'O1.1': "Substances and materials generally: Solid",
    'O1.2': "Substances and materials generally: Liquid",
    'O1.3': "Substances and materials generally: Gas",
    'O2': "Objects generally",
    'O3': "Electricity and electrical equipment",
    'O4': "Physical attributes",
    'O4.1': "General appearance and physical properties",
    'O4.2': "Judgement of appearance (pretty etc.)",
    'O4.3': "Colour and colour patterns",
    'O4.4': "Shape",
    'O4.5': "Texture",
    'O4.6': "Temperature",

    # P: EDUCATION
    'P': "Education",
    'P1': "Education in general",

    # Q: LINGUISTIC ACTIONS, STATES AND PROCESSES
    'Q': "Linguistic actions, states and processes",
    'Q1': "Communication",
    'Q1.1': "Communication in general",
    'Q1.2': "Paper documents and writing",
    'Q1.3': "T elecommunications",
    'Q2': "Speech acts",
    'Q2.1': "Speech etc: Communicative",
    'Q2.2': "Speech acts",
    'Q3': "Language, speech and grammar",
    'Q4': "The Media",
    'Q4.1': "The Media: Books",
    'Q4.2': "The Media: Newspapers etc.",
    'Q4.3': "The Media: TV, Radio & Cinema",

    # S: SOCIAL ACTIONS, STATES AND PROCESSES
    'S': "Social actions, states and processes",
    'S1': "Social actions, states & processes",
    'S1.1': "Social actions, states & processes",
    'S1.1.1': "General",
    'S1.1.2': "Reciprocity",
    'S1.1.3': "Participation",
    'S1.1.4': "Deserve etc.",
    'S1.2': "Personality traits",
    'S1.2.1': "Approachability and Friendliness",
    'S1.2.2': "Avarice",
    'S1.2.3': "Egoism",
    'S1.2.4': "Politeness",
    'S1.2.5': "T oughness; strong/weak",
    'S1.2.6': "Sensible",
    'S2': "People",
    'S2.1': "People: Female",
    'S2.2': "People: Male",
    'S3': "Relationship",
    'S3.1': "Relationship: General",
    'S3.2': "Relationship: Intimate/sexual",
    'S4': "Kin",
    'S5': "Groups and affiliation",
    'S6': "Obligation and necessity",
    'S7': "Power relationship",
    'S7.1': "Power, organizing",
    'S7.2': "Respect",
    'S7.3': "Competition",
    'S7.4': "Permission",
    'S8': "Helping/hindering",
    'S9': "Religion and the supernatural",

    # T: TIME
    'T': "Time",
    'T1': "Time",
    'T1.1': "Time: General",
    'T1.1.1': "Time: General: Past",
    'T1.1.2': "Time: General: Present; simultaneous",
    'T1.1.3': "Time: General: Future",
    'T1.2': "Time: Momentary",
    'T1.3': "Time: Period",
    'T2': "Time: Beginning and ending",
    'T3': "Time: Old, new and young; age",
    'T4': "Time: Early/late",

    # W: THE WORLD AND OUR ENVIRONMENT
    'W': "The world and our environment",
    'W1': "The universe",
    'W2': "Light",
    'W3': "Geographical terms",
    'W4': "Weather",
    'W5': "Green issues",

    # X: PSYCHOLOGICAL ACTIONS, STATES AND PROCESSES
    'X': "Psychological actions, states and processes",
    'X1': "General",
    'X2': "Mental actions and processes",
    'X2.1': "Thought, belief",
    'X2.2': "Knowledge",
    'X2.3': "Learn",
    'X2.4': "Investigate, examine, test, search",
    'X2.5': "Understand",
    'X2.6': "Expect",
    'X3': "Sensory",
    'X3.1': "Sensory: T aste",
    'X3.2': "Sensory: Sound",
    'X3.3': "Sensory: T ouch",
    'X3.4': "Sensory: Sight",
    'X3.5': "Sensory: Smell",
    'X4': "Mental object",
    'X4.1': "Mental object: Conceptual object",
    'X4.2': "Mental object: Means, method",
    'X5': "Attention",
    'X5.1': "Attention",
    'X5.2': "Interest/boredom/excited/energetic",
    'X6': "Deciding",
    'X7': "Wanting; planning; choosing",
    'X8': "Trying",
    'X9': "Ability",
    'X9.1': "Ability: Ability, intelligence",
    'X9.2': "Ability: Success and failure",

    # Y: SCIENCE AND TECHNOLOGY
    'Y': "Science and technology",
    'Y1': "Science and technology in general",
    'Y2': "Information technology and computing",

    # Z: NAMES AND GRAMMATICAL WORDS
    'Z': "Names and grammatical words",
    'Z0': "Unmatched proper noun",
    'Z1': "Personal names",
    'Z2': "Geographical names",
    'Z3': "Other proper names",
    'Z4': "Discourse Bin",
    'Z5': "Grammatical",  # Original 'Grammatical bin'
    'Z6': "Negative",
    'Z7': "If",
    'Z8': "Pronouns etc.",
    'Z9': "Other",  # Original 'Trash can'
    'Z99': "Unmatched",
}

EXTRA_CHARS = {
    '%': "Rarity marker (1)",
    '@': "Rarity marker (2)",
    'f': "Female",
    'm': "Male",
    'n': "Neuter",
    'c': "Potential antecedents of conceptual anaphors (neutral for number)",
    'i': "Indicates a semantic idiom",
}


class TagComparison(Enum):
    """
    This class represents the different degrees of similarity between two tags
    """
    UNEQUAL       = 0  # All components are unequal
    SAME_FIELD    = 1  # Top-level field is the same
    SAME_1L_DIV   = 2 # First subdivision is the same
    SUB_CATEGORY  = 3  # One is a sub-category of the other
    SAME_CATEGORY = 4  # Category is equal (but symbols are not)
    EQUAL         = 5  # All components are equal


TAG_COMP_VALUES = {
    TagComparison.UNEQUAL:       0.0,
    TagComparison.SAME_FIELD:    0.4,
    TagComparison.SAME_1L_DIV:   0.6,
    TagComparison.SUB_CATEGORY:  0.7,
    TagComparison.SAME_CATEGORY: 0.8,
    TagComparison.EQUAL:         1.0,
}


class Tag:
    """
    A simple tag (i.e. not a compound one)
    """

    TAG_REGEX = re.compile("([ABCEFGHIKLMNOPQSTWXYZ])([0-9.]+)([%@fmnci]*)(\\+{0,3}\\-{0,3})")

    def __init__(self, tag_str: str):
        self.tag_str = tag_str.strip()

        match_res = self.TAG_REGEX.search(self.tag_str)
        if match_res is None:
            raise TypeError("'%s' is an invalid Tag value" % tag_str)

        self.field = match_res.group(1)

        self.subdivisions_str = match_res.group(2)
        self.subdivisions = self.subdivisions_str.split(".")

        symbols_str = match_res.group(3)
        self.symbols = set([c for c in symbols_str])
        plusminus_str = match_res.group(4)
        if plusminus_str != "":
            self.symbols.add(plusminus_str)
        self.symbols_str = symbols_str + plusminus_str

    def __str__(self) -> str:
        return self.tag_str

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, str(self))

    @property
    def category(self) -> str:
        return "%s%s" % (self.field, self.subdivisions_str)

    @property
    def field_description(self) -> str:
        return DESCRIPTIONS[self.field]

    @property
    def category_description(self) -> str:
        return DESCRIPTIONS[self.category]

    def __eq__(self, other: 'Tag') -> bool:
        return (self.field, self.subdivisions, self.symbols) == \
            (other.field, other.subdivisions, other.symbols)

    def compare(self, other: 'Tag') -> TagComparison:
        """
        Compare this tag with another
        Returns: a TagComparison object (enum)
        """
        # If either of them is Z99 then they are unequal
        if (self.tag_str == "Z99") or (other.tag_str == "Z99"):
            return TagComparison.UNEQUAL

        # if everything matches, EQUAL
        if self == other:
            return TagComparison.EQUAL

        if self.category == other.category:
            # Category is equal (but symbols are not)
            return TagComparison.SAME_CATEGORY

        if self.field == other.field:
            # Fields are the same, but how similar are the subdivisions?
            # if top-level subdivision matches, 
            if self.subdivisions[0] == other.subdivisions[0]:
                # is 'self' a sub-category of 'other'?
                len_sds_self = len(self.subdivisions)
                len_sds_other = len(other.subdivisions)
                if (len_sds_other >= len_sds_self) and (other.subdivisions[:len_sds_self] == self.subdivisions):
                    return TagComparison.SUB_CATEGORY

                # The tags are of the same top-level subdivision
                return TagComparison.SAME_1L_DIV

            return TagComparison.SAME_FIELD

        # at this point, we know the field is different, so they're UNEQUAL
        return TagComparison.UNEQUAL
    
    def match(self, other: 'Tag') -> float:
        """
        Compare this Tag with another and return a match value
        Returns a match value (0.0 -> 1.0).
        """
        return TAG_COMP_VALUES[self.compare(other)]


class CompoundTag:
    """
    A compound tag is one with multiple tags separated by forward slashes.
    This indicates membership of multiple categories
    """

    def __init__(self, cmp_tag_str: str):
        self.cmp_tag_str = cmp_tag_str.strip()
        self.tags = [Tag(tag) for tag in self.cmp_tag_str.split("/")]

    def __str__(self) -> str:
        return self.cmp_tag_str

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__, str(self))

    @property
    def description(self) -> str:
        """
        A compound description using USAS categories
        NOTE: This is just the category descriptions, it doesn't include modifying symbols.
        """
        return " / ".join([t.category_description for t in self.tags])

    @property
    def num_tags(self) -> int:
        return len(self.tags)

    def match(self, other: 'CompoundTag') -> float:
        """
        Compare this CompoundTag with another and return a match value.
        Returns a match value (0.0 -> 1.0).
        """
        non_zero_matches = []
        self_match_map = [0 for _ in self.tags]
        other_match_map = [0 for _ in other.tags]

        for si, stag in enumerate(self.tags):
            for oi, otag in enumerate(other.tags):
                ctag_match_value = stag.match(otag)
                if ctag_match_value > 0.0:
                    non_zero_matches.append(ctag_match_value)
                    self_match_map[si] = 1
                    other_match_map[oi] = 1

        if len(non_zero_matches) > 0:
            non_zero_match_avg = sum(non_zero_matches) / len(non_zero_matches)
            pc_self_matches = sum(self_match_map) / len(self_match_map)
            pc_other_matches = sum(other_match_map) / len(other_match_map)
            return non_zero_match_avg * pc_self_matches * pc_other_matches
        else:
            return 0.0


class MultiSenseTag:
    """
    A 'tag' sting that has multiple possible matches, separated by spaces.
    This indicates that there are multiple possible 'matches' for a particular token.
    This is probably because there are multiple possible 'senses' for the token, but that may not always be the case.
    'MultiSenseTag' isn't the best name for this, but it'll do.
    """

    def __init__(self, ms_tag_str: str):
        self.ms_tag_str = ms_tag_str.strip()
        senses = [s for s in re.split(" |,", ms_tag_str) if s != ""]  # Make sure there are no extra spaces
        self.senses = [CompoundTag(ct) for ct in senses]  # each 'sense' is treated as a compound tag

    def __str__(self) -> str:
        return self.ms_tag_str

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__, str(self))

    @property
    def num_senses(self):
        return len(self.senses)

    def match(self, ctag: CompoundTag) -> float:
        """
        Compare this tag against an 'expected' CompoundTag and return the match value.
        Returns a match value (0.0 -> 1.0).
        """
        POSITION_WEIGHT = 0.7
        NUM_SENSES_WEIGHT = 0.3

        match_values = []
        num_senses = len(self.senses)

        for i, self_ctag in enumerate(self.senses):
            mv = self_ctag.match(ctag)
            if mv > 0.0:
                position = i + 1
                multiplier = (POSITION_WEIGHT / position) + (NUM_SENSES_WEIGHT / num_senses)
                match_values.append(mv * multiplier)

        num_match_values = len(match_values)
        if num_match_values == 0:
            return 0.0
        else:
            return sum(match_values) / num_match_values