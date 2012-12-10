```
 _____       ______  _____
|  __ \      |  ___|/  __ \
| |  \/  ___ | |_   | /  \/  ___   _ __ ___   _ __
| | __  / _ \|  _|  | |     / _ \ | '_ ` _ \ | '_ \
| |_\ \|  __/| |    | \__/\| (_) || | | | | || |_) |
 \____/ \___|\_|     \____/ \___/ |_| |_| |_|| .__/
                                             | |
                                             |_|

                       -- all your genes belong to us!
```

GeFComp is a Python script for comparing performance metrics of different gene
finding tools. Given a number of [genome assemblies] [ga-wiki] in FASTA format,
GeFComp executes each available tool on each of the genomes and evaluates
*Type I* and *Type II* errors, also known as false positives and false negatives.
Results are then summarised

Currently, GeFComp supports:

* [GeneMark] [gm]
* [GeneMark.hmm] [gm]
* [GeneMark-S] [gm]

[ga-wiki]: http://en.wikipedia.org/wiki/Genome_project#Genome_assembly
[ggplot2]: http://ggplot2.org
[gm]: http://exon.gatech.edu

## Installation

Python-only requirements can be installed via the usual `pip` boilerplate, but to do the
evaluation you also have to make sure that the following tools are available in `$PATH`:

* [BWA] [bwa], a popular short read aligner.

```bash
$ pip install -r requirements.txt
```

Or, if you prefer Debian and system-wide installation:

```bash
# aptitude install python-biopython bwa
```

[bwa]: http://bio-bwa.sourceforge.net

## Usage

```bash
$ gefcomp.py config.py
$ ls *.csv
summary.csv
```