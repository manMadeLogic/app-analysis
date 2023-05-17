import argparse
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
"""
SELECT_METADATA_TABLE_STATEMENT = """
SELECT app_type, filename FROM apps_metadata
"""

# TODO
CREATE_APP_STORE_APPS_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS app_store_apps_table
( PRIMARY KEY,
)
"""
app_store_column_mapper = {

}

CREATE_GOOGLE_PLAY_APPS_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS google_play_apps_table
( PRIMARY KEY,
)
"""
google_play_column_mapper = {

}


class AppDbManager:
    def __init__(self, app_store_file=DEFAULT_APP_STORE_FILENAME, google_play_file=DEFAULT_GOOGLE_PLAY_FILENAME):
        self.conn = sqlite3.connect(f'./{DB_NAME}')
        self.cur = self.conn.cursor()
        self.__init_metadata__()
        self.__init_app_data__(app_store_file, google_play_file)

    def __exit__(self, ext_type, exc_value, traceback):
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

    def __init_app_data__(self, app_store_file, google_play_file):
        # check metadata
        apps_metadata_stored = self.cur.execute(SELECT_METADATA_TABLE_STATEMENT)
        store = dict()
        for row in apps_metadata_stored:
            store[row[0]] = row[1]
        if 'app_store' not in store or store['app_store'] != app_store_file:
            self.load_data('app_store', app_store_file)
        if 'google_play' not in store or store['google_play'] != google_play_file:
            self.load_data('google_play', google_play_file)

    def load_data(self, app_type, filename):
        # load data and update metadata
        if app_type == 'app_store':
            table_sql = CREATE_APP_STORE_APPS_TABLE_STATEMENT
            table_column_mapper = app_store_column_mapper
        elif app_type == 'google_play':
            table_sql = CREATE_APP_STORE_APPS_TABLE_STATEMENT
            table_column_mapper = google_play_column_mapper
        # read files and insert
        
        # update metadata
        self.cur.execute(REPLACE_METADATA_TABLE_STATEMENT.format(
            app_type=app_type, table_name=f'{app_type}_apps_table', filename=filename)
        )
        self.conn.commit()
        # self.cur.execute(CREATE_APP_STORE_APPS_TABLE_STATEMENT)
        # self.cur.execute(CREATE_GOOGLE_PLAY_APPS_TABLE_STATEMENT)


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
    db = AppDbManager(app_store_file=args.app_store_filename, google_play_file=args.google_play_filename)
