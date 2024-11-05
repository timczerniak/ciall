import sys
import argparse
import yaml

from ciall import pipeline
from ciall.utils import tsv
from ciall.utils import cg3


def main(args, conf):
    # Gather the input
    instr = ""
    if args.infile is None:
        instr = "\n".join([line for line in sys.stdin])
    else:
        with open(args.infile, "r") as fin:
            instr = fin.read()
    if instr == "":
        print("No input data!")
        return 1

    # Make the pipeline
    nlp = pipeline.make_pipeline(conf, accuracy=args.accuracy)

    # Make the Doc object from the input
    if isinstance(conf.get('input'), dict) and (conf['input'].get('format') == "tsv"):
        # if input format is tsv parse it into a doc first
        infields = conf['input'].get('fields', None)
        if infields:
            fields = infields.split("|")
        else:
            fields = []
        doc = tsv.doc_from_tsv(nlp, instr, fields=fields)
    elif isinstance(conf.get('input'), dict) and (conf['input'].get('format') == "cg3"):
        doc = cg3.doc_from_cg3(nlp, instr)

    if args.accuracy:
        # TODO!!!
        pass
    else:
        # Run the pipeline
        doc = nlp(doc)

        # Make the output stream
        if args.outfile is None:
            outstr = sys.stdout
        else:
            outstr = open(args.outfile, "w")

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

    # Print coverage information
    if args.coverage:
        num_tokens = 0
        num_z99 = 0
        for token in doc:
            if token._.pymusas_tags == None:
                continue
            num_tokens += 1
            if token._.pymusas_tags[0] == "Z99":
                num_z99 += 1
        num_matched = num_tokens - num_z99
        pc_matched = round((num_matched / num_tokens) * 100.0, 3)
        print(f"Total tokens: {num_tokens}")
        print(f"Num tokens matched: {num_matched}")
        print(f"Percentage tokens matched: {pc_matched}%")

    return 0


def parse_args_conf():
    parser = argparse.ArgumentParser(prog='ciall',
                                     description='The Irish semantic tagging pipeline')
    parser.add_argument('-c', '--config',
                        default="ciall_conf.yaml",
                        help="The configuration file to use.")
    parser.add_argument('-i', '--infile',
                        default=None,
                        help="The input file to process. " \
                             "If unspecified, STDIN is used.")
    parser.add_argument('-o', '--outfile',
                        default=None,
                        help="The destination file for output. " \
                             "If unspecified, STDOUT is used.")
    parser.add_argument('-C', '--coverage',
                        action='store_true',
                        default=False,
                        help="Print semantic tagging coverage information. " \
                             "If specified, the output itself is not printed.")
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