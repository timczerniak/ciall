# ciall

`ciall` is a tool for adding semantic annotation to Irish texts.
*Ciall* is an Irish word that translates to English as *meaning* or *sense*.
It is roughly pronounced `[ki:l]`, similar to the English word *keel*.


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
The `fields` value can be ommitted from the config if the first line of the TSV file contains the field names like so:

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
  fields: ID|TOKEN|LEMMA|POS|PAROLE|MWE|USAS|USAS_DESCRIPTION
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