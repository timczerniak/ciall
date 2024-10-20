from spacy.tokens import Token


# Extensions to the spacy Token class
Token.set_extension("ifst_matches", default=[])
Token.set_extension("morph_tags", default=[])
def morph_tags_str(token):
    if token._.morph_tags is None:
        tags_str = ""
    else:
        tags_str = ",".join(token._.morph_tags)
    return tags_str
Token.set_extension("morph_tags_str", method=morph_tags_str)
Token.set_extension("dep_tags", default=[])
def dep_tags_str(token):
    if token._.dep_tags is None:
        tags_str = ""
    else:
        tags_str = ",".join(token._.dep_tags)
    return tags_str
Token.set_extension("dep_tags_str", method=dep_tags_str)
Token.set_extension("par_long", default="")
Token.set_extension("par_short", default="")
Token.set_extension("parent", default=None)
Token.set_extension("deptree_tag", default="")