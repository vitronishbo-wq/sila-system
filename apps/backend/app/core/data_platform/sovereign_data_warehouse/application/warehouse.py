class SovereignDataWarehouse:

    def __init__(self):
        self.tables = {}

    def create_table(self, table_name):
        self.tables[table_name] = []

    def insert(self, table_name, row):
        self.tables[table_name].append(row)

    def query(self, table_name):
        return self.tables.get(table_name, [])