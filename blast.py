import subprocess
import json
from pprint import pprint

from Bio import SeqIO

class BLAST:
    def __init__(self, blast_type: str, query_file: str, db_file: str,
                 output_fmt: str = "6", output_file: str = "data/out/blastresults.out", **kwargs) -> None:
        self.blast_type = blast_type
        self.query_file = query_file
        self.db_file = db_file
        self.output_fmt = output_fmt
        self.output_file = output_file
        self.extra_args = kwargs

    def run(self):
        command = f"{self.blast_type} -db {self.db_file} -query {self.query_file} -outfmt {self.output_fmt} -out {self.output_file}"

        for key, value in self.extra_args.items():
            command += f" -{key} {value}"

        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error occurred. Exit status:", result.returncode)
            print("Standard Error:")
            print(result.stderr)
            return 0
        return 1

class BlastJSONParser:
    def __init__(self, blast_result):
        self.blast_result = blast_result

    @staticmethod
    def get_sequence_from_file(fasta_file: str, search_id: str):
        with open(fasta_file, "r") as file:
            for seq in SeqIO.parse(file, "fasta"):
                if seq.id == search_id:
                    return seq.seq
            return None

    def parse(self):
        definitive_results = []
        with open(self.blast_result, 'r') as file:
            data = json.loads(file.read())
            for report in data['BlastOutput2']:
                results = report['report']['results']
                query_title = results['search']['query_title']
                sorted_hits = sorted(results['search']['hits'], key=lambda x: x['hsps'][0]['evalue'])
                highest_score = sorted_hits[0]
                highest_score['query_title'] = query_title
                highest_score['original_nuc_seq'] = str(self.get_sequence_from_file('seq.fa', query_title)) 
                definitive_results.append(highest_score)
            return definitive_results
