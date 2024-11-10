import sys
import os
import argparse
import yaml

from ciall import pipeline
from ciall.utils import tsv
from ciall.utils import cg3
from ciall.components.accuracy import AccuracyReport


def main(args, conf):
    # Gather the input
    instrs = []
    if args.infile is None:
        instr.append("\n".join([line for line in sys.stdin]))
    else:
        if os.path.isdir(args.infile):
            files = []
            for file in os.listdir(args.infile):
                dirpath = os.path.abspath(args.infile)
                files.append(os.path.join(dirpath,file))
        elif os.path.isfile(args.infile):
            files = [args.infile]
        else:
            print ("Input file doesn't exist: %s" % args.infile)
            return 1
        for file in files:
            with open(file, "r") as fin:
                instrs.append(fin.read())
    if (len(instrs) == 0) or (instrs[0] == ""):
        print("No input data!")
        return 1

    # For saving accuracy reports
    accuracy_reports = []

    # Make the pipeline
    nlp = pipeline.make_pipeline(conf, accuracy=args.accuracy)

    # Process each input string
    for instr in instrs:
        # Make the Doc object from the input
        if isinstance(conf.get('input'), dict) and (conf['input'].get('format') == "tsv"):
            # if input format is tsv parse it into a doc first
            infields = conf['input'].get('fields', None)
            if infields:
                fields = infields.split("|")
            else:
                fields = []
            doc = tsv.doc_from_tsv(nlp, instr, fields=fields, accuracy=args.accuracy)
        elif isinstance(conf.get('input'), dict) and (conf['input'].get('format') == "cg3"):
            doc = cg3.doc_from_cg3(nlp, instr)

        # Run the pipeline
        doc = nlp(doc)

        # Save the accuracy report
        if args.accuracy:
            accuracy_reports.append(doc._.accuracy_report)
        else: # Print the output
            # Make the output stream
            if args.outfile is None:
                outstr = sys.stdout
            else:
                # In the case of multiple input files, append mode ('a') means the outputs will all be in the same file
                outstr = open(args.outfile, "a")

            # Write the output
            if isinstance(conf.get('output'), dict) and conf['output'].get('fields') is not None:
                outfields = conf['output']['fields'].split("|")
            else:
                print("Must specify configuration value output.fields as a |-separated list of fields to output")
                return 1
            outstr.write(tsv.output_tsv(doc, outfields))

            # Close the output
            if args.outfile is not None:
                outstr.close()

    if args.accuracy:
        # Print the combined accuracy report
        combined_accuracy_report = AccuracyReport.combine_reports(accuracy_reports)
        print(combined_accuracy_report.report_str)

    return 0


# This is separate to make the main() function more testable
def parse_args_conf():
    parser = argparse.ArgumentParser(prog='ciall',
                                     description='The Irish semantic tagging pipeline')
    parser.add_argument('-c', '--config',
                        default="ciall_conf.yaml",
                        help="The configuration file to use.")
    parser.add_argument('-i', '--infile',
                        default=None,
                        help="The input file to process. " \
                             "If unspecified, STDIN is used. " \
                             "This can also be a folder containing multiple .tsv files to process.")
    parser.add_argument('-o', '--outfile',
                        default=None,
                        help="The destination file for output. " \
                             "If unspecified, STDOUT is used.")
    parser.add_argument('-A', '--accuracy',
                        action='store_true',
                        default=False,
                        help="Run accuracy tests using the input as a test file. " \
                             "This only works with TSV input. " \
                             "If specified, the output itself is not printed.")
    # TODO: Add this when we find a good way to do logging
    # parser.add_argument('-v', '--verbose', default=False, action='store_true',
    #                     help="When specified, log messages will be sent to STDOUT.")
    args = parser.parse_args()
    
    # Parse config
    with open(args.config, 'r') as conf_file:
        conf = yaml.safe_load(conf_file)

    return (args, conf)


if __name__ == "__main__":
    sys.exit(main(*parse_args_conf()))