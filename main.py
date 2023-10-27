from pprint import pprint
import argparse
from tqdm import tqdm
import psycopg2

# Import database connection class
from connection import Connection

# Import query files
from queries.gene import GeneQuery
from queries.raw_sequence import RawSequenceQuery
from queries.protein import ProteinQuery
from queries.pathway import PathwayQuery
from queries.protein_pathway import ProteinPathwayQuery
from queries.protein_alignment import ProteinAlignmentQuery
from queries.alignment import AlignmentQuery
from queries.splicing_variant import SplicingVariantQuery
from queries.function import FunctionQuery
# Import models
from models.alignment import Alignment
from models.gene import Gene
from models.protein import Protein
from models.protein_alignment import ProteinAlignment
from models.raw_sequence import RawSequence
from models.splicing_variant import SplicingVariant
from models.function import Function
# Import database classes
from database import DatabaseInitializer

# Import API wrappers
from api import UniProtAPI, KEGGAPI

# Import BLAST wrapper & JSON parser
from blast import BLAST, BlastJSONParser

# Import parser functions
from parsers import (parse_alignment,
                     parse_gene,
                     parse_protein,
                     get_sequence_from_title,
                     get_isoforms_from_fasta
                     )



def blast(query_file, db_file):
     blast = BLAST('blastx', query_file, db_file).run()
     return blast


def get_alignments():
    data = BlastJSONParser('data/out/blastresults.out').parse()
    with Connection.connect_from_ini_config() as (cur, conn):
        for alignments in tqdm(data, desc='Processing alignments', unit='alignment'):
        # for alignments in data:
            raw_seq = RawSequence(
                    alignments['results']['search']['query_title'],
                    get_sequence_from_title('seq.fa', alignments['results']['search']['query_title'])
                    )
            raw_seq_id = RawSequenceQuery('raw_sequence', cur).insert(raw_seq)
            for a in alignments['results']['search']['hits']:
                if a['hsps'][0]['evalue'] < 1e-20:
                    query_from, query_to = a['hsps'][0]['query_from'], a['hsps'][0]['query_to']

                    gene = parse_gene(a, raw_seq.nucleotide_sequence[query_from:query_to])
                    existing_gene = GeneQuery('gene', cur).get_id_by_name(gene.name)
                    if existing_gene:
                        gene_id = existing_gene
                    else:
                        gene_id = GeneQuery('gene', cur).insert(gene)

                    protein = parse_protein(a)
                    existing_protein = ProteinQuery('protein', cur).get_id_by_name(protein.name)
                    if existing_protein:
                        protein_id = existing_protein
                    else:
                        protein_id = ProteinQuery('protein', cur).insert(parse_protein(a))

                    alignment_id = AlignmentQuery('alignment', cur).insert(parse_alignment(a, gene_id, protein_id, raw_seq_id))

def get_pathways():
    with Connection.connect_from_ini_config() as (cur, conn):
        added_pathways = {}
        processed_proteins = {}

        proteins = ProteinQuery('protein', cur).get_all()
        
        for prot in tqdm(proteins, desc='Processing proteins', unit='protein'):
            gene_protein_join = ProteinQuery('protein', cur).join_genes(prot[0])
            for gene_name, prot_id in gene_protein_join:
                if gene_name not in processed_proteins:
                    kegg_id = UniProtAPI().translate_accession_to_keggid(gene_name)
                    pathways = KEGGAPI().get_pathways(kegg_id)
                    for key, value in pathways.items():
                        if "asn" in key:
                            if key not in added_pathways:
                                pathway_id = PathwayQuery('pathway', cur).insert(key, value)
                                added_pathways[key] = pathway_id
                            else:
                                pathway_id = added_pathways[key]
                        
                            ProteinPathwayQuery('protein_pathway', cur).insert(prot_id, pathway_id)
                            processed_proteins[gene_name] = pathway_id
                else:
                    ProteinPathwayQuery('protein_pathway', cur).insert(prot_id, processed_proteins[gene_name])

def load_isoforms():
    with Connection.connect_from_ini_config() as (cur, conn):
        isoform_dict = get_isoforms_from_fasta("data/proteoom_alligator.fa")
        existing_genes_dict = {}
        existing_genes = GeneQuery('gene', cur).get_all()
        for x in existing_genes:
            existing_genes_dict[x[1]] = x[0]

        for gn, info in tqdm(isoform_dict.items(), desc='Processing isoforms', unit='isoform'):
            if gn in existing_genes_dict:
                splice_protein = Protein(info['name'], info['sequence'])
                protein_id = ProteinQuery('protein', cur).insert(splice_protein)
                splicing_variant = SplicingVariant(
                    info['sequence'],
                    existing_genes_dict[gn],
                    protein_id
                )
                SplicingVariantQuery('splicing_variant', cur).insert(splicing_variant)

def get_functions():
    with Connection.connect_from_ini_config() as (cur, conn):
        proteins = ProteinQuery('protein', cur).get_all()
        for prot in tqdm(proteins, desc='Fetching protein functions', unit='function'):
            gene_protein_join = ProteinQuery('protein', cur).join_genes(prot[0])
            for gene_name, prot_id in gene_protein_join:
                function = UniProtAPI().get_function(gene_name)
                if function:
                    new_function = Function(function, prot_id)
                    try:
                        FunctionQuery('function', cur).insert(new_function)
                    except psycopg2.IntegrityError as e:
                        conn.rollback()


def create_tables():
    with Connection.connect_from_ini_config() as (cur, conn):
        db_init = DatabaseInitializer(cur)
        db_init.create_all()

def drop_tables():
    with Connection.connect_from_ini_config() as (cur, conn):
        db_init = DatabaseInitializer(cur)
        db_init.drop_all()

def main():
    copyright_notice = """
    BlastDBTool  Copyright (C) 2023  Jim van Dijk
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see LICENSE.md for details.\n"""
    print(copyright_notice)

    parser = argparse.ArgumentParser(
            description='BlastDBTool Command Line Interface',
            epilog='https://github.com/jimdijkeman/BlastDBTool'
            )
    
    parser.add_argument('--blast', nargs=2, metavar=('QUERY_FILE', 'DB_FILE'), help='Run BLAST')
    parser.add_argument('--insert', action='store_true', help='Insert gene and protein data')
    parser.add_argument('--load_isoforms', action='store_true', help='Load isoforms from a blastdb')
    parser.add_argument('--get_functions', action='store_true', help='Fetch protein function')
    parser.add_argument('--get_pathways', action='store_true', help='Retrieve pathways')
    parser.add_argument('--create_tables', action='store_true', help='Create all tables')
    parser.add_argument('--drop_tables', action='store_true', help='Drop all tables')
    args = parser.parse_args()


    if args.drop_tables:
        drop_tables()
    if args.blast:
        blast(*args.blast)
    if args.create_tables:
        create_tables()
    if args.insert:
        get_alignments()
    if args.load_isoforms:
        load_isoforms()
    if args.get_functions:
        get_functions()
    if args.get_pathways:
        get_pathways()

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()


