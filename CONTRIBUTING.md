# Contributing

Herein are notes for developing the `ciall` library.

## Using Docker

To avoid having to manage requirements manually on your local machine
it is useful to run the pipeline via Docker. For this, the only requirements are:

* [Docker](https://www.docker.com), installed using the packages on the website.
* [`make`](https://www.gnu.org/software/make/) which can usually be installed using apt,
  brew or another package manager.

All other dependencies are automatically built into the Docker image.

All instructions below assume that Docker is running.

## Running Unit Tests

If running with dependencies installed locally, run unit tests like so

```bash
$ make test
```

If running via Docker, run tests like so

```bash
$ make dockertest
```

## Running the Commandline Tool

To run the tool, it is easiest to drop into a docker shell like so:

```bash
$ make dockershell
```

Then from within the docker container, you can run the tool as normal:

```bash
\# cat input.tsv | python3 -m ciall.cmd --conf=ciall_conf.yaml
```

## Contributing Changes or Fixes

If you want to contribute, please contact me first. All changes should be reviewed using GitHub Pull Requests.