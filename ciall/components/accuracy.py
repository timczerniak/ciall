import spacy

from spacy.tokens import Token, Doc
from spacy.language import Language


Token.set_extension("expected_musas_tags", default=None)
Doc.set_extension("accuracy_report", default=None)

# Accuracy reporter
@Language.component("ciall_accuracy")
def accuracy_function(doc):
    return doc