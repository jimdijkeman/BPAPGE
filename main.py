from pprint import pprint
import re
import argparse

# Import database connection class
from connection import Connection

# Import query files
from queries.gene import GeneQuery
from queries.protein import ProteinQuery
from queries.pathway import PathwayQuery
from queries.protein_pathway import ProteinPathwayQuery

# Import database classes
from database import DatabaseInitializer

# Import API wrappers
from api import UniProtAPI, KEGGAPI
# Import BLAST wrapper & JSON parser
from blast import BLAST, BlastJSONParser

def blast(query_file, db_file):
     blast = BLAST('blastx', query_file, db_file).run()
     return blast

def insert_gene_and_protein():
    data = BlastJSONParser('data/out/blastresults.out').parse()
    with Connection.connect_from_ini_config() as (cur, conn):
        gene_query = GeneQuery('gene', cur)
        protein_query = ProteinQuery('protein', cur)
        proteins_in_db = []
        for hit in data:
            accession = hit['description'][0]['accession']
            nuc_sequence = hit['original_nuc_seq']
            gene_id = gene_query.insert(accession, nuc_sequence)
            protein_data = get_protein_data(hit, gene_id)
            if protein_data[0] not in proteins_in_db:
                protein_id = protein_query.insert(protein_data)
                proteins_in_db.append(protein_data[0])


def get_protein_data(hit, gene_id):
    pattern = re.compile(r'GN=([^\s]+)')
    match = pattern.search(hit['description'][0]['title'])
    if match:
        gn_value = match.group(1)
    else:
        gn_value = ''
    amino_seq = hit['hsps'][0]['qseq']
    return (gn_value, amino_seq, gene_id)


def get_pathways():
    with Connection.connect_from_ini_config() as (cur, conn):
        kegg_api = KEGGAPI()
        uniprot_api = UniProtAPI()
        proteins = ProteinQuery('protein', cur).get_all()
        pathways_in_db = []
        for p in proteins:
            kegg_id = uniprot_api.translate_accession_to_keggid(p[1])
            pathways = kegg_api.get_pathways(kegg_id)
            pathway_query = PathwayQuery('pathway', cur)
            protein_pathway_query = ProteinPathwayQuery('protein_pathway', cur)
            for name, description in pathways.items():
                if name not in pathways_in_db:
                   pathway_id = pathway_query.insert(name, description)
                   protein_pathway_query.insert(p[0], pathway_id)
                   pathways_in_db.append(name)
                else:
                   pw_id = pathway_query.get_by_kegg_id(name)
                   protein_pathway_query.insert(p[0], pw_id)

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
            epilog='https://github.com/jimdijkeman/BPAPGE'
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
        insert_gene_and_protein()
    if args.get_pathways:
        get_pathways()
    if args.drop_tables:
        drop_tables()

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()


