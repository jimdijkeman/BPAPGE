from .basequery import BaseQuery
from models.splicing_variant import SplicingVariant

class SplicingVariantQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('splicing_variant', cursor)

    def insert(self, splicing_variant: SplicingVariant):
        query = f'INSERT INTO {self.table} (variant_sequence, gene_id, protein_id) VALUES (%s, %s, %s) RETURNING id'
        self.cursor.execute(query, (splicing_variant.variant_sequence, splicing_variant.gene_id, splicing_variant.protein_id))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0] 
