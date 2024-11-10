import spacy
from spacy.tokens import Token, Doc
from spacy.language import Language

from ciall.utils.musas_tags import CompoundTag, MultiSenseTag


Token.set_extension("expected_musas_tag", default=None)
Doc.set_extension("accuracy_report", default=None)


class AccuracyReport(object):
    def __init__(self):
        # Initialise members that can then be 
        self.num_tokens = 0              # The total number of tokens in the doc
        self.num_z99 = 0                 # The number of tokens with no Semantic Tag matched (Z99: Unmatched)
        self.num_fully_correct = 0       # The number of tokens with fully correct MUSAS tags
        self.num_cont_fully_correct = 0  # The number of content word tokens with fully correct MUSAS tags
        self.all_match_values = []       # match values for all tokens
        self.cont_match_values = []      # match values for content words
    
    def add_token(self, par_short: str, pymusas_tags: list[str], expected_pymusas_tag: str):
        # Increment number of tokens
        self.num_tokens += 1

        # Is it unmatched?
        if pymusas_tags[0] == "Z99":
            self.num_z99 += 1

        # Calculate and save the MUSAS accuracy value
        mv = MultiSenseTag(" ".join(pymusas_tags)).match(CompoundTag(expected_pymusas_tag))
        self.all_match_values.append(mv)

        # Is it fully correct?
        if mv == 1.0:
            self.num_fully_correct += 1

        # If it's a content word, add info to content calculation
        if par_short[0] in ('N', 'V', 'A', 'R', 'M'):  # content words
            if mv == 1.0:
                self.num_cont_fully_correct += 1
            self.cont_match_values.append(mv)

    def calculate_totals(self):
        self.lexical_coverage = round(((self.num_tokens - self.num_z99) / self.num_tokens) * 100.0, 3)

        self.pc_all_fully_correct = round((self.num_fully_correct / self.num_tokens) * 100, 3)
        self.pc_cont_fully_correct = round((self.num_cont_fully_correct / len(self.cont_match_values)) * 100, 3)

        self.all_accuracy = sum(self.all_match_values) / len(self.all_match_values)
        self.pc_all_accuracy = round(self.all_accuracy * 100, 3)
        self.cont_accuracy = sum(self.cont_match_values) / len(self.cont_match_values)
        self.pc_cont_accuracy = round(self.cont_accuracy * 100, 3)

    @property
    def report_str(self):
        # printed results
        report_str = "### Results\n\n"
        report_str += "Num tokens: %s\n " % self.num_tokens
        report_str += "Lexical coverage: %s%%\n" % self.lexical_coverage
        report_str += "Fully correct MUSAS tags (all tokens): %s%% (%s tokens)" % \
                      (self.pc_all_fully_correct, self.num_fully_correct)
        report_str += "Fully correct MUSAS tags (content tokens): %s%% (%s tokens)" % \
                      (self.pc_cont_fully_correct, self.num_cont_fully_correct)
        report_str += "Overall semantic tag accuracy (all tokens): %s%%" % self.pc_all_accuracy
        report_str += "Overall semantic tag accuracy (content tokens): %s%%" % self.pc_cont_accuracy
        return report_str
    
    @classmethod
    def combine_reports(cls, reports: list[object]):
        combined_report = AccuracyReport()
        for report in reports:
            combined_report.num_tokens += report.num_tokens
            combined_report.num_z99 += report.num_z99
            combined_report.num_fully_correct += report.num_fully_correct
            combined_report.num_cont_fully_correct += report.num_cont_fully_correct
            combined_report.all_match_values.append(report.all_match_values)
            combined_report.cont_match_values.append(report.cont_match_values)
            combined_report.calculate()
        return combined_report


# Accuracy reporter
@Language.component("ciall_accuracy")
def accuracy_function(doc):
    # Create the report
    report = AccuracyReport()

    # Run through the doc adding all the tokens
    for token in doc:
        report.add_token(par_short=token._.par_short,
                         pymusas_tags=token._.pymusas_tags,
                         expected_pymusas_tag=token._.expected_pymusas_tag)

    # Calculate totals
    report.calculate_totals()

    # Add the report to the doc
    doc._.accuracy_report = report

    return doc