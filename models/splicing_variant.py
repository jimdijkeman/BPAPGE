from dataclasses import dataclass

@dataclass
class SplicingVariant:
    variant_sequence: str
    gene_id: int
    protein_id: int
