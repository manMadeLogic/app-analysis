# app-analysis
requirements:
python3
sqlite

files:
[appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps)

1. clone the repo and put the [appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps) files under app-analysis folder
2. run `pip3 install -r requirements.txt`
3. run `python3 create_table.py`. It will create an app_db.db file under app-analysis folder
4. run `python3 load_data.py`. It will load both csv files to xxx and xxx tables.
5. jupyter notebook `python3 -m notebook`

design choices:
1. single table vs individual tables 
2. same schema vs different schemas
3. pre-process the genre vs store original and modify it later