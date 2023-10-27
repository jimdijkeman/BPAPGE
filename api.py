import requests
import re

class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
    
    def make_request(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

class UniProtAPI(APIClient):
    def __init__(self) -> None:
        base_url = 'http://togows.org'
        super().__init__(base_url)

    def translate_accession_to_keggid(self, accession: str):
        endpoint = f'entry/ebi-uniprot/{accession}/dr.json'
        res = self.make_request(endpoint)
        kegg_id = res[0]['KEGG'][0][0]
        return kegg_id
    
    def get_function(self, gene_name: str):
        endpoint = f'entry/ebi-uniprot/{gene_name}/comment.json'
        res = self.make_request(endpoint)
        pattern = r"(\(.*?\))|(\{.*?\})|(?<=\W)\."
        if res[0].get('FUNCTION'):
            function_raw = res[0].get('FUNCTION')[0]
            result = re.sub(pattern, "", function_raw)
            return result.strip()
        else:
            return 0

class KEGGAPI(APIClient):
    def __init__(self) -> None:
        base_url = 'http://togows.org'
        super().__init__(base_url)

    def get_pathways(self, kegg_id) -> dict:
        endpoint = f'entry/kegg-genes/{kegg_id}/pathways.json'
        res = self.make_request(endpoint)
        return res[0]


