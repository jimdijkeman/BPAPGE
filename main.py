from pprint import pprint

from connection import Connection
from queries.gene import GeneQuery

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

def insert_genes(data):
    with Connection.connect_from_ini_config() as (cur, conn):
        genequery = GeneQuery('gene', cur)
        for hit in data:
            accession = hit['description'][0]['accession']
            nuc_sequence = hit['original_nuc_seq']
            #pprint(nuc_sequence)
            query_result = genequery.insert(accession, nuc_sequence)
            pprint(query_result)
            #break

insert_genes(data)
