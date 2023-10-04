import requests

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


class KEGGAPI(APIClient):
    def __init__(self) -> None:
        base_url = 'http://togows.org'
        super().__init__(base_url)

    def get_pathways(self, gene_id):
        endpoint = f'entry/kegg-genes/{gene_id}/pathways.json'
        res = self.make_request(endpoint)
        return res[0]


