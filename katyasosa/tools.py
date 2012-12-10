from abc import abstractmethod, ABCMeta
import os
import re
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from Bio import SeqIO
import itertools

__author__ = 'katya'

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
        GC_count += sequence.count('G') + sequence.count('C')
        length += len(sequence) - sequence.count('N')
    return round((1.0 * GC_count)/length * 100, 2)

class GeneFinder(object):
    __metaclass__ = ABCMeta

    executable = 'gene_finder'
    name = 'gene_finder'

    def __init__(self, data_dir, lib_dir):
        self.lib_dir = lib_dir
        self.data_dir = data_dir
        self.install()

    def execute(self, genome_name):
        genome_path = os.path.join(self.data_dir, genome_name + '.fasta')
        args = self.get_args(genome_path)
        devnull = open(os.devnull, "w")

        subprocess.check_call(
            [os.path.join(self.lib_dir, self.executable)] + args,
            stdout=devnull, stderr=devnull)
        parsed_result_path = os.path.join(self.data_dir,
            '{0}_{1}_genes.fasta'.format(genome_name, self.name))

        SeqIO.write(self.parse_result(genome_path), parsed_result_path, 'fasta')
        return parsed_result_path

    __call__ = execute

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def get_args(self, _genome_path):
        pass

    @abstractmethod
    def parse_result(self, _genome_path):
        pass


class GeneMarkCommonGC(GeneFinder):
    """
    ./gm -rn -m heuristic_path genome_path
    """
    executable = 'gm'
    name = 'gm_commonGC'

    def install(self):
        gm_key_path = os.path.join(self.lib_dir, 'gm_key')
        if not os.path.isfile(os.path.expanduser('~/.gm_key')):
            shutil.copyfile(gm_key_path, os.path.expanduser('~/.gm_key'))

    def get_args(self, genome_path):
        gc = common_gc_content(SeqIO.parse(genome_path, 'fasta'))
        gc = min(70, max(30, int(gc)))
        heuristic_dir = os.path.join(self.lib_dir, 'heuristic_mat')
        heuristic_filename = os.path.join(heuristic_dir, 'heu_11_{0}.mat'.format(gc))
        return ["-rn", "-m", heuristic_filename, genome_path]

    def parse_result(self, genome_path):
        result_path = genome_path + '.fasta.rgn'
        if not os.path.isfile(os.path.expanduser(result_path)):
            return

        gm_result = SeqIO.parse(result_path, 'fasta')

        for seq_record in gm_result:
            seq_record.description = ""
            yield seq_record

class GeneMarkEveryGC(GeneMarkCommonGC):
    """
   For every GC:
   ./gm -rn -m heuristic_for_the_gc_path contigs_with_the_gc_path
   """
    executable = 'gm'
    name = 'gm_everyGC'

    def execute(self, genome_name):
        genome_path = os.path.join(self.data_dir, genome_name + '.fasta')

        counter = [0]
        def rename(gene):
            gene.id = gene.description = gene.name = self.name + '_' + str(counter[0])
            counter[0] += 1
            return gene

        genes = []
        execute = super(GeneMarkEveryGC, self).execute
        for seq_record in SeqIO.parse(genome_path, 'fasta'):
            if len(seq_record.seq) > 200:
                with NamedTemporaryFile(prefix=seq_record.id,
                    suffix='.fasta') as f:
                    SeqIO.write(seq_record, f, 'fasta')
                    f.flush()
                    current_genes = SeqIO.parse(execute(f.name.replace('.fasta', '')),
                        'fasta')
                    genes.append(itertools.imap(rename, current_genes))

        parsed_result_path = os.path.join(self.data_dir,
            '{0}_{1}_genes.fasta'.format(genome_name, self.name))
        SeqIO.write(itertools.chain(*genes), parsed_result_path, 'fasta')
        return parsed_result_path

