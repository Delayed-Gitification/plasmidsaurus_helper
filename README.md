# plasmidsaurus_helper

A very simple convenience tool for identifying low-confidence bases and optionally also re-indexing (including reverse complementing) nanopore plasmid sequencing data, eg from Plasmidsaurus, Full Circle etc.

It outputs a fasta file where low confidence bases are converted to lower case, making them very easy to spot. 

Also, if the user provides the start sequence of their plasmid map, it automatically re-indexes/reverse complements (if necessary) the sequence so that it matches the map, making alignment easier.

## Installation: 

Install from pypi:

```pip install plasmidsaurus_helper```

## Usage

The only required input is the FASTQ (not FASTA!) file (option -i/--input). Optionally a list of fastqs can be provided (eg using * pattern matching).

Optionally, you can specify a custom output fasta name (option -o/--output). You cannot use this if providing a list of fastqs.

To provide the start sequence of your plasmid map, use option -s/--start_sequence (use a unique sequence, eg 10-20 nt)

By default, a phred score of 20 (1% error rate) is used as the threshold for changing bases to lower-case. But this can be altered with option -t/--low_confidence_threshold

eg run 

```plasmidsaurus_helper -i sequencing_results/*.fastq -s atcgcgcgaattcga```

This will automatically find all the fastq files in the your sequencing results folder and process them as described above

Happy cloning :)
