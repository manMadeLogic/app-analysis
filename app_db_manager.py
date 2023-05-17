import argparse
import csv
import dateparser
import sqlite3

DB_NAME = "app_db.db"
DEFAULT_APP_STORE_FILENAME = "appleAppData.csv"
DEFAULT_GOOGLE_PLAY_FILENAME = "Google-Playstore.csv"
CREATE_METADATA_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS apps_metadata
(
    app_type text PRIMARY KEY,
    table_name text,
    filename text
)
"""
REPLACE_METADATA_TABLE_STATEMENT = """
REPLACE INTO apps_metadata (app_type, table_name, filename)
VALUES ('{app_type}', '{table_name}', '{filename}')
"""  # todo
SELECT_METADATA_TABLE_STATEMENT = """
SELECT app_type, filename FROM apps_metadata
"""

CREATE_APPS_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    app_id text PRIMARY KEY,
    app_name text,
    category text,
    size_in_mb real,
    released_date text,
    rating real,
    rating_count int
)
"""
INSERT_APP_TABLE_STATEMENT = """
INSERT INTO {table_name}
(app_id, app_name, category, size_in_mb, released_date, rating, rating_count) 
VALUES (?, ?, ?, ?, ?, ?, ?)
"""


def modify_app_store_row(row):
    return (
        row['App_Id'],
        row['App_Name'],
        row['Primary_Genre'],
        int(row['Size_Bytes']) / 1024 / 1024 if row['Size_Bytes'] else None,
        row['Released'][:10],
        float(row['Average_User_Rating']),
        int(row['Reviews']),
    )


def modify_google_play_row(row):
    size = None
    if row['Size'] == 'Varies with device' or not row['Size']:
        size = None
    elif row['Size'][-1] == 'k':
        size = float(row['Size'][:-1].replace(',', '')) / 1024
    elif row['Size'][-1] == 'M':
        size = float(row['Size'][:-1].replace(',', ''))
    elif row['Size'][-1] == 'G':
        size = float(row['Size'][:-1].replace(',', '')) * 1024
    else:
        print(row['Size'])

    return (
        row['App Id'],
        row['App Name'],
        row['Category'],
        size,
        dateparser.parse(row['Released']).strftime('%Y-%m-%d') if row['Released'] else None,
        float(row['Rating']) if row['Rating Count'] and row['Rating'] else 0,
        int(row['Rating Count']) if row['Rating Count'] and row['Rating'] else 0,
    )


class AppDbManager:
    def __init__(self,
                 no_load=True,
                 app_store_file=DEFAULT_APP_STORE_FILENAME,
                 google_play_file=DEFAULT_GOOGLE_PLAY_FILENAME
                 ):
        print(f"__init__ function with app_store_file={app_store_file}, google_play_file={google_play_file}")
        self.conn = sqlite3.connect(f'./{DB_NAME}')
        self.cur = self.conn.cursor()
        self.__init_metadata__()
        if not no_load:
            self.__init_app_data__(app_store_file, google_play_file)

    def __exit__(self, ext_type, exc_value, traceback):
        print(f"__exit__ function")
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def __init_metadata__(self):
        # create table metatable
        self.cur.execute(CREATE_METADATA_TABLE_STATEMENT)
        self.conn.commit()

    # check metadata
    def __init_app_data__(self, app_store_file, google_play_file):
        apps_metadata_stored = self.cur.execute(SELECT_METADATA_TABLE_STATEMENT)
        store = dict()
        for row in apps_metadata_stored:
            store[row[0]] = row[1]
        # update if different
        if 'app_store' not in store or store['app_store'] != app_store_file:
            column_modifier = modify_app_store_row
            self.load_data('app_store', column_modifier, app_store_file)
        if 'google_play' not in store or store['google_play'] != google_play_file:
            column_modifier = modify_google_play_row
            self.load_data('google_play', column_modifier, google_play_file)

    def __load_file__(self, table_name, column_modifier, filename):
        print(f"__load_file__ for {table_name} with filename: {filename}")
        # create table if exist
        self.cur.execute(CREATE_APPS_TABLE_STATEMENT.format(table_name=table_name))

        # delete table
        self.cur.execute(f"DELETE FROM {table_name}")

        # read files
        with open(filename, 'r') as f:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(f)
            store = [column_modifier(r) for r in dr]

        # insert
        print("insert")
        self.cur.executemany(INSERT_APP_TABLE_STATEMENT.format(table_name=table_name), store)
        self.conn.commit()

    # load data and update metadata
    def load_data(self, app_type, column_modifier, filename):
        # read files and insert
        self.__load_file__(f'{app_type}_apps_table', column_modifier, filename)

        # update metadata
        self.cur.execute(REPLACE_METADATA_TABLE_STATEMENT.format(
            app_type=app_type, table_name=f'{app_type}_apps_table', filename=filename)
        )
        self.conn.commit()

    def run_select(self, query):
        result = self.conn.execute(query)
        return list(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='app_db_manager',
        description='Handles BD related operations')
    parser.add_argument('-a', '--app_store_filename',
                        nargs='?',
                        default=DEFAULT_APP_STORE_FILENAME,
                        help='csv files name for appStore')
    parser.add_argument('-g', '--google_play_filename',
                        nargs='?',
                        default=DEFAULT_GOOGLE_PLAY_FILENAME,
                        help='csv files name for google play')  # option that takes a value
    args = parser.parse_args()
    db = AppDbManager(no_load=False, app_store_file=args.app_store_filename, google_play_file=args.google_play_filename)
