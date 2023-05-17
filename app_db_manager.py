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
INSERT_METADATA_TABLE_STATEMENT = """
INSERT INTO apps_metadata VALUES({app_type}, {table_name}, {filename})
"""

CREATE_APP_STORE_APPS_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS app_store_apps_table
( PRIMARY KEY,
)
"""

CREATE_GOOGLE_PLAY_APPS_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS google_play_apps_table
( PRIMARY KEY,
)
"""


class AppDbManager:
    def __init__(self, app_store_file=DEFAULT_APP_STORE_FILENAME, google_play_file=DEFAULT_GOOGLE_PLAY_FILENAME):
        self.__init_metadata__()
        # self.__init_app_data__(app_store_file, google_play_file)

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def __init_metadata__(self):
        self.conn = sqlite3.connect(f'./{DB_NAME}')
        self.cur = self.conn.cursor()
        # create table metatable
        self.cur.execute(CREATE_METADATA_TABLE_STATEMENT)
        self.conn.commit()

    # def __init_app_data__(self, app_store_file, google_play_file):
    #     # check metadata
    #     apps_metadata_stored = self.cur.execute("SELECT app_type, filename FROM apps_metadata")
    #     store = dict()
    #     for row in apps_metadata_stored:
    #         store[row[0]] = row[1]
    #     print(store)
    #     # load data if empty or inconsistent
    #     # metadata list local
    #     # apps_metadata_local = [
    #     #     ('app_store', 'app_store_apps_table', self.app_store)
    #     # ]
    #     self.cur.execute(INSERT_METADATA_TABLE_STATEMENT.format(
    #         app_type='app_store', table_name='app_store_apps_table', filename=app_store_file)
    #     )
    #     self.cur.execute(INSERT_METADATA_TABLE_STATEMENT.format(
    #         app_type='google_play', table_name='google_play_apps_table', filename=google_play_file)
    #     )
    #     self.conn.commit()
    #     # self.cur.execute(CREATE_APP_STORE_APPS_TABLE_STATEMENT)
    #     # self.cur.execute(CREATE_GOOGLE_PLAY_APPS_TABLE_STATEMENT)


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
