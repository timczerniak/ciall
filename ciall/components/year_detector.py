import spacy
from spacy.language import Language


TIME_PERIOD_USAS_TAG = "T1.3"


# Year detector
@Language.component("ciall_year_detector")
def year_detector_function(doc):
    """
    This component depends on the ciall_musas_tagger being in the pipeline before it
    """

    for token in doc:
        pos_is_number = (token._.par_short[0] == 'M') if token._.par_short else False
        token_is_numeric = str(token.text).isnumeric()
        
        if pos_is_number and token_is_numeric:
            token_int = int(token.text)

            if (token_int >= 1000) and (token_int <= 2100):
                # token is an integer between 1000 and 2100, it's probably a year
                # Add the time period USAS tag as the most likely tag
                #print("year detected %s" % token.text)
                if token._.musas_tags is None:
                    token._.musas_tags = []
                token._.musas_tags = [TIME_PERIOD_USAS_TAG] + token._.musas_tags

    return doc