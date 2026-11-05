import os
import re
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / 'agriculture_db.sqlite3'


def _normalize_sql(sql: str) -> str:
    if sql is None:
        return sql
    return re.sub(r'%s', '?', sql)


class SQLiteCursor:
    def __init__(self, connection, dictionary=False):
        self._native_cursor = connection.cursor()
        self._dictionary = dictionary
        if dictionary:
            self._native_cursor.row_factory = sqlite3.Row

    def execute(self, sql, params=()):
        normalized = _normalize_sql(sql)
        return self._native_cursor.execute(normalized, tuple(params) if params else ())

    def executemany(self, sql, seq_of_params):
        normalized = _normalize_sql(sql)
        return self._native_cursor.executemany(normalized, seq_of_params)

    @property
    def description(self):
        return self._native_cursor.description

    def fetchone(self):
        row = self._native_cursor.fetchone()
        if self._dictionary and row is not None:
            return dict(row)
        return row

    def fetchall(self):
        rows = self._native_cursor.fetchall()
        if self._dictionary:
            return [dict(row) for row in rows]
        return rows

    def close(self):
        self._native_cursor.close()


class SQLiteConnection:
    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row

    def execute(self, sql, params=()):
        native = self._conn.execute(_normalize_sql(sql), tuple(params) if params else ())
        return native

    def executemany(self, sql, seq_of_params):
        native = self._conn.executemany(_normalize_sql(sql), seq_of_params)
        return native

    def cursor(self, dictionary=False):
        return SQLiteCursor(self._conn, dictionary=dictionary)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def _seed_database(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS regions (region_id INTEGER PRIMARY KEY AUTOINCREMENT, region_name TEXT NOT NULL UNIQUE)')
    conn.execute('CREATE TABLE IF NOT EXISTS crops (crop_id INTEGER PRIMARY KEY AUTOINCREMENT, crop_name TEXT NOT NULL UNIQUE)')
    conn.execute('CREATE TABLE IF NOT EXISTS crop_records (record_id INTEGER PRIMARY KEY AUTOINCREMENT, crop_id INTEGER NOT NULL, region_id INTEGER NOT NULL, year INTEGER NOT NULL, cultivated_area_ha REAL NOT NULL, production_tonnes REAL NOT NULL, rainfall_mm REAL, FOREIGN KEY(crop_id) REFERENCES crops(crop_id), FOREIGN KEY(region_id) REFERENCES regions(region_id))')
    conn.execute('CREATE TABLE IF NOT EXISTS farmers (farmer_id INTEGER PRIMARY KEY AUTOINCREMENT, farmer_name TEXT NOT NULL, mobile_number TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, village TEXT NOT NULL)')
    conn.execute('CREATE TABLE IF NOT EXISTS farmer_records (farmer_record_id INTEGER PRIMARY KEY AUTOINCREMENT, farmer_id INTEGER NOT NULL, crop_id INTEGER NOT NULL, region_id INTEGER NOT NULL, year INTEGER NOT NULL, cultivated_area_ha REAL NOT NULL, production_tonnes REAL NOT NULL, rainfall_mm REAL, FOREIGN KEY(farmer_id) REFERENCES farmers(farmer_id), FOREIGN KEY(crop_id) REFERENCES crops(crop_id), FOREIGN KEY(region_id) REFERENCES regions(region_id))')

    regions = [
        (1, 'Andhra Pradesh'),
        (2, 'Telangana'),
        (3, 'Karnataka'),
        (4, 'Tamil Nadu'),
        (5, 'Maharashtra'),
    ]
    crops = [
        (1, 'Rice'),
        (2, 'Wheat'),
        (3, 'Cotton'),
        (4, 'Maize'),
        (5, 'Sugarcane'),
    ]
    crop_records = [
        (1, 1, 1, 2021, 1000.00, 4000.00, 850.00),
        (2, 1, 1, 2022, 1100.00, 4620.00, 900.00),
        (3, 1, 1, 2023, 1200.00, 5040.00, 880.00),
        (4, 1, 2, 2021, 800.00, 3200.00, 780.00),
        (5, 1, 2, 2022, 850.00, 3570.00, 820.00),
        (6, 1, 2, 2023, 900.00, 3870.00, 800.00),
        (7, 2, 3, 2021, 600.00, 1800.00, 650.00),
        (8, 2, 3, 2022, 650.00, 2080.00, 680.00),
        (9, 2, 3, 2023, 700.00, 2310.00, 700.00),
        (10, 3, 2, 2021, 700.00, 1400.00, 720.00),
        (11, 3, 2, 2022, 750.00, 1575.00, 760.00),
        (12, 3, 2, 2023, 800.00, 1680.00, 740.00),
        (13, 4, 4, 2021, 500.00, 2500.00, 900.00),
        (14, 4, 4, 2022, 550.00, 2860.00, 920.00),
        (15, 4, 4, 2023, 600.00, 3180.00, 910.00),
        (16, 5, 5, 2021, 400.00, 28000.00, 1000.00),
        (17, 5, 5, 2022, 420.00, 30240.00, 1050.00),
        (18, 5, 5, 2023, 450.00, 33300.00, 1020.00),
    ]

    if conn.execute('SELECT COUNT(*) FROM regions').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO regions (region_id, region_name) VALUES (?, ?)',
            regions
        )

    if conn.execute('SELECT COUNT(*) FROM crops').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO crops (crop_id, crop_name) VALUES (?, ?)',
            crops
        )

    if conn.execute('SELECT COUNT(*) FROM crop_records').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO crop_records '
            '(record_id, crop_id, region_id, year, cultivated_area_ha, '
            'production_tonnes, rainfall_mm) VALUES (?, ?, ?, ?, ?, ?, ?)',
            crop_records
        )

    conn.commit()


def connect():
    if not DB_PATH.exists():
        DB_PATH.touch()
    conn = SQLiteConnection(str(DB_PATH))
    _seed_database(conn)
    return conn


# expose a simple module-level connection for code that imports and uses it directly
connection = connect()
