# ciall

`ciall` is a tool for adding semantic annotation to Irish texts.
*Ciall* is an Irish word that translates to English as *meaning* or *sense*.
It is roughly pronounced `[ki:l]`, similar to the English word *keel*.


## Usage and Referencing

The licence for usage GPU, described in [LICENSE.txt](LICENSE.txt).
Additionally, if using this code, please acknowledge and reference the following publication:

```
Czerniak, T., & Uí Dhonnchadha, E. (2024). Towards Semantic Tagging for Irish. In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024) (pp. 16643-16652).
```


## Installing requirements

The pipeline requires:

* [`python3`](https://www.python.org)
* [`spacy`](https://spacy.io)
* [`pymusas`](https://ucrel.github.io/pymusas/)
* [`PyYAML`](https://pyyaml.org)

For Debian/Ubuntu, you can install requirements like so (note you may need to run these using `sudo`):

```
$ apt install python3.12
$ pip3 install -r requirements.txt
```


## Running the Pipeline

You can run the pipeline like so:

```bash
$ python3 -m ciall.cmd
```

To get information on arguments run:

```bash
$ python3 -m ciall.cmd --help
```

To run an example:

```bash
$ cat example/example_text.tsv | python3 -m ciall.cmd --conf=example/example_conf.yaml
```


## The Configuration File

The example configuration file in `example/example_conf.yaml` should serve as a good starting point.
This uses [YAML format](https://yaml.org).

The pipeline has several components, which need to be enabled and listed in a particular order.
These should not need to be changed from the example config:

```yaml
components:
  - ciall_musas_tagger    # The MUSAS tagger itself
  - ciall_doc_tags        # A component to refine tags based on document-level calculations
  - ciall_year_detector   # A component that detects numbers which are likely to be years
  - ciall_prop_nouns      # A component that refines tags on proper nouns
```

The `ciall_musas_tagger` component needs to be given a single-word lexicon file and a multi-word lexicon file.
These are configured as below. Just change the file paths to use your own lexicon files.
Absolute or relative paths can be used.

```yaml
ciall_musas_tagger:
  sw_lexicon: example/example_sw_lexicon.tsv
  mw_lexicon: example/example_mw_lexicon.tsv
```

Input format can be either tab-separated values (also known as vert files), or cg3 format.
To configure TSV, use the following.

```yaml
input:
  format: tsv
  fields: TOKEN|LEMMA|PAROLE
```

Note that the `fields` value is a list of fields separated by 'bar' (`|`) characters.
The `fields` value can be ommitted from the config if the first line of the TSV file contains the field names as below.
Note that if the `fields` value is set in the config and if there is also a heading line in the TSV files as below,
they must match.

```tsv
TOKEN   LEMMA   PAROLE
Níl     bí      Vmip
aon     aon     Dq
...
```

To configure input as cg3, use the following. No `fields` value is necessary since the cg3 format has these built in.

```yaml
input:
  format: cg3
```

Output format can only be TSV at present. The `fields` value must be specified to list the fields for the output.

```yaml
output:
  format: tsv
  fields: ID|TOKEN|LEMMA|UPOS|PAROLE|MWE|USAS|USAS_DESCRIPTION
```


## Input/Output Pipes & Files

Input can be piped in or read from a file, and output can be piped out or saved to a file:

To use pipes:

```bash
$ cat input.tsv | python3 -m ciall.cmd --conf=ciall_conf.yaml > output.tsv
```

To use files:

```bash
$ python3 -m ciall.cmd --conf=ciall_conf.yaml --infile=input.tsv --outfile=output.tsv
```

Combinations can also be used:

```bash
$ python3 -m ciall.cmd --conf=ciall_conf.yaml --infile=input.tsv > output.tsv
$ cat input.tsv | python3 -m ciall.cmd --conf=ciall_conf.yaml --outfile=output.tsv
```


## Running Accuracy Tests

To test the accuracy of the pipeline running with a given configuration against pre-tagged and checked texts,
run the pipeline with the `--accuracy` argument. This requires an input text which already has the `USAS` column.
The contents of this column will be used as the 'expected' output, compared with the output of the pipeline,
and scored accordingly.

To run the example accuracy test:

```bash
$ python3 -m ciall.cmd --accuracy --conf=example/example_conf.yaml --infile=example/example_accuracy_test.tsv
```

Also note that this can be run on a folder containing multiple input TSV files. This is necessary to calculate accuracy across a larger corpus.

```bash
$ python3 -m ciall.cmd --accuracy --conf=example/example_conf.yaml --infile=my_corpus_of_tsv_texts/
```

This will print a report containing the following values:
- **Num tokens** - The total number of tokens
- **Lexical coverage** - The number and percentage of tokens that were assigned a USAS tag by the pipeline (i.e. not `Z99`)
- **Fully correct MUSAS tags (all tokens)** - The number & percentage of tokens for which the pipeline assigned *exactly* the same USAS value that is in the `USAS` column in the input file.
- **Fully correct MUSAS tags (content tokens)** - Same as the value above but only counting content tokens (Nouns, Verbs, Adjectives, Adverbs & Numerals)
- **Overall semantic tag accuracy (all tokens)** - The overall semantic tag  accuracy calculation takes account for partial correctness, e.g. where the correct semantic tag is among the list of assigned tags (for details, see Czerniak & Uí Dhonnchadha (2024)
- **Overall semantic tag accuracy (content tokens)** - The overall semantic tag accuracy, calculated as described in Czerniak & Uí Dhonnchadha (2024), but only counting content words.