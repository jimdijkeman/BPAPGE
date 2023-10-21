from pprint import pprint
import argparse

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

# Import models
from models.alignment import Alignment
from models.gene import Gene
from models.protein import Protein
from models.protein_alignment import ProteinAlignment
from models.raw_sequence import RawSequence

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
                     get_sequence_from_title
                     )



def blast(query_file, db_file):
     blast = BLAST('blastx', query_file, db_file).run()
     return blast


def get_alignments():
    data = BlastJSONParser('data/out/blastresults.out').parse()
    with Connection.connect_from_ini_config() as (cur, conn):
        for alignments in data:
            raw_seq = RawSequence(
                    alignments['results']['search']['query_title'],
                    get_sequence_from_title('seq.fa', alignments['results']['search']['query_title'])
                    )
            raw_seq_id = RawSequenceQuery('raw_sequence', cur).insert(raw_seq)
            for a in alignments['results']['search']['hits']:
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
    parser.add_argument('--get_pathways', action='store_true', help='Retrieve pathways')
    parser.add_argument('--create_tables', action='store_true', help='Create all tables')
    parser.add_argument('--drop_tables', action='store_true', help='Drop all tables')
    args = parser.parse_args()

    if args.blast:
        blast(*args.blast)
    if args.create_tables:
        create_tables()
    if args.insert:
        get_alignments()
    if args.get_pathways:
        #get_pathways()
        pass
    if args.drop_tables:
        drop_tables()

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()


