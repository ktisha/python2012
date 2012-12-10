from tools import *

RESULT_DIR = ''

DATA_DIR = 'Data'
GENOMES = {'ECO2_seq': 'Data/eco_genes.fasta',
                     'ECO3_seq': 'Data/eco_genes.fasta',
                     'ECO6_seq': 'Data/eco_genes.fasta',
                     'ECO7_seq': 'Data/eco_genes.fasta',
                     'MRU5_seq': 'Data/mru_genes.fasta',
                     'MRU6_seq': 'Data/mru_genes.fasta',
                     'MRU9_seq': 'Data/mru_genes.fasta',
                     'PHE4_seq': 'Data/phe_genes.fasta',
                     'PHE6_seq': 'Data/phe_genes.fasta',
                     'PHE7_seq': 'Data/phe_genes.fasta'}


GENE_FINDER_TOOLS = [GeneMarkCommonGC(DATA_DIR, 'genemark_suite_linux_64/gmsuite'),
                     GeneMarkEveryGC(DATA_DIR, 'genemark_suite_linux_64/gmsuite'),
                     GeneMarkHmmCommomGC(DATA_DIR, 'genemark_suite_linux_64/gmsuite'),
                     GeneMarkHmmEveryGC(DATA_DIR, 'genemark_suite_linux_64/gmsuite'),
                     GeneMarkS(DATA_DIR, 'genemark_suite_linux_64/gmsuite')]