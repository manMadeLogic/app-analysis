# app-analysis
requirements:
python3
sqlite

files:
[appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps)

1. clone the repo and put the [appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps) files under app-analysis folder
2. run `python3 create_table.py`. It will create an app_db.db file under app-analysis folder
3. run `python3 load_data.py`. It will load both csv files to xxx and xxx tables. 
4. jupyter notebook
