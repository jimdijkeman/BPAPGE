from pprint import pprint
import re
from connection import Connection

from queries.gene import GeneQuery
from queries.protein import ProteinQuery
from blast import BLAST, BlastJSONParser
from api import UniProtAPI, KEGGAPI
#with Connection.connect_from_ini_config() as (conn, curr):
#    print(conn)

#blastx = BLAST('blastx', 'seq.fa', 'data/proteoom_alligator.fa', '15')
#blastx.run()
#new_api = UniProtAPI()
#keggid = new_api.translate_accession_to_keggid("LOC102384980")
#print(keggid)
#keggapi = KEGGAPI()
#pathways = kecggapi.get_pathways("asn:102384980")
#print(pathways)

parser = BlastJSONParser('data/blastresults.out')
data = parser.parse()


def insert_gene_and_protein(data):
    with Connection.connect_from_ini_config() as (cur, conn):
        #gene_id = insert_genes(data)
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

        pprint(proteins_in_db)


def get_protein_data(hit, gene_id):
    pattern = re.compile(r'GN=([^\s]+)')
    match = pattern.search(hit['description'][0]['title'])
    if match:
        gn_value = match.group(1)
    else:
        gn_value = ''
    amino_seq = hit['hsps'][0]['qseq']
    return (gn_value, amino_seq, gene_id)

insert_gene_and_protein(data) 

