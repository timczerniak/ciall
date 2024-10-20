
# Universal dependency tags (https://universaldependencies.org/u/pos/)
#  ADJ: adjective
#  ADP: adposition
#  ADV: adverb
#  AUX: auxiliary
#  CCONJ: coordinating conjunction
#  DET: determiner
#  INTJ: interjection
#  NOUN: noun
#  NUM: numeral
#  PART: particle
#  PRON: pronoun
#  PROPN: proper noun
#  PUNCT: punctuation
#  SCONJ: subordinating conjunction
#  SYM: symbol
#  VERB: verb
#  X: other
#
# This is an attempt at a mapping from the first char of PAROLE tag to the Universal dependency tag
PAR_TO_UDT = {
    "N": "NOUN",
    "V": "VERB",
    "A": "ADJ",
    "P": "PRON",
    "D": "DET",
    "T": "DET",
    "S": "ADP",
    "M": "NUM",
    "U": "X",
    "X": "X", # need to account for foreign nouns etc.
    "R": "ADV",
    "C": "CCONJ", # what about "SCONJ"?
    "I": "INTJ",
    "F": "PUNCT",
    "Y": "X", # abbreviations are what?
    "W": "AUX", # copula is particle or verb?
    "Q": "PART",
}

# TODO: Make sure all of the rules here are obeyed:
# https://universaldependencies.org/ga/index.html
def pos2par(pos_tags, lemma=None):
    """
    This function is for converting the morphalogical tags as defined here:
        https://www.scss.tcd.ie/~uidhonne/morphtag.htm
    into PAROLE tags as defined here:
        https://www.scss.tcd.ie/~uidhonne/parole.htm
    
    Arguments:
        pos_tags ([str]): The list of morphological tags associated with the token
        lemma (str): The lemma of the token
        short (bool): If True, a short version of the tag will be returned
    
    Return:
        A tuple containing:
          - Long PAROLE tag (str)
          - Short PAROLE tag (str)
          - Universal dependency tag (str))
    """

    # Build the tag - this returns a list of characters
    par_long = _build_par_tag(pos_tags, lemma)

    # make the par_short tag
    par_short = shorten_par_tag(par_long)

    # Get the Universal Dependency tag
    udep = PAR_TO_UDT.get(par_long[0], "X")

    # Convert the PAROLE tag from a list of characters into a string,
    # and remove any trailing dashes
    par_long = "".join(par_long).rstrip("-")
    par_short = "".join(par_short).rstrip("-")
    
    # return the PAROLE tag
    # If short is True, we return shortened versions
    return par_long, par_short, udep


def shorten_par_tag(par_long):
    if par_long == '':
        return ''
    # Nouns, Verbs, Adjectives, Pronouns, Determiners, Articles, Adpositions, Numerals, Uniques, Other
    elif par_long[0] in ('N', 'V', 'A', 'P', 'D', 'T', 'S', 'M', 'U', 'X'):
        return par_long[:2]  # Shorten to 2 characters
    # Adverbs, Conjunctions, Interjections, Punctuation, Abbreviation, Copula, Particles
    elif par_long[0] in ('R', 'C', 'I', 'F', 'Y', 'W', 'Q'):
        return par_long[:1]  # Shorten to 1 character
    else:
        return par_long


def _build_par_tag(pos_tags, lemma=None):

    # Convert the list of POS tags into a set, for quick comparisons
    pos_tags = set(pos_tags)

    # Initialise the resultant PAROLE tag as a list of 9 dashes
    # This will be converted into a single string tag before return
    result = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

    ### Guessed analyses
    if ("Guess" in pos_tags) or ("GuessCmpd" in pos_tags):
        # We can't predict what this is, so we'll just use Unknown
        result[0] = 'X'
        result[1] = 'x'

    ### Foreign
    if "Foreign" in pos_tags:
        result[0] = 'X'
        result[1] = 'f'

        # English
        if "English" in pos_tags:
            result[2] = 'e'
            if "Noun" in pos_tags:
                # English Noun
                result[3] = 'n'
                if "Prop" in pos_tags:
                    # Proper Noun
                    result[4] = 'p'
                    if "Def" in pos_tags:
                        # Definite Proper Noun (e.g. 'The Bahamas')
                        result[5] = 'd'
            elif "Verb" in pos_tags:
                # English Verb
                result[3] = 'v'
            elif "Adj" in pos_tags:
                # English Adjective
                result[3] = 'a'
            elif "Pron" in pos_tags:
                # English Pronoun
                result[3] = 'p'
            elif "Det" in pos_tags:
                # English Determiner
                result[3] = 'd'
            elif "Adv" in pos_tags:
                # English Adverb
                result[3] = 'r'
            elif "Prep" in pos_tags:
                # English Preposition
                result[3] = 's'
            elif "Conj" in pos_tags:
                # English Conjunction
                result[3] = 'c'
            elif "Num" in pos_tags:
                # English Numeral
                result[3] = 'm'
        
        # Latin
        if "Latin" in pos_tags:
            result[2] = 'l'

    ### Noun
    elif "Noun" in pos_tags:
        result[0] = 'N'

        # Noun sub-class
        if "Verbal" in pos_tags:
            # Verbal
            result[1] = 'v'
        elif "Prop" in pos_tags:
            # Proper
            result[1] = 'p'
        elif "Subst" in pos_tags:
            # Substantiative
            result[1] = 's'
        else:
            # Common
            result[1] = 'c'

        # Noun Gender
        if "Masc" in pos_tags:
            # Masculine
            result[2] = 'm'
        elif "Fem" in pos_tags:
            # Feminine
            result[2] = 'f'
        
        # Noun Number
        if "Sg" in pos_tags:
            # Singular
            result[3] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[3] = 'p'
        
        # Noun Case
        if "Com" in pos_tags:
            # Common
            result[4] = 'c'
        elif "Gen" in pos_tags:
            # Genitive
            result[4] = 'g'
        elif "Voc" in pos_tags:
            # Vocative
            result[4] = 'v'
        elif "Dat" in pos_tags:
            # Dative
            result[4] = 'd'
        
        # Noun Contrast
        if "Emph" in pos_tags:
            # Emphatic
            result[6] = 'e'
        
        # Noun Derived
        if "NStem" in pos_tags:
            # De-nominal
            result[7] = 'n'
    
    ### Verb
    elif "Verb" in pos_tags:
        result[0] = 'V'

        # Main
        result[1] = 'm'

        # TODO: This was in the java version, but it's not in the parole tags definition
        #if lemma == "bí":
        #    # 'bí' could be an auxiliary verb
        #    result[1] = 't'
        
        # Verb Mood
        if "Ind" in pos_tags:
            # Indicative
            result[2] = 'i'
        elif "Subj" in pos_tags:
            # Subjunctive
            result[2] = 's'
        elif "Imper" in pos_tags:
            # Imperavie
            result[2] = 'm'
        elif "Cond" in pos_tags:
            # Conditional
            result[2] = 'c'

        # Verb Tense
        if "Pres" in pos_tags:
            # Present
            result[3] = 'p'
        elif "Past" in pos_tags:
            # Past
            result[3] = 's'
        elif "Fut" in pos_tags:
            # Future
            result[3] = 'f'
        elif "PastImp" in pos_tags:
            # Indicative Past Imperfect/Habitual
            result[2] = 'i'
            result[3] = 'h'
        elif "FutInd" in pos_tags:
            # Indicative Future
            result[2] = 'i'
            result[3] = 'f'
        elif "PresImp" in pos_tags:
            # Indicative Present Habitual
            result[2] = 'i'
            result[3] = 'g'
        elif "PastInd" in pos_tags:
            # Indicative Past
            result[2] = 'i'
            result[3] = 's'
        elif "PastIndDep" in pos_tags:
            # Indicative Past Dependent
            result[2] = 'i'
            result[3] = 's'
            result[7] = 'd'
        elif "PresInd" in pos_tags:
            # Indicative Present
            result[2] = 'i'
            result[3] = 'p'
        elif "PresSubj" in pos_tags:
            # Subjunctive Present
            result[2] = 's'
            result[3] = 'p'
        elif "PastSubj" in pos_tags:
            # Subjunctive Past
            result[2] = 's'
            result[3] = 's'
        elif "Imper" in pos_tags:
            # Imperative
            result[2] = 'm'
            result[3] = 'p'
        
        # Verb Person
        if "1P" in pos_tags:
            # First Person
            result[4] = '1'
        elif "2P" in pos_tags:
            # Second Person
            result[4] = '2'
        elif "3P" in pos_tags:
            # Third Person
            result[4] = '3'
        elif "Auto" in pos_tags:
            # Autonomous form
            result[4] = '0'
        
        # Verb Number
        if "Sg" in pos_tags:
            # Singular
            result[5] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[5] = 'p'
        
        # Verb Dependency
        if "Dep" in pos_tags:
            # Dependent
            result[7] = 'd'
        elif "Rel" in pos_tags:
            # Relative
            result[7] = 'r'
        elif "Neg" in pos_tags:
            # Negative
            result[7] = 'n'
        
        # Verb Contrast
        if "Emph" in pos_tags:
            # Emphatic
            result[8] = 'e'

    ### Adjective
    elif "Adj" in pos_tags:
        result[0] = 'A'

        # Adjective Type
        if "Verbal" in pos_tags:
            # Verbal Adjective
            result[1] = 'v'
        else:
            # Qualificator
            result[1] = 'q'
        
        # Adjective Degree
        if "Comp" in pos_tags:
            # Comparative
            result[2] = 'c'
        #elif "Base" in pos_tags:
        else: # TODO: Is this the default???
            # Positive
            result[2] = 'p'
        
        # Adjective Gender
        if "Masc" in pos_tags:
            # Masculine
            result[3] = 'm'
        elif "Fem" in pos_tags:
            # Feminine
            result[3] = 'f'
        
        # Adjective Number
        if "Sg" in pos_tags:
            # Singular
            result[4] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[4] = 'p'
        
        # Adjective Case
        if "Com" in pos_tags:
            # Common
            result[5] = 'c'
        elif "Gen" in pos_tags:
            # Genitive
            result[5] = 'g'
        elif "Voc" in pos_tags:
            # Vocative
            result[5] = 'v'
        
        # Adjective Contrast
        if "Emph" in pos_tags:
            # Emphatic
            result[6] = 'e'
    
    ### Pronoun
    elif "Pron" in pos_tags:
        result[0] = 'P'

        # Pronoun Type
        if "Pers" in pos_tags:
            # Personal
            result[1] = 'p'
        elif "Ref" in pos_tags:
            # Reflexive
            result[1] = 'x'
        elif "Idf" in pos_tags:
            # Indefinite
            result[1] = 'i'
        elif "Prep" in pos_tags:
            # Prepositional
            result[1] = 'r'
        elif "Dem" in pos_tags:
            # Demonstrative
            result[1] = 'd'
        elif "Q" in pos_tags:
            # Interrogative
            result[1] = 'q'
        
        # Pronoun Person
        if "1P" in pos_tags:
            # First Person
            result[2] = '1'
        elif "2P" in pos_tags:
            # Second Person
            result[2] = '2'
        elif "3P" in pos_tags:
            # Third Person
            result[2] = '3'

        # Pronoun Gender
        if "Masc" in pos_tags:
            # Masculine
            result[3] = 'm'
        elif "Fem" in pos_tags:
            # Feminine
            result[3] = 'f'

        # Pronoun Number
        if "Sg" in pos_tags:
            # Singular
            result[4] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[4] = 'p'

        # Pronoun Case
        # TODO: Is this used anymore? What about other cases?
        if ("VerbSubj" in pos_tags) or ("Sbj" in pos_tags):
            # Nominative/Accusative (Common) Case
            result[5] = 'n'
        
        # Pronoun Contrast
        if "Emph" in pos_tags:
            # Emphatic
            result[6] = 'e'
    
    ### Determiner
    elif "Det" in pos_tags:
        result[0] = 'D'

        # Determiner Type
        if "Dem" in pos_tags:
            # Demonstrative
            result[1] = 'd'
        elif "Poss" in pos_tags:
            # Possessive
            result[1] = 'p'
        elif "Qty" in pos_tags:
            # Quantifier
            result[1] = 'q'
        elif "Q" in pos_tags:
            # Interrogative
            # TODO: This might be obsolete
            result[1] = 'w'
        
        # Determiner Person
        if "1P" in pos_tags:
            # First Person
            result[2] = '1'
        elif "2P" in pos_tags:
            # Second Person
            result[2] = '2'
        elif "3P" in pos_tags:
            # Third Person
            result[2] = '3'
        
        # Determiner Gender
        if "Masc" in pos_tags:
            # Masculine
            result[3] = 'm'
        elif "Fem" in pos_tags:
            # Feminine
            result[3] = 'f'
        
        # Determiner Number
        if "Sg" in pos_tags:
            # Singular
            result[4] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[4] = 'p'
    
    ### Copula
    elif "Cop" in pos_tags:
        result[0] = 'W'

        # Copula Tense/Mood
        if "Pres" in pos_tags:
            # Present Indicative
            result[1] = 'p'
            result[3] = 'i'
        elif "Past" in pos_tags:
            # Past Indicative
            result[1] = 's'
            result[3] = 'i'
        elif "Cond" in pos_tags:
            # Conditional
            result[1] = 's'
        elif "PresSubj" in pos_tags:
            # Present Subjunctive
            result[1] = 'p'
            result[3] = 's'
        
        # Copula Clause Type
        if "Rel" in pos_tags:
            # Relative Direct
            result[2] = 'r'
        elif "RelInd" in pos_tags:
            # Relative Indirect
            result[2] = 's'
        elif "Dep" in pos_tags:
            # Dependent
            result[2] = 'd'
        
        # Copula Person
        if "Pron" in pos_tags:
            # 3rd Person
            result[5] = '3'
        
        # Copula Negative/Question
        if "Neg" in pos_tags:
            # Negative
            result[4] = 'n'
        if "NegQ" in pos_tags:
            # Negative Question
            result[4] = 'n'
            result[3] = 'q'
        if "Q" in pos_tags:
            # Question
            result[3] = 'q'

    ### Adverb
    elif "Adv" in pos_tags:
        result[0] = 'R'

        # Adverb Type
        if "Gn" in pos_tags:
            # General
            result[1] = 'g'
        elif "Its" in pos_tags:
            # Intensifier
            result[1] = 'i'
        elif "Q" in pos_tags:
            # Interrogative
            result[1] = 'q'
        #elif "Rel" in pos_tags:
        #    # Relative? NOT USED
        #    # result[1] = 'r'
        elif "Temp" in pos_tags:
            # Temporal
            result[1] = 't'
        elif "Dir" in pos_tags:
            # Direction
            result[1] = 'd'
        elif "Loc" in pos_tags:
            # Locative
            result[1] = 'l'
    
    ### Adposition
    elif "Prep" in pos_tags:
        # Note: this comes after Pronouns because 'Prep' can be used for prepositional pronouns

        result[0] = 'S'

        # Preposition (this is always the case)
        result[1] = 'p'

        # Adposition Formation
        if "Cmpd" in pos_tags:
            # Compound
            result[2] = 'c'
        elif "Art" in pos_tags:
            # With Article
            result[2] = 'a'
        #elif "Inf" in pos_tags:
        #    # Infinitive NOT USED
        #    result[2] = 'i'
        elif "Deg" in pos_tags:
            # With Degree Part
            result[2] = 'd'
        elif "Poss" in pos_tags:
            # With Possessive Determiner
            result[2] = 'p'
        elif "Rel" in pos_tags:
            # With Relative Particle (e.g. in+a -> ina mbíonn)
            result[2] = 'r'
        elif "Obj" in pos_tags:
            # With Object Pronoun (e.g. de+a = á mbualadh)
            result[2] = 'o'
        
        # Article Number
        if "Sg" in pos_tags:
            # Singular
            result[4] = 's'
        if "Pl" in pos_tags:
            # Plural
            result[4] = 'p'

    ### Article
    elif "Art" in pos_tags:
        # Note: This comes after Prepositions because 'Art' can be used for prepositions with article

        result[0] = 'T'

        # Definite Article
        result[1] = 'd'

        # Article Gender
        if "Masc" in pos_tags:
            # Masculine
            result[2] = 'm'
        elif "Fem" in pos_tags:
            # Feminine
            result[2] = 'f'

        # Article Number
        if "Sg" in pos_tags:
            # Singular
            result[3] = 's'
        elif "Pl" in pos_tags:
            # Plural
            result[3] = 'p'

        # Article Case
        if "Gen" in pos_tags:
            # Genitive
            result[4] = 'g'
    
    ### Conjunction
    elif "Conj" in pos_tags:
        result[0] = 'C'

        # Conjunction Type
        if "Coord" in pos_tags:
            # Coordinate
            result[1] = 'c'
        elif "Subord" in pos_tags:
            # Subordinative
            result[1] = 's'
        
        # Conjunction CType
        if "Cop" in pos_tags:
            # With Copula
            result[2] = 'w'
        #elif "Rel" in pos_tags:
        #    # Relative? NOT USED
        #    result[2] = 'r'
        
        # Conjunction Coord-Pos
        if "Past" in pos_tags:
            # Past Tense
            result[3] = 's'
    
    ### Numeral
    elif "Num" in pos_tags:
        result[0] = 'M'

        # Numeral Type
        if "Card" in pos_tags:
            # Cardinal
            result[1] = 'c'
        elif "Ord" in pos_tags:
            # Ordinal
            result[1] = 'o'
        elif "Pers" in pos_tags:
            # Personal
            result[1] = 'p'
        elif "Dig" in pos_tags:
            # Numeral
            result[1] = 'n'
        elif "Rom" in pos_tags:
            # Roman
            result[1] = 'r'
        elif "Op" in pos_tags:
            # Operator
            result[1] = 's'
        
    ### Interjection
    elif "Itj" in pos_tags:
        result[0] = 'I'
    
    ### Verbal Particles
    elif ("Part" in pos_tags) and ("Vb" in pos_tags): # only verbal particles (non-verbal are Unique membership class, below)
        result[0] = 'Q'

        # Verbal Particle Negative/Interrogative
        if "NegQ" in pos_tags:
            # Negative type, Interrogative mood
            result[1] = 'n'
            result[2] = 'q'
        elif ("Neg" in pos_tags) and ("Q" in pos_tags):
            # Negative type, Interrogative mood
            result[1] = 'n'
            result[2] = 'q'
        elif "Neg" in pos_tags:
            # Negative type
            result[1] = 'n'
        elif "Q" in pos_tags:
            # Question type
            result[1] = 'q'
        
        # Verbal Particle Mood/Relative-ness
        if "Subj" in pos_tags:
            # Subjunctive mood
            result[2] = 's'
        elif "Imp" in pos_tags:
            # Imperative mood
            result[2] = 'm'
        elif ("Rel" in pos_tags) or ("Direct" in pos_tags):
            # Relative particle
            result[2] = 'r'
        elif "Indirect" in pos_tags:
            # Indirect relative particle
            result[2] = 'i'
        elif "Pro" in pos_tags:
            # Relative particle with pronoun
            result[2] = 'p'
        
        # Verbal Particle Tense
        if ("Past" in pos_tags) or ("PastIrreg" in pos_tags):
            result[3] = 's'
        
        # TODO: What is "Part Vb Cmpl"? i.e. what is Cmpl?
        # TODO: "Part Vb Cond" (i.e. 'má') not covered?

    ### Unique Membership Class
    elif ("Part" in pos_tags) and ("Vb" not in pos_tags): # particles except verbal ones
        result[0] = 'U'

        # Particle Type
        if "Cp" in pos_tags:
            # Copular Particle
            result[1] = 'w'
        elif "Ad" in pos_tags:
            # Adverbial Particle 'go'
            result[1] = 'a'
        elif "Deg" in pos_tags:
            # Degree Particle 'a'
            result[1] = 'd'
        elif "Voc" in pos_tags:
            # Vocative particle 'a'
            result[1] = 'v'
        elif "Nm" in pos_tags:
            # Numeral Particle 'a'
            result[1] = 'm'
        elif "Comp" in pos_tags:
            # Comparative Particle 'níos'
            result[1] = 'c'
        elif "Pat" in pos_tags:
            # Patronymic Particle 'Mac', 'ó', 'Uí', 'Ní' etc.
            result[1] = 'p'
        #elif "Sup" in pos_tags:
        #    # Superlative Particle 'is' NOT USED
        #    result[1] = 's'
        #elif "Inf" in pos_tags:
        #    # ??? Particle NOT USED
        #    result[1] = 'i'
    
    ### Punctuation
    elif "Punct" in pos_tags:
        result[0] = 'F'

        # Punctuation Type
        if "Fin" in pos_tags:
            # Sentence-Final
            result[1] = 'e'
        elif "Int" in pos_tags:
            # Sentence-Internal (comma, semicolon etc.)
            result[1] = 'i'
        elif "Quo" in pos_tags:
            # Quotation Marks
            result[1] = 'a'
        elif "Bar" in pos_tags:
            # Hyphen, Underscore
            result[1] = 'b'
        elif "Brack" in pos_tags:
            # Brackets (round and square)
            result[1] = 'p'
        elif "Curr" in pos_tags:
            # Currency symbol
            result[1] = 'c'
        
        if "Q" in pos_tags:
            # Question (this overwrites 'e' above)
            result[1] = 'q'
    
    ### Abbreviation
    elif "Abr" in pos_tags:
        result[0] = 'Y'
    
    ### Residuals
    # TODO: Tags without equivalent 
    #   Xa: acronym
    #   Xd: date
    #   Xn: number
    #   Xt: toponym
    #   Xy: symbol
    elif "Item" in pos_tags:
        # List Item
        result[0] = 'X'
        result[1] = 'l'
    elif "Email" in pos_tags:
        # Email Address
        result[0] = 'X'
        result[1] = 'e'
    elif "Web" in pos_tags:
        # Web Adress
        result[0] = 'X'
        result[1] = 'w'
    elif "Filler" in pos_tags:
        # Spoken filler
        result[0] = 'X'
        result[1] = 's'
        result[2] = 'f'
    elif ("Cmc" in pos_tags) and ("English" in pos_tags):
        # Spoken communicator - English
        result[0] = 'X'
        result[1] = 'l'
        result[2] = 'c'
        result[3] = 'e'
    elif "Event" in pos_tags:
        # Spoken event (cough, sneeze, laugh)
        result[0] = 'X'
        result[1] = 's'
        result[2] = 'e'
    elif "Fragment" in pos_tags:
        # Spoken phonetic fragment
        result[0] = 'X'
        result[1] = 's'
        result[2] = 'p'
    elif "Xxx" in pos_tags:
        # Indecipherable speech
        result[0] = 'X'
        result[1] = 's'
        result[2] = 'x'
    #elif "Disfluency" in pos_tags:
    #    # Disfluency (correction, repetition etc.) IS THIS USED?
    #    result[0] = 'X'
    #    result[1] = 's'
    #    result[2] = 'd'

    ### Unknown
    elif "?" in pos_tags:
        # Unknown
        result[0] = 'X'
        result[1] = 'x'
    
    ### Everything else is unknown
    else:
        # Unknown
        result[0] = 'X'
        result[1] = 'x'
    
    return result