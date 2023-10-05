from .basequery import BaseQuery

class GeneQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('gene', cursor)

    def insert(self, accession, nuc_sequence):
        query = f'INSERT INTO {self.table} (accession, nucleotide_sequence) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (accession, nuc_sequence))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
