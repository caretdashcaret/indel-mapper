# Indel Mapper

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

## Set up

First, make sure the correct version of `virtualenv` is installed:

```shell
$ pip3 install virtualenv
```

Next, `cd` into your project and set up the `virtualenv` directory:

```shell
$ virtualenv --python=python3 .indel-mapper
```

Activate `virtualenv`. This adds the `indel-mapper/bin` directory to the start
of your `$PATH`.

```shell
$ source .indel-mapper/bin/activate
```

Install the required libraries:

```shell
$ pip3 install -r requirements.txt
```

## Run the tests:

```shell
$ python3 -m pytest
```

## Running the app

Example:

```shell
$ python3 indel-mapper.py -a ~/Documents/bowtie2_results.sam -r ~/Documents/references.csv -o ~/Documents/results.csv -m
```

There are three required arguments:

* `-a` or `--alignment` Alignment SAM file
* `-r` or `--reference` Reference CSV file
* `-o` or `--output` Output file, in CSV
* `-m` or `--metadata` Include a metadata JSON in the output generation, for visualization

## License

Indel Mapper is licensed under Version 3 of the GNU General Public License.
