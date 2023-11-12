import glob
import pandas as pd
from bs4 import BeautifulSoup
import configparser

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

seed_channels_dir = config['seed_channels_parsing']['html_path']
save_path = config['seed_channels_parsing']['save_path']

files = glob.glob(seed_channels_dir)
print("Processing files from: ", seed_channels_dir)
print("Files will be saved in: ", save_path)
print("Initial htmls found: ", files)

dfs = []
for file_name in files:
    print(file_name)
    seed_channels_df = pd.read_html(file_name)[0]
    with open(file_name) as f:
        lines = f.readlines()
    soup = BeautifulSoup("".join(lines), "html.parser")
    job_elements = soup.find_all("div", class_="channel-name flex items-center channel-name_M")
    ids = [s['href'].split('/')[-1].split('-')[0] for s in soup.find_all('a', class_='channel-name__title')]
    names = ["-".join(s['href'].split('/')[-1].split('-')[1:]) for s in
             soup.find_all('a', class_='channel-name__title')]
    titles = [s.text for s in soup.find_all('a', class_='channel-name__title')]

    seed_channels_df["names"] = names
    seed_channels_df["ids"] = ids
    seed_channels_df["titles"] = titles
    seed_channels_df["country"] = file_name.split("/")[-1][:2]
    dfs.append(seed_channels_df)

seed_df = pd.concat(dfs).drop_duplicates("ids").reset_index(drop=True)
seed_df = seed_df[["names", "ids", "titles", "country", "Subscribers", "Category"]]
seed_df.columns = ["names", "ids", "titles", "country", "n_subscribers", "category"]
seed_df.to_csv(save_path, index=False)
