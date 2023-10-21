class DatabaseManager:
    def __init__(self, table_name: str, cursor) -> None:
        self.cursor = cursor
        self.table_name = table_name

    def create_table(self, sql: str):
        try:
            self.cursor.execute(sql)
            print(f"Table created or already exists: {self.table_name}")
        except Exception as e:
            print(e)

    def drop_table(self):
        try:
            sql = f'DROP TABLE IF EXISTS {self.table_name}'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

class RawSequenceTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('raw_sequence', cursor)

    def create(self):
        sql = """
        CREATE TABLE raw_sequence (
            id SERIAL PRIMARY KEY,
            title varchar(255) NOT NULL,
            nucleotide_sequence text NOT NULL
            )
        """
        self.create_table(sql)

class GeneTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('gene', cursor)

    def create(self):
        sql = """CREATE TABLE gene (id SERIAL PRIMARY KEY, gene_name varchar(255) NOT NULL,
                nucleotide_sequence text NOT NULL)"""
        self.create_table(sql)


class ProteinTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('protein', cursor)

    def create(self):
        sql = """
        CREATE TABLE protein (
            id SERIAL PRIMARY KEY,
            name varchar(255),
            aminoacid_sequence text NOT NULL
            )
        """
        self.create_table(sql)

class AlignmentTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('alignment', cursor)

    def create(self):
        sql = """
        CREATE TABLE alignment (
            id SERIAL PRIMARY KEY,
            length INT NOT NULL,
            bit_score FLOAT NOT NULL,
            raw_score INT NOT NULL,
            evalue FLOAT NOT NULL,
            identity INT NOT NULL,
            positive INT NOT NULL,
            query_from INT NOT NULL,
            query_to INT NOT NULL,
            hit_seq TEXT NOT NULL,
            query_seq TEXT NOT NULL,
            gene_id INT NOT NULL,
            protein_id INT NOT NULL,
            raw_seq_id INT NOT NULL,
            FOREIGN KEY (gene_id) REFERENCES gene(id),
            FOREIGN KEY (protein_id) REFERENCES protein(id),
            FOREIGN KEY (raw_seq_id) REFERENCES raw_sequence(id)
            )
        """
        self.create_table(sql)


class FunctionTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('function', cursor)

    def create(self):
        sql = """CREATE TABLE function (id SERIAL PRIMARY KEY,
                description text NOT NULL, protein_id integer NOT NULL,
                FOREIGN KEY (protein_id) REFERENCES protein(id))"""
        self.create_table(sql)

class SplicingVariantTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('splicing_variant', cursor)

    def create(self):
        sql = """CREATE TABLE splicing_variant (id SERIAL PRIMARY KEY,
                variant_sequence text NOT NULL, gene_id integer NOT NULL, protein_id integer NOT NULL,
                FOREIGN KEY (gene_id) REFERENCES gene(id), FOREIGN KEY (protein_id) REFERENCES protein(id))"""
        self.create_table(sql)


class PathwayTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('pathway', cursor)

    def create(self):
        sql = """CREATE TABLE pathway (id SERIAL PRIMARY KEY,
                name varchar(255) NOT NULL, description text)"""
        self.create_table(sql)

class ProteinPathwayTable(DatabaseManager):
    def __init__(self, cursor) -> None:
        super().__init__('protein_pathway', cursor)

    def create(self):
        sql = """CREATE TABLE protein_pathway (id SERIAL PRIMARY KEY,
                protein_id integer NOT NULL, pathway_id integer NOT NULL,
                FOREIGN KEY (protein_id) REFERENCES protein(id),
                FOREIGN KEY (pathway_id) REFERENCES pathway(id))"""
        self.create_table(sql)


class DatabaseInitializer:
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.tables = [
            RawSequenceTable(cursor),
            GeneTable(cursor),
            ProteinTable(cursor),
            AlignmentTable(cursor),
            FunctionTable(cursor),
            SplicingVariantTable(cursor),
            PathwayTable(cursor),
            ProteinPathwayTable(cursor)
        ]

    def create_all(self):
        for table in self.tables:
            table.create()
        print("Tables succesfully created...")

    def drop_all(self):
        for table in reversed(self.tables):
            table.drop_table()
        print("Tables sucesfully dropped...")

