import joblib
import feedparser
import configparser
from tqdm import tqdm
import schedule
import time


rss_feed_data = {
    "NYT_Ukraine": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/topic/destination/ukraine/rss.xml",
    "NYT_Russia": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/topic/destination/russia/rss.xml",
    "NYT_General": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "Pravda": "https://www.pravda.com.ua/rss/",
    "Unian": "https://rss.unian.net/site/news_ukr.rss",
    "Unian_eng": "https://rss.unian.net/site/news_eng.rss",
    "korespondent_net": "http://k.img.com.ua/rss/ru/all_news2.0.xml",
    "gordon": "https://gordonua.com/xml/rss_category/top.html",
    "NV": "https://nv.ua/rss/all.xml",
    "espreso": "https://espreso.tv/rss",
    "censor": "https://assets.censor.net/rss/censor.net/rss_ru_news.xml",
    "lenta": "https://lenta.ru/rss",
    "vesti": "https://www.vesti.ru/vesti.rss",
    "RT": "https://www.rt.com/rss/",
    "Meduza": "https://meduza.io/rss/all",
    "TASS": "http://tass.com/rss/v2.xml",
    "komersant": "https://www.kommersant.ru/RSS/main.xml",
    "FT_international": "https://www.ft.com/rss/home/international",
    "FT_ukraine": "https://www.ft.com/ukraine?format=rss",
    "FOX_all": "https://moxie.foxnews.com/google-publisher/world.xml",
    "FOX_politics": "https://moxie.foxnews.com/google-publisher/politics.xml",
    "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Guardian": "https://www.theguardian.com/world/rss",
    "Independent": "https://www.independent.co.uk/news/world/rss",
    "EL_PAIS": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "espana": "https://rss.elconfidencial.com/espana/",
    "DW": "https://rss.dw.com/rdf/rss-en-all",
    "ZEIT": "http://newsfeed.zeit.de/index",
    "france24": "https://www.france24.com/en/rss",
    "euronews": "https://www.euronews.com/rss",
    "euronews_ru": "https://ru.euronews.com/rss",
    "economist": "https://www.economist.com/latest/rss.xml",
    "mirror": "https://www.mirror.co.uk/news/world-news/?service=rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "skynews": "https://feeds.skynews.com/feeds/rss/world.xml",
    "daily_mail": "https://www.dailymail.co.uk/news/worldnews/index.rss",
    "politico": "https://www.politico.com/rss/politicopicks.xml",
    "politico_eu": "https://www.politico.eu/feed/",
    "time": "https://time.com/feed/",
}


class RSSFeedParser:
    def __init__(self, url: str, name: str, data_path: str):
        self.url = url
        self.name = name
        self.data_path = data_path
        self.feed = []
    
    def parse(self) -> list:
        try:
            # Code to parse the RSS feed
            # Parse the feed
            new_feed = feedparser.parse(self.url)['entries']
            # merge with existing feed
            existing_ids = set([item['id'] for item in self.feed])
            self.feed = self.feed + [item for item in new_feed if item['id'] not in existing_ids]
            return self.feed
        except:
            print(f"Error in parsing the feed for {self.name}")
            pass

    def load_feed(self,):
        # Code to load the RSS feed
        try:
            self.feed = joblib.load(self.data_path + "/" + self.name + '.data')
        except:
            self.feed = []
    
    def save_feed(self,):
        # Code to save the RSS feed
        joblib.dump(self.feed, self.data_path + "/" + self.name + '.data')






def job():
    print("Running the job")
    data_path = "data/news_feed"
    rss_feeds = rss_feed_data   # TODO: Move to some constants file     
    
    # Assuming rss_feeds is a list of RSSFeed objects
    for rss_feed_name, rss_feed_url in tqdm(rss_feeds.items()):
        rss_feed_parser = RSSFeedParser(url=rss_feed_url, name=rss_feed_name, data_path=data_path)
        rss_feed_parser.load_feed()
        rss_feed_parser.parse()
        rss_feed_parser.save_feed()

# Schedule the job every 30 minutes
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    
