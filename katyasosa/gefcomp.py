# -*- coding: utf-8 -*-

from collections import namedtuple
import csv
import importlib
import os
import subprocess
import itertools
import sys
import imp
from config import *



def cross_align(predict_path, genes_path, out_path_prefix, tool_name):
    """Aligns predicted genes on known genes using BWA and vise versa.

    :param predict_path: path to a FASTA file with genes, predicted
                         by the tool, being evaluated.
    :param genes_path: path to a FASTA file with **true** genes.
    :param out_path_prefix: a prefix for resulting alignment-files in
                            SAM format.
    :param tool_name: human-readable name of the tool, being evaluated.
    :return: a tuple, where the first argument is a path to a SAM file
             with predicted genes, aligned on known genes, and second
             is a SAM file with known genes, aligned on predicted genes.
    """
    devnull = open(os.devnull, 'w')
    subprocess.call(['bwa', 'index', '-a', 'bwtsw', predict_path],
        stdout=devnull, stderr=devnull)
    subprocess.call(['bwa', 'index', '-a', 'bwtsw', genes_path],
        stdout=devnull, stderr=devnull)

    genes_sam_path = out_path_prefix + tool_name + '_on.sam'
    predict_sam_path = out_path_prefix + 'on_' + tool_name + '.sam'
    with open(genes_sam_path, 'w') as fout:
        subprocess.call(['bwa', 'bwasw', predict_path, genes_path],
            stdout=fout, stderr=devnull)
    with open(predict_sam_path, 'w') as fout:
        subprocess.call(['bwa', 'bwasw', genes_path, predict_path],
            stdout=fout, stderr=devnull)

    return genes_sam_path, predict_sam_path


Hypothesis = namedtuple('Hypothesis', ['name', 'TP', 'FP', 'FN', 'precision', 'recall', 'f1_score'])

def evaluate_alignments(genes_sam_path, predict_sam_path):
    """Evaluates precision-recall and F1-score metrics for aligned genes."""
    def unique_alignments(sam_path):
        res, seen = {}, set()
        with open(sam_path) as sam_file:
            for line in sam_file:
                if line.startswith('@'):
                    continue

                chunks = line.split()
                qname, rname, mapq = chunks[0], chunks[2], int(chunks[4])
                seen.add(qname)

                # mapq = -10*log(10, Pr{mapp. pos. is wrong}), if mapq = 200, Pr{..} = 10**(-20)
                if mapq >= 200:
                    res[qname] = rname

        return res, len(seen)

    predict_on_genes, predict_count = unique_alignments(predict_sam_path)
    genes_on_predict, genes_count = unique_alignments(genes_sam_path)

    # Hypothesis #1: predicted gene is actually a known gene.
    TP = len(predict_on_genes)
    FP = predict_count - TP
    FN = genes_count - len(set(predict_on_genes.values()))

    precision = TP * 1. / (TP + FP)
    recall = TP * 1. / (TP + FN)
    f_score = 2 * precision * recall / (precision + recall)
    H_predict_is_gene = Hypothesis('predict is gene', TP, FP, FN,
        precision, recall, f_score)

    # Hypothesis #2: a known gene was predicted correctly.
    TP = len(genes_on_predict)
    FP = genes_count - TP
    FN = predict_count - len(set(genes_on_predict.values()))

    precision = TP * 1. / (TP + FP)
    recall = TP * 1. / (TP + FN)
    f_score = 2 * precision * recall / (precision + recall)
    H_gene_was_predicted = Hypothesis('gene was predicted', TP, FP, FN,
        precision, recall, f_score)
    return H_predict_is_gene, H_gene_was_predicted

def compare_data(tools, genomes, data_dir):
    for genome_name, tool in itertools.product(genomes, tools):
        path_result = tool.execute(genome_name)
        path_prefix = os.path.join(data_dir, genome_name) + '_'
        genes_sam_path, predict_sam_path =\
        cross_align(path_result, genomes[genome_name], path_prefix, tool.name)

        hypothesises = evaluate_alignments(genes_sam_path, predict_sam_path)
        for hypothesis in hypothesises:
            yield {'hypothesis_name': hypothesis.name,
                   'genome_name': genome_name,
                   'tool_name': tool.name,
                   'TP': hypothesis.TP,
                   'FP': hypothesis.FP,
                   'FN': hypothesis.FN,
                   'precision': hypothesis.precision,
                   'recall': hypothesis.recall,
                   'f1_score': hypothesis.f1_score}

if __name__ == '__main__':
    config_path = sys.argv[1]
    config = imp.load_source('config', config_path)

    data_dir = config.DATA_DIR
    genomes = config.GENOMES
    tools = config.GENE_FINDER_TOOLS

    csv_path = os.path.join(config.RESULT_DIR, 'summary.csv')
    with open(csv_path, 'w') as f:
        summary = csv.DictWriter(f, ['hypothesis_name', 'genome_name',
                                     'tool_name', 'TP', 'FP', 'FN',
                                     'precision', 'recall', 'f1_score'])
        summary.writeheader()
        summary.writerows(compare_data(tools, genomes, data_dir))
