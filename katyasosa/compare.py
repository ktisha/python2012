# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from collections import namedtuple
import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from Bio import SeqIO
import itertools


class GeneFinder(object):
    __metaclass__ = ABCMeta

    executable = "gene_finder"
    name = "gene_finder"

    def __init__(self, data_dir, lib_dir):
        self.lib_dir = lib_dir
        self.data_dir = data_dir
        self.install()

    def execute(self, genome_name):
        self.genome_name = genome_name
        genome_path = os.path.join(self.data_dir, genome_name + ".fasta")
        args = self.get_args(genome_path)
        devnull = open(os.devnull, "w")

        subprocess.check_call(
            [os.path.join(self.lib_dir, self.executable)] + args,
            stdout=devnull, stderr=devnull)
        parsed_result_path = os.path.join(self.data_dir,
            "{0}_{1}_genes.fasta".format(genome_name, self.name))

        def rename(gene):
            gene.id = gene.name = gene.description = self.name  
        result = itertools.imap(rename, self.parse_result())
        SeqIO.write(self.parse_result(), parsed_result_path, "fasta")
        return parsed_result_path

    __call__ = execute

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def get_args(self, _genome_path):
        pass

    @abstractmethod
    def parse_result(self):
        pass


class GeneMarkCommonGC(GeneFinder):
    """
    ./gm -rn -m heuristic_path genome_path
    """
    executable = "gm"
    name = "gm_commonGC"

    def install(self):
        gm_key_path = os.path.join(self.lib_dir, "gm_key")
        if not os.path.isfile(os.path.expanduser("~/.gm_key")):
            shutil.copyfile(gm_key_path, os.path.expanduser("~/.gm_key"))

    def get_args(self, genome_path):
        gc = common_gc_content(SeqIO.parse(genome_path, "fasta"))
        gc = min(70, max(30, int(gc)))
        heuristic_dir = os.path.join(self.lib_dir, "heuristic_mat")
        heuristic_filename = os.path.join(heuristic_dir, "heu_11_{0}.mat".format(gc))
        return ["-rn", "-m", heuristic_filename, genome_path]

    def parse_result(self):
        result_path = os.path.join(self.data_dir, self.genome_name + ".fasta.rgn")
        if not os.path.isfile(os.path.expanduser(result_path)):
            return

        gm_result = SeqIO.parse(result_path, "fasta")

        for seq_record in gm_result:
            seq_record.description = ""
            yield seq_record

class GeneMarkEveryGC(GeneMarkCommonGC):
    """
   For every GC:
   ./gm -rn -m heuristic_for_the_gc_path contigs_with_the_gc_path
   """
    executable = "gm"
    name = "gm_everyGC"

    def execute(self, genome_name):
        genome_path = os.path.join(self.data_dir, genome_name + ".fasta")

        counter = [0]
        def rename(gene):
            gene.id = gene.description = gene.name = self.name + "_" + str(counter[0])
            counter[0] += 1
            return gene

        genes = []
        execute = super(GeneMarkEveryGC, self).execute
        for seq_record in SeqIO.parse(genome_path, "fasta"):
            if len(seq_record.seq) > 200:
                with NamedTemporaryFile(prefix=seq_record.id,
                    suffix=".fasta") as f:
                    SeqIO.write(seq_record, f, "fasta")
                    f.flush()
                    current_genes = SeqIO.parse(execute(f.name.replace(".fasta", "")),
                        "fasta")
                    genes.append(itertools.imap(rename, current_genes))

        parsed_result_path = os.path.join(self.data_dir,
            "{0}_{1}_genes.fasta".format(genome_name, self.name))
        SeqIO.write(itertools.chain(*genes), parsed_result_path, "fasta")
        return parsed_result_path

def common_gc_content(sequences):
    """
    Example:
    s = "AGCCT"
    gc_content = count_gc_content(s)
    print "GC content is %.2f%%"%gc_content

    Result:
    GC content is 60.00%
    """
    GC_count, length = 0, 0
    for seq_record in sequences:
        sequence = seq_record.seq
        GC_count += sequence.count("G") + sequence.count("C")
        length += len(sequence) - sequence.count("N")
    return round((1.0 * GC_count)/length * 100, 2)

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
    keys = set()
    with open(sam_path) as first:
        for line in first:
            if line.startswith('@'):
                pass
            else:
                sl = line.split()
                qname, rname, mapq = sl[0], sl[2], int(sl[4])
                keys.add(qname)
                if mapq >= 200: #mapq = -10*log(10, Pr{mapp. pos. is wrong}), if mapq = 200, Pr{..} = 10**(-20)
                    res[qname] = rname
    return res, len(keys)

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
    lib_dir = 'genemark_suite_linux_64/gmsuite'
    genomes = {'ECO2_seq': 'Data/eco_genes.fasta', 'ECO3_seq': 'Data/eco_genes.fasta',
               'ECO6_seq': 'Data/eco_genes.fasta', 'ECO7_seq': 'Data/eco_genes.fasta',
               'MRU5_seq': 'Data/mru_genes.fasta', 'MRU6_seq': 'Data/mru_genes.fasta',
               'MRU9_seq': 'Data/mru_genes.fasta', 'PHE4_seq': 'Data/phe_genes.fasta',
               'PHE6_seq': 'Data/phe_genes.fasta', 'PHE7_seq': 'Data/phe_genes.fasta'}
    gm_common_gc = GeneMarkCommonGC(data_dir, lib_dir)
    gm_every_gc = GeneMarkEveryGC(data_dir, lib_dir)
    tools = [gm_common_gc, gm_every_gc]
    with open('compare_out', 'w') as out:
        for data in compare_data(tools, genomes, data_dir):
            out.write(','.join([str(x) for x in data]) + '\n')