from models.gene import Gene
from models.alignment import Alignment
from models.protein import Protein

import re

from Bio import SeqIO

def parse_gene_name_from_title(title):
    pattern = re.compile(r'GN=([^\s]+)')
    match = pattern.search(title)
    if match:
        gn_value = match.group(1)
    else:
        gn_value = ''
    return gn_value

def parse_protein_name_from_title(title):
    pattern = re.compile(r'^(.+?)\sOS=')
    match = pattern.search(title)
    if match:
        pn_value = match.group(1)
    else:
        pn_value = ''
    return pn_value

def parse_protein(data:dict) -> Protein:
    hsps = data['hsps'][0]
    description = data['description'][0]
    protein_obj = Protein(
            name = parse_protein_name_from_title(description['title']),
            amino_acid_sequence = hsps['hseq']
            )
    return protein_obj

def parse_alignment(data:dict, gene_identifier, protein_identifier, raw_seq_identifier) -> Alignment:
    hsps = data['hsps'][0]
    alignment_obj = Alignment(
            length = hsps['align_len'],
            bit_score = hsps['bit_score'],
            raw_score = hsps['score'],
            evalue = hsps['evalue'],
            identity = hsps['identity'],
            positive = hsps['positive'],
            query_from = hsps['query_from'],
            query_to = hsps['query_to'],
            hit_seq = hsps['hseq'],
            query_seq = hsps['qseq'],
            gene_id = gene_identifier,
            protein_id = protein_identifier,
            raw_seq_id = raw_seq_identifier
            )
    return alignment_obj

def parse_gene(data: dict, seq: str) -> Gene:
    hsps = data['hsps'][0]
    description = data['description'][0]
    gene = Gene(
            name = parse_gene_name_from_title(description['title']),
            nucleotide_sequence = seq
            )
    return gene

def get_sequence_from_title(fasta_file: str, search_id: str) -> str:
    with open(fasta_file, "r") as file:
        for seq in SeqIO.parse(file, "fasta"):
            if seq.id == search_id:
                return str(seq.seq)
        return ''
