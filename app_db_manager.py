import argparse
import pandas as pd
import sqlite3
import subprocess

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
CREATE_APP_STORE_STAGING_STATEMENT = """
CREATE TABLE IF NOT EXISTS app_store_staging
(
    app_id text PRIMARY KEY,
    app_name text,
    appStore_url text,
    primary_genre text,
    content_rating text,
    size_bytes bigint,
    required_ios_version text,
    released text,
    updated text,
    version text,
    price text,
    currency text,
    free int,
    developerid text,
    developer text,
    developer_url text,
    developer_website text,
    average_user_rating real,
    reviews int
)
"""
CREATE_GOOGLE_PLAY_STAGING_STATEMENT = """
CREATE TABLE IF NOT EXISTS google_play_staging
(
    app_name text,
    app_id text PRIMARY KEY,
    category text,
    rating real,
    rating_count int,
    installs int,
    minimum_installs int,
    maximum_installs int,
    free int,
    price real,
    currency text,
    size text,
    minimum_android text,
    developer_d text,
    developer_website text,
    developer_email text,
    released text
)
"""
INSERT_APP_STORE_APP_TABLE_STATEMENT = """
INSERT INTO app_store_apps_table
(app_id, app_name, category, size_in_mb, released_date, rating, rating_count) 
SELECT
    app_id,
    app_name,
    primary_genre AS category,
    size_bytes * 1.0 / 1024 / 1024 AS size_in_mb,
    CASE
        WHEN released = '' THEN NULL
        ELSE SUBSTR(released, 1, 10)
    END AS released_date,
    average_user_rating AS rating,
    reviews AS rating_count
FROM app_store_staging
"""
INSERT_GOOGLE_PLAY_APP_TABLE_STATEMENT = """
INSERT INTO google_play_apps_table
(app_id, app_name, category, size_in_mb, released_date, rating, rating_count) 
SELECT
    app_id,
    app_name,
    category,
    CASE
        WHEN size IN ('Varies with device', '') THEN NULL
        WHEN SUBSTR(size, -1) = 'k' THEN CAST(REPLACE(SUBSTR(size, 1, LENGTH(size)-1), ',', '') AS REAL) / 1024
        WHEN SUBSTR(size, -1) = 'M' THEN CAST(REPLACE(SUBSTR(size, 1, LENGTH(size)-1), ',', '') AS REAL)
        WHEN SUBSTR(size, -1) = 'G' THEN CAST(REPLACE(SUBSTR(size, 1, LENGTH(size)-1), ',', '') AS REAL) * 1024
    END AS size_in_mb,
    SUBSTR(released,-4) || '-' ||
      CASE SUBSTR(released, 1, 3)
         WHEN 'Jan' THEN '01'
         WHEN 'Feb' THEN '02'
         WHEN 'Mar' THEN '03'
         WHEN 'Apr' THEN '04'
         WHEN 'May' THEN '05'
         WHEN 'Jun' THEN '06'
         WHEN 'Jul' THEN '07'
         WHEN 'Aug' THEN '08'
         WHEN 'Sep' THEN '09'
         WHEN 'Oct' THEN '10'
         WHEN 'Nov' THEN '11'
         WHEN 'Dec' THEN '12'
      END || '-' ||
      CASE 
         WHEN LENGTH(released) = 12 THEN SUBSTR(released, 5, 2)
         WHEN LENGTH(released) = 11 THEN '0' || SUBSTR(released, 5, 1)
      END
    AS released_date,
    rating,
    rating_count
FROM google_play_staging
"""


class AppDbManager:
    def __init__(self,
                 no_load=True,
                 app_store_file=DEFAULT_APP_STORE_FILENAME,
                 google_play_file=DEFAULT_GOOGLE_PLAY_FILENAME
                 ):
        print(f"__init__ function with app_store_file={app_store_file}, google_play_file={google_play_file}")
        self.conn = sqlite3.connect(DB_NAME)
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
            self.load_data('app_store', app_store_file)
        if 'google_play' not in store or store['google_play'] != google_play_file:
            self.load_data('google_play', google_play_file)

    # load data and update metadata
    def load_data(self, app_type, filename):
        # read files and insert
        self.__load_file__(app_type, filename)

        # update metadata
        self.cur.execute(REPLACE_METADATA_TABLE_STATEMENT.format(
            app_type=app_type, table_name=f'{app_type}_apps_table', filename=filename)
        )
        self.conn.commit()

    def __load_file__(self, app_type, filename):
        print(f"__load_file__ function with app_type={app_type} and filename={filename}")
        self.cur.execute(CREATE_APPS_TABLE_STATEMENT.format(table_name=f"{app_type}_apps_table"))
        # create staging table
        if app_type == 'app_store':
            self.cur.execute(CREATE_APP_STORE_STAGING_STATEMENT)
        elif app_type == 'google_play':
            self.cur.execute(CREATE_GOOGLE_PLAY_STAGING_STATEMENT)

        # load data to staging table
        subprocess.run(
            ['sqlite3', 'app_db.db', '-cmd', f'.import --csv --skip 1 {filename} {app_type}_staging', '.quit'],
            capture_output=True)

        # delete the final table and insert staging to the final table
        self.cur.execute(f"DELETE FROM {app_type}_apps_table")
        if app_type == 'app_store':
            self.cur.execute(INSERT_APP_STORE_APP_TABLE_STATEMENT)
        elif app_type == 'google_play':
            self.cur.execute(INSERT_GOOGLE_PLAY_APP_TABLE_STATEMENT)

        # drop the staging table
        self.cur.execute(f"DROP TABLE {app_type}_staging")
        self.conn.commit()

    def run_select(self, query):
        result = self.conn.execute(query)
        return list(result)

    def run_select_pd(self, query):
        return pd.read_sql_query(query, self.conn)


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
