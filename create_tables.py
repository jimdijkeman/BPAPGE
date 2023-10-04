import psycopg2

conn_string = """
host='localhost'
user='jimdijkemans'
dbname='bpapge'
"""

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

try:
    print("Creating gene table....")
    sql = """CREATE TABLE gene (id SERIAL PRIMARY KEY, accession varchar(255) NOT NULL,
    nucleotide_sequence text NOT NULL)"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    # conn.close()
except Exception as e:
    print(e)
    conn.close()

try:
    print("Creating protein table....")
    sql = """CREATE TABLE protein (id SERIAL PRIMARY KEY,
    name varchar(255), ec_number varchar(11), aminoacid_sequence text NOT NULL, gene_id integer NOT NULL,
    FOREIGN KEY (gene_id) REFERENCES gene(id))"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    # conn.close()
except Exception as e:
    print(e)
    conn.close()

try:
    print("Creating Function table....")
    sql = """CREATE TABLE function (id SERIAL PRIMARY KEY,
    description text NOT NULL, protein_id integer NOT NULL,
    FOREIGN KEY (protein_id) REFERENCES protein(id))"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    # conn.close()
except Exception as e:
    print(e)
    conn.close()

try:
    print("Creating Splicing Variant table....")
    sql = """CREATE TABLE splicing_variant (id SERIAL PRIMARY KEY,
    variant_sequence text NOT NULL, gene_id integer NOT NULL, protein_id integer NOT NULL,
    FOREIGN KEY (gene_id) REFERENCES gene(id), FOREIGN KEY (protein_id) REFERENCES protein(id))"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    # conn.close()
except Exception as e:
    print(e)
    conn.close()

try:
    print("Creating Pathway table....")
    sql = """CREATE TABLE pathway (id SERIAL PRIMARY KEY,
    name varchar(255) NOT NULL, description text)"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    # conn.close()
except Exception as e:
    print(e)
    conn.close()

try:
    print("Creating Protein Pathway pivot table....")
    sql = """CREATE TABLE protein_pathway (id SERIAL PRIMARY KEY,
    protein_id integer NOT NULL, pathway_id integer NOT NULL,
    FOREIGN KEY (protein_id) REFERENCES protein(id),
    FOREIGN KEY (pathway_id) REFERENCES pathway(id))"""
    cursor.execute(sql)
    print("query executed")
    conn.commit()
    print("query commited")
    conn.close()
except Exception as e:
    print(e)
    conn.close()
