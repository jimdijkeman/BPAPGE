
# BlastDBTool Command Line Interface


## Requirements
- Python 3.10.12 or above
    - [Biopython](https://biopython.org/)
    - [psycopg2](https://pypi.org/project/psycopg2/)
- PostgreSQL
## Installation


```bash
  git clone https://github.com/jimdijkeman/BlastDBTool.git
  cd BlastDBTool
  pip3 install -r requirements.txt
```
Configure `database.ini` as shown below.
## Environment Variables

To use this application, make sure the proper variables have been set in `database.ini`:

```
[postgresql]
host=hostname
dbname=databasename
user=username
password=password (indien nodig)
```

## Usage/Examples

```bash
usage: main.py [-h] [--blast QUERY_FILE DB_FILE] [--insert] [--get_pathways] [--create_tables] [--drop_tables]

options:
  -h, --help            show this help message and exit
  --blast QUERY_FILE DB_FILE
                        Run BLAST
  --insert              Insert gene and protein data
  --get_pathways        Retrieve pathways
  --create_tables       Create all tables
  --drop_tables         Drop all tables
```

### Example:
```bash
python3 main.py --create_tables --blast seq.fa proteoomdb.fa --insert --get_pathways
```


## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)


