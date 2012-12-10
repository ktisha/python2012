# -*- coding: utf-8 -*-

from collections import namedtuple
import os
import subprocess
from tools import GeneMarkCommonGC, GeneMarkEveryGC, GeneMarkHmmCommomGC, GeneMarkHmmEveryGC, GeneMarkS


def make_sam_out(predict_path, genes_path, genome_name, data_dir, method_name):
    devnull = open(os.devnull, "w")
    subprocess.call(['bwa', 'index', '-a', 'bwtsw', predict_path],
        stdout=devnull, stderr=devnull)
    subprocess.call(['bwa', 'index', '-a', 'bwtsw', genes_path],
        stdout=devnull, stderr=devnull)
    out_path_prefix = os.path.join(data_dir, genome_name) + '_'
    with open(out_path_prefix + method_name + '_on.sam', 'w') as fout:
        subprocess.call(['bwa', 'bwasw', predict_path, genes_path],
            stdout=fout, stderr=devnull)
    with open(out_path_prefix + 'on_' + method_name + '.sam', 'w') as fout:
        subprocess.call(['bwa', 'bwasw', genes_path, predict_path],
            stdout=fout, stderr=devnull)
    return out_path_prefix

def get_sam_map(sam_path):
    res = {}
    qnames = set()
    with open(sam_path) as sam_file:
        for line in sam_file:
            if line.startswith('@'):
                pass
            else:
                sl = line.split()
                qname, rname, mapq = sl[0], sl[2], int(sl[4])
                qnames.add(qname)
                if mapq >= 200: #mapq = -10*log(10, Pr{mapp. pos. is wrong}), if mapq = 200, Pr{..} = 10**(-20)
                    res[qname] = rname
    return res, len(qnames)

def count_metrics(genes_sam_path, predict_sam_path):
    predict_on_genes, predict_count = get_sam_map(predict_sam_path)
    genes_on_predict, genes_count = get_sam_map(genes_sam_path)
    H = namedtuple('H', ['name', 'TP', 'FP', 'FN'])
    TP = len(predict_on_genes)
    H_predict_is_gene = H('predict is gene', TP, predict_count - TP,
        genes_count - len(set(predict_on_genes.values())))
    TP = len(genes_on_predict)
    H_gene_was_predicted = H('gene was predicted', TP, genes_count - TP,
        predict_count - len(set(genes_on_predict.values())))
    return H_predict_is_gene, H_gene_was_predicted

def compare_data(tools, genomes, data_dir):
    for genome_name, genes_path in genomes.iteritems():
        for tool in tools:
            path_result = tool.execute(genome_name)
            path_prefix = make_sam_out(path_result, genes_path, genome_name,
                data_dir, tool.name)
            hypothesises = count_metrics(path_prefix + tool.name + '_on.sam',
                path_prefix + 'on_' + tool.name + '.sam')
            for hypothesis in hypothesises:
                yield hypothesis.name, genome_name, tool.name, hypothesis.TP, \
                      hypothesis.FP, hypothesis.FN


if __name__ == "__main__":
    data_dir = 'Data'
    lib_dir = '/home/katya/CSC/python2012/katyasosa/gmsuite'
    genomes = {'ECO2_seq': 'Data/eco_genes.fasta'}
#        'ECO3_seq': 'Data/eco_genes.fasta',
#               'ECO6_seq': 'Data/eco_genes.fasta', 'ECO7_seq': 'Data/eco_genes.fasta',
#               'MRU5_seq': 'Data/mru_genes.fasta', 'MRU6_seq': 'Data/mru_genes.fasta',
#               'MRU9_seq': 'Data/mru_genes.fasta', 'PHE4_seq': 'Data/phe_genes.fasta',
#               'PHE6_seq': 'Data/phe_genes.fasta', 'PHE7_seq': 'Data/phe_genes.fasta'}
    gm_common_gc = GeneMarkCommonGC(data_dir, lib_dir)
    gm_every_gc = GeneMarkEveryGC(data_dir, lib_dir)
    gm_hmm_common_gc = GeneMarkHmmCommomGC(data_dir, lib_dir)
    gm_hmm_every_gc = GeneMarkHmmEveryGC(data_dir, lib_dir)
    gm_s = GeneMarkS(data_dir, lib_dir)
    tools = [gm_common_gc, gm_every_gc, gm_hmm_common_gc, gm_hmm_every_gc, gm_s]
    with open('compare_out', 'w') as out:
        for data in compare_data(tools, genomes, data_dir):
            out.write(','.join([str(x) for x in data]) + '\n')