from collections import defaultdict

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from ciall.utils.musas_tags import CompoundTag


# Extensions to the spacy Token class
Doc.set_extension("musas_field_stats", default={})
# def musas_field_stats_str(token):
#     if token._.musas_field_stats is None:
#         ret_str = None
#     else:
#         ret_str = str(token._.musas_field_stats)
#     return ret_str
# Doc.set_extension("musas_field_stats_str", method=musas_field_stats_str)


# Document-level disambiguation
@Language.component("ciall_doc_tags")
def doc_tags_function(doc):
    """
    This component depends on the ciall_musas_tagger being in the pipeline before it
    """

    fields = defaultdict(lambda: 0)

    ## First pass
    # Find all tokens that have a definite (single) tag,
    # and calculate the number for each USAS 'field'
    for token in doc:
        if token._.musas_tags and len(token._.musas_tags) == 1:
            ct = CompoundTag(token._.musas_tags[0])
            if len(ct.tags) == 1:
                t = ct.tags[0]
                #print(token._.musas_tags[0], t.field)
                if t.field != 'Z':
                    fields[t.field] += 1
    # Save it in the musas_field_stats doc extension
    for k, v in fields.items():
        doc._.musas_field_stats[k] = v

    # Sort the most common fields by frequency
    sorted_fields = sorted(list(doc._.musas_field_stats.keys()),
                           key=lambda x:doc._.musas_field_stats[x],
                           reverse=True)
    # print(doc._.musas_field_stats)
    # print("Most common fields", sorted_fields)

    ## Second pass
    # Re-order ambiguous tags by doc-level frequency
    for token in doc:
        if token._.musas_tags and len(token._.musas_tags) > 1:
            curr_tags = token._.musas_tags
            def sortfunc(compound_tag):
                if compound_tag == '':
                    return -1000
                ct = CompoundTag(compound_tag)
                fs = [t.field for t in ct.tags]
                fstats = [doc._.musas_field_stats[f] for f in fs if f in doc._.musas_field_stats]
                if len(fstats) > 0:
                    return max(fstats)
                else:
                    # in the case where a tag's field isn't common in the doc,
                    # just leave it in the original order
                    # this puts the original ordering below 0 on the sorting scale:
                    # [most common doc freq, less common doc freq, 0, first element in curr_tags, second element, etc.]
                    return (-1 - curr_tags.index(compound_tag))
            token._.musas_tags = sorted(curr_tags, key=sortfunc, reverse=True)
            # if curr_tags != token._.musas_tags:
            #     print("Re-ordered tags for %s from %s to %s" % (token.text, curr_tags, token._.musas_tags))

    return doc