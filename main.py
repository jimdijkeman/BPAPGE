from connection import Connection

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
#pathways = keggapi.get_pathways("asn:102384980")
#print(pathways)

parser = BlastJSONParser('data/blastresults.out')
parser.parse()
