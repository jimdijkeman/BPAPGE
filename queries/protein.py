from .basequery import BaseQuery
from models.protein import Protein


class ProteinQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('protein', cursor)

    def insert(self, protein: Protein):
        query = f'INSERT INTO {self.table} (name, aminoacid_sequence) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (protein.name, protein.amino_acid_sequence))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]

    def get_id_by_name(self, prot_name: str):
        query = f'SELECT id FROM {self.table} WHERE name = %s'
        self.cursor.execute(query, (prot_name,))
        self.cursor.connection.commit()
        return self.cursor.fetchone()

    def join_genes(self, prot_id):
            query ="""
            SELECT DISTINCT 
                   g.gene_name, a.protein_id
            FROM 
                   alignment a
            JOIN 
                   gene g ON a.gene_id = g.id
            WHERE 
                   a.protein_id = %s;
            """
            self.cursor.execute(query, (prot_id,))
            results = self.cursor.fetchall()
            self.cursor.connection.commit()
            return results

# def get_alignment(self):
