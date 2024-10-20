import os
import csv

# LEMMA_FREQ is a dictionary of lemma(string) -> frequency(integer)
LEMMA_FREQ = {}
with open(os.path.dirname(os.path.abspath(__file__)) + "/lemmafreq.csv") as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        LEMMA_FREQ[row[0]] = int(row[1])

def lemmafreq(lemma):
    """
    returns the relative frequency of the given lemma, or 0 if the lemma is unrecognised
    """
    return LEMMA_FREQ.get(lemma, 0)