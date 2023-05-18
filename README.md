# app-analysis

files:
[appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps)

1. clone the repo and put the [appleAppData.csv](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps) and [Google-Playstore.csv](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps) files under app-analysis folder
2. run `pip3 install -r requirements.txt`.
3. run `python3 app_db_manager.py`. It will create an app_db.db file under app-analysis folder and load the data.
4. jupyter notebook `python3 -m notebook` and open "App analysis.ipynb"
