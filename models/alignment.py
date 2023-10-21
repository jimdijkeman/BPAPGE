from dataclasses import dataclass
from pprint import pprint


@dataclass
class Alignment:
    length: int
    bit_score: float
    raw_score: int
    evalue: float
    identity: int
    positive: int
    query_from: int
    query_to: int
    hit_seq: str
    query_seq: str
    gene_id: int
    protein_id: int
    raw_seq_id: int
