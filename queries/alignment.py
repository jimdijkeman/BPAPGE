from .basequery import BaseQuery
from models.alignment import Alignment

class AlignmentQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('alignment', cursor)
    
    def insert(self, alignment: Alignment):
        query = f"""
        INSERT INTO {self.table} (
            length,
            bit_score,
            raw_score,
            evalue,
            identity,
            positive,
            query_from,
            query_to,
            hit_seq,
            query_seq,
            gene_id,
            protein_id,
            raw_seq_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        values = (
            alignment.length,
            alignment.bit_score,
            alignment.raw_score,
            alignment.evalue,
            alignment.identity,
            alignment.positive,
            alignment.query_from,
            alignment.query_to,
            alignment.hit_seq,
            alignment.query_seq,
            alignment.gene_id,
            alignment.protein_id,
            alignment.raw_seq_id
        )
        self.cursor.execute(query, values)
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
