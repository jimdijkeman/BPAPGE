from .basequery import BaseQuery
from models.raw_sequence import RawSequence

class RawSequenceQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('raw_sequence', cursor)

    def insert(self, raw_sequence: RawSequence):
        query = f"""
        INSERT INTO {self.table} (
        title,
        nucleotide_sequence
        )
        VALUES (
        %s, %s
        ) RETURNING id
        """
        values = (raw_sequence.title, raw_sequence.nucleotide_sequence)
        self.cursor.execute(query, values)
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