class GeneMarkHmmCommomGC(GeneFinder):
    executable = 'gmhmmp'
    name = 'gmhmmp_commonGC'

    def install(self):
        gm_key_path = os.path.join(self.lib_dir, 'gm_key')
        if not os.path.isfile(os.path.expanduser('~/.gm_key')):
            shutil.copyfile(gm_key_path, os.path.expanduser('~/.gm_key'))

    def get_args(self, genome_path):
        gc = common_gc_content(SeqIO.parse(genome_path, 'fasta'))
        gc = min(70, max(30, int(gc)))
        heuristic_dir = os.path.join(self.lib_dir, 'heuristic_mod')
        heuristic_filename = os.path.join(heuristic_dir, 'heu_11_{0}.mod'.format(gc))
        result_path = genome_path + '.gmhmm'
        return ['-d', '-p', '0','-m', heuristic_filename, '-o', result_path, genome_path]

    def parse_result(self, genome_path):
        result_path = genome_path + '.gmhmm'
        reading_gene = False
        with open(result_path) as f:
            for line in f:
                if line.startswith('>gene'):
                    reading_gene = True
                    seq = []
                    seq_id = re.sub(r'[\s>]', '', line)
                    # >gene_2|GeneMark.hmm|57_nt|+|1|57	>NODE_3_length_713_cov_1.25228
                elif reading_gene:
                    if line.isspace():
                        reading_gene = False
                        seq = SeqIO.Seq(''.join(seq))
                        #genes.append(Gene(contig_id, strand, left_index, right_index, str_seq))
                        yield SeqIO.SeqRecord(seq, id='>' + seq_id, description = '', name='')
                    else:
                         seq.append(line.strip())

class GeneMarkHmmEveryGC(GeneMarkHmmCommomGC):
    executable = 'gmhmmp'
    name = 'gmhmmp_everyGC'

    def execute(self, genome_name):
        genome_path = os.path.join(self.data_dir, genome_name + '.fasta')

        counter = [0]
        def rename(gene):
            gene.id = gene.description = gene.name = self.name + '_' + str(counter[0])
            counter[0] += 1
            return gene

        genes = []
        execute = super(GeneMarkHmmCommomGC, self).execute
        for seq_record in SeqIO.parse(genome_path, 'fasta'):
            if len(seq_record.seq) > 200:
                with NamedTemporaryFile(prefix=seq_record.id,
                    suffix='.fasta') as f:
                    SeqIO.write(seq_record, f, 'fasta')
                    f.flush()
                    current_genes = SeqIO.parse(execute(f.name.replace('.fasta', '')),
                        'fasta')
                    genes.append(itertools.imap(rename, current_genes))

        parsed_result_path = os.path.join(self.data_dir,
            '{0}_{1}_genes.fasta'.format(genome_name, self.name))
        SeqIO.write(itertools.chain(*genes), parsed_result_path, 'fasta')
        return parsed_result_path

class GeneMarkS(GeneFinder):
    executable = 'gmsn.pl'
    name = 'gms'

    def install(self):
        gm_key_path = os.path.join(self.lib_dir, 'gm_key')
        if not os.path.isfile(os.path.expanduser('~/.gm_key')):
            shutil.copyfile(gm_key_path, os.path.expanduser('~/.gm_key'))

    def get_args(self, genome_path):
        return ['--clean', genome_path]

    def parse_result(self, genome_path):
        result_path = genome_path + '.fasta.lst'
        if not os.path.isfile(os.path.expanduser(result_path)):
            return
        contigs = dict([(s.id, s.seq) for s in SeqIO.parse(open(genome_path),
            'fasta')])
        with open(result_path, 'r') as f:
            reading_genes = False
            for line in f.readlines():
                if line.startswith('    #'):
                    reading_genes = True
                    continue
                if line.startswith('---') or line.strip() == '':
                    reading_genes = False
                if reading_genes:
                    gene_sp = re.split(r'[\t ]+', line.strip())
                    seq_id = contig_id + '_gene_' + gene_sp[0]
                    l_index = int(gene_sp[2].replace('<', '')) -1
                    r_index = int(gene_sp[3].replace('>', ''))
                    seq = contig_seq[l_index:r_index]
                    yield SeqIO.SeqRecord(seq, id=seq_id, description='', name='')
                if line.startswith('FASTA definition line'):
                    contig_id = line.strip().replace('FASTA definition line: ', '')
                    contig_seq = contigs[contig_id]
        os.remove(result_path)
        os.remove('gms.log')
        os.remove('GeneMark_hmm.mod')
