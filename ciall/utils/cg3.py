import sys, os
from dataclasses import dataclass, field

import spacy

from ciall.utils.pos2par import pos2par
from ciall.utils.lemmafreq import lemmafreq


@dataclass
class CG3Match:
    # Lemma
    lemma: str
    # Morphological feature tags (POS)
    morph_tags: list[str] = field(default_factory=list)
    # PAROLE tag
    par_tag_long: str = None
    par_tag_short: str = None
    # Universal dependency POS tag
    udep_tag: str = None
    # Dependency tags
    dep_tags: list[str] = field(default_factory=list)


@dataclass
class CG3Entry:
    token: str
    matches: list[CG3Match] = field(default_factory=list)


class CG3Document(object):

    def __init__(self):
        self.tokens = []

    def length(self):
        return len(self.tokens)

    @classmethod
    def from_stream(cls, stream):
        """
        `stream` is a file object (sys.stdin can be used too)
        """
        return cls.from_lines(stream)

    @classmethod
    def from_string(cls, s):
        """
        `s` is a string
        """
        return cls.from_lines(s.split("\n"))

    @classmethod
    def from_lines(cls, lines):
        # Format of cg3 file is:
        #
        # "<TOKEN>"\n
        # \t"LEMMA1" TAG11 TAG12 TAG13...
        # \t"LEMMA2" TAG21 TAG22 TAG23...
        #
        # Each line with lemma and tags is a possible match

        doc = cls()

        curr_token = None
        found_new_token = False

        for line in lines:

            if line.strip() == "":
                continue

            if line[0] == '"':
                ## Entry head line
                if found_new_token:
                    print(f"Found an entry head line, but we're already inside an entry!\n{line}", file=sys.stderr)
                    continue

                # Expected format is "<TOKEN>"\n
                # We just want TOKEN
                curr_token = line.strip('\n')  # First strip any trailing newlines
                curr_token = curr_token[2:-2]  # Take off the initial "< and final >"
                found_new_token = True

            if line[0] == '\t':
                ## Tags line
                entry_words = line.strip().split()
                lemma = entry_words[0].strip('"')
                tags = entry_words[1:]
                
                morph_tags = []
                dep_tags = []
                for tag in tags:
                    if tag.startswith('@') or tag.startswith('#') or tag.startswith('^'):
                        dep_tags.append(tag)
                    else:
                        morph_tags.append(tag)

                # convert tags from a list of POS tags into a single PAROLE tag, using pos2par()
                l_par_tag, s_par_tag, udep_tag = pos2par(morph_tags)

                # create the Match object
                match = CG3Match(lemma=lemma,
                                 morph_tags=morph_tags,
                                 par_tag_long=l_par_tag,
                                 par_tag_short=s_par_tag,
                                 udep_tag=udep_tag,
                                 dep_tags=dep_tags)
                if found_new_token:
                    # This is the first lemma line for this token
                    doc.tokens.append(CG3Entry(token=curr_token, matches=[match]))
                else:
                    # This is a subsequent lemma line for this token
                    doc.tokens[-1].matches.append(match)
                
                found_new_token = False

        return doc

    def reorder_by_lemma_freq(self):
        """
        This re-orders matches by the lemma frequency
        """
        for i in range(0, len(self.tokens)):
            # If there's more than one lemma
            if len(set([m.lemma for m in self.tokens[i].matches])) > 1:
                # CG3Entry and CG3Match are immutable (they are NamedTuples)
                self.tokens[i].matches = sorted(self.tokens[i].matches, key=lambda m: lemmafreq(m.lemma), reverse=True)


def doc_from_cg3(nlp: spacy.language.Language, cg3: str):
    cg3doc = CG3Document.from_string(cg3)
    cg3doc.reorder_by_lemma_freq()

    # Create the Doc object
    words = []
    spaces = []
    for token in cg3doc.tokens:
        words.append(token.token)
        spaces.append(True)  # TODO: something more intelligent?
    doc = spacy.tokens.doc.Doc(vocab=nlp.vocab, words=words, spaces=spaces)

    # update the attributes of the doc object with cg3 information
    for i in range(len(doc)):
        # Firstly, add all matches from the irishfst pipeline
        doc[i]._.ifst_matches = cg3doc.tokens[i].matches
        # Lemmatizer
        doc[i].lemma_ = doc[i]._.ifst_matches[0].lemma
        # POS tagger
        doc[i].pos_ = doc[i]._.ifst_matches[0].udep_tag
        doc[i]._.par_long = doc[i]._.ifst_matches[0].par_tag_long
        doc[i]._.par_short = doc[i]._.ifst_matches[0].par_tag_short
        doc[i]._.morph_tags = doc[i]._.ifst_matches[0].morph_tags
        doc[i]._.dep_tags = doc[i]._.ifst_matches[0].dep_tags

    return doc