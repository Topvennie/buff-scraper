import mysql.connector


class Database:
    def __init__(self, user: str, password: str, host: str, database: str):
        self._conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def executemany(self, sql: str, params: list = None):
        self.cursor.executemany(sql, params or ())

    def update_many(self, data_list: list, table_name: str):
        query = ''
        values = []
        for data_dict in data_list:
            if not query:
                columns = ', '.join(f'`{k}`' for k in data_dict)
                duplicates = ', '.join(f'{k}=VALUES({k})' for k in data_dict)
                place_holders = ', '.join('%s'.format(k) for k in data_dict)
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({place_holders})'
                query = f'{query} ON DUPLICATE KEY UPDATE {duplicates}'

            v = list(data_dict.values())
            values.append(v)

        self.executemany(query, values)
