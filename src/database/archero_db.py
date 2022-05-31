import sqlite3
import io
import os
from pathlib import Path


class ArcheroDb:
    def __init__(self, db_name=None):
        if db_name is None:
            self.__set_db_name(file_name='archero_database.db')
        else:
            self.__set_db_name(file_name=db_name)
        # print(f'db_name [{self.db_name}]')
        self.__conn = None
        self.__cursor = None
        self.__backup_file = 'archero_backup.sql'
        self.__table_eggs = 'EGGS'
        self.__table_sql_seq = 'sqlite_sequence'

    def dump(self):
        print(f'conn [{self.__conn}]')
        print(f'cursor [{self.__cursor}]')

    def create_db_file(self):
        self.__connect()
        self.__close_conn()

    def __set_db_name(self, file_name):
        self.db_name = os.path.join(Path(__file__).parent.parent.parent, file_name)

    def __connect(self):
        self.__conn = sqlite3.connect(self.db_name)
        self.__cursor = self.__conn.cursor()

    def __commit(self):
        if self.__conn:
            self.__conn.commit()

    def __close_conn(self):
        if self.__conn:
            self.__conn.close()

    def get_row_count(self):
        if self.__cursor:
            return self.__cursor.rowcount
        else:
            return 0

    def list_all_tables(self, debug=False):
        self.__connect()
        self.__cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        all_tables = self.__cursor.fetchall()
        if debug:
            print('Tabelas:')
            for tabela in all_tables:
                print('> [%s]' % tabela)
        self.__close_conn()
        return all_tables

    def list_columns_from_table(self, table_name, debug=False):
        self.__connect()
        self.__cursor.execute('PRAGMA table_info({})'.format(table_name))
        cols = [tupla[1] for tupla in self.__cursor.fetchall()]
        if debug:
            print(f'Colunas tabela {table_name}: {cols}')
        self.__close_conn()
        return cols

    def export_db(self):
        self.__connect()
        with io.open(self.__backup_file, 'w') as f:
            for linha in self.__conn.iterdump():
                f.write('%s\n' % linha)
        self.__close_conn()

    def create_table_eggs(self):
        self.__connect()
        self.__cursor.execute(f"""
        CREATE TABLE {self.__table_eggs} (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            image BLOOB,
            name_en TEXT NOT NULL,
            name_pt TEXT,
            type_mob BOOLEAN NOT NULL,
            type_boss BOOLEAN NOT NULL,
            collected BOOLEAN NOT NULL,
            stars INTEGER NOT NULL,
            find_normal_chapters TEXT,
            find_hero_chapters TEXT,
            find_events TEXT,
            to_hatch INTEGER,
            natural_hatch INTEGER,
            quest1 INTEGER,
            quest1_unlocked BOOLEAN,
            quest2 INTEGER,
            quest2_unlocked BOOLEAN,
            train_cost TEXT,
            train_stats TEXT,
            train_stats_stars TEXT,
            competition_available BOOLEAN,
            competition_stats TEXT,
            date_created TIMESTAMP NOT NULL,
            date_updated TIMESTAMP
        );
        """)
        self.__commit()
        self.__close_conn()

    """
    ===============================================================================================
    INSERT
    ===============================================================================================
    """
    def insert_egg(self, egg_insert):
        fields, values = egg_insert.get_fields()
        self.__connect()
        self.__cursor.execute(f"""
        INSERT INTO {self.__table_eggs} {fields}
        VALUES ({values})
        """, egg_insert.to_tuple_db())
        self.__commit()
        self.__close_conn()

    """
    ===============================================================================================
    SELECT
    ===============================================================================================
    """
    def select_autoincrement(self, debug=False):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.__table_sql_seq};
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    def select_all_eggs(self, debug=False, sort_by_en=True):
        sort_key = 'name_en' if sort_by_en else 'name_pt'
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.__table_eggs} ORDER BY {sort_key};
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    """
    ===============================================================================================
    UPDATE
    ===============================================================================================
    """
    def update_egg(self, egg):
        self.__connect()
        self.__cursor.execute(f"""
        UPDATE {self.__table_eggs}
        SET
        {egg.update_fields()}
        WHERE
        id = {egg.id};
        """, egg.to_tuple_db())
        rows = self.get_row_count()
        self.__commit()
        self.__close_conn()
        return rows

    """
    ===============================================================================================
    DELETE
    ===============================================================================================
    """
    def delete_all_eggs(self, reset_seq=False):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.__table_eggs};
        """)
        self.__commit()
        self.__close_conn()
        if reset_seq:
            self.reset_autoincrement_table_eggs()

    """
    ===============================================================================================
    RESET AUTOINCREMENT
    ===============================================================================================
    """
    def __reset_autoincrement(self, table_name):
        self.__connect()
        self.__cursor.execute(f"""
        UPDATE {self.__table_sql_seq} SET seq = 0 WHERE name = '{table_name}';
        """)
        self.__commit()
        self.__close_conn()

    def reset_autoincrement_table_eggs(self):
        self.__reset_autoincrement(table_name=self.__table_eggs)
