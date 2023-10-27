import re
import requests

class APIClient:
    """
    A client for making API requests.
    """
    def __init__(self, base_url: str) -> None:
        """
        Initializes the APIClient with a base URL.

        Parameters:
        base_url (str): The base URL for the API.
        """
        self.base_url = base_url

    def make_request(self, endpoint: str):
        """
        Makes a request to the given endpoint and returns JSON response.

        Parameters:
        endpoint (str): The endpoint to make the request to.

        Returns:
        dict: JSON response from the endpoint.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

class UniProtAPI(APIClient):
    """
    A client for interacting with the UniProt API.
    """
    def __init__(self) -> None:
        """
        Initializes the UniProtAPI with a specific base URL.
        """
        base_url = 'http://togows.org'
        super().__init__(base_url)

    def translate_accession_to_keggid(self, accession: str):
        """
        Translates a UniProt accession to a KEGG ID.

        Parameters:
        accession (str): The UniProt accession to be translated.

        Returns:
        str: The corresponding KEGG ID.
        """
        endpoint = f'entry/ebi-uniprot/{accession}/dr.json'
        res = self.make_request(endpoint)
        kegg_id = res[0]['KEGG'][0][0]
        return kegg_id

    def get_function(self, gene_name: str):
        """
        Retrieves the function of a gene.

        Parameters:
        gene_name (str): The name of the gene to retrieve the function for.

        Returns:
        str: The function of the gene.
        """
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
    """
    A client for interacting with the KEGG API.
    """
    def __init__(self) -> None:
        """
        Initializes the KEGGAPI with a specific base URL.
        """
        base_url = 'http://togows.org'
        super().__init__(base_url)

    def get_pathways(self, kegg_id) -> dict:
        """
        Retrieves the pathways for a given KEGG ID.

        Parameters:
        kegg_id (str): The KEGG ID to retrieve pathways for.

        Returns:
        dict: A dictionary containing the pathways.
        """
        endpoint = f'entry/kegg-genes/{kegg_id}/pathways.json'
        res = self.make_request(endpoint)
        return res[0]