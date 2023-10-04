import subprocess
import json
from pprint import pprint

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

    def parse(self):
        definitive_results = []
        with open(self.blast_result, 'r') as file:
            data = json.loads(file.read())
            for report in data['BlastOutput2']:
                results = report['report']['results']
                sorted_hits = sorted(results['search']['hits'], key=lambda x: x['hsps'][0]['evalue'])
                highest_score = sorted_hits[0]

                #if highest_score['hsps'][0]['identity'] == highest_score['hsps'][0]['align_len']:
                definitive_results.append(highest_score)

            print(len(definitive_results))

                #break
