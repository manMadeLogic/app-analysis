# app-analysis

files:
[appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps)

1. clone the repo and put the [appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps) files under app-analysis folder
2. run `pip3 install -r requirements.txt`.
3. run `python3 app_db_manager.py`. It will create an app_db.db file under app-analysis folder and load the data. run `python3 app_db_manager.py -a apple_file_name -g google_file_name` for other files than the question. The database will check if the file is the same as what's loaded in the tables and reload if the file name is different.
4. jupyter notebook `python3 -m notebook` and open "App analysis.ipynb"

design choices:
1. load file first and modify later vs modify before loading into the table: 
   1. Some data modification for Google's column (app size and released data) are taking the reading file process too long (takes more than 1 hour).
   2. it's easier for debugging the parsing logic with the original data stored.
2. individual tables vs single table:
   1. Benefit for individual tables is we can have different set of columns and both tables are more normalized and easy to see what fields are corresponding to each platforms. Benefit of individual table is we will only have 1 source, and it's easier for making changes to the downstream tables when we want to add new platforms.
   2. it's less likely to have silent errors when checking the data readiness if we have individual tables e.g. if we have a column `platform` to store if it's google or apple, then we set the value as null or the opposite value, then the check will have unexpected behaviors.
3. pre-process the genre vs store original and modify it later:
   1. although we already made a few modifications to the fields, we still want to keep the data as close to original as possible in case we want to look into analysis related to subtypes of games for Google play.
4. due to the time constrain, there should be more checks, error throwing and logging but I didn't get a chance to implement them all. Here is a list of most important ones
   1. check input file type
   2. catch and output errors for the queries
