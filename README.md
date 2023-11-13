# Telegram parsing experiments
Some experiments with parsing information from telegram channels. 

In order to run a script you need the `config.ini` file with your configurations.
You can get your configurations by creating a [telegram app here](https://my.telegram.org/apps).

Example of `config.ini` file: 
```commandline
[Telegram]
# no need for quotes

# you can get telegram development credentials in telegram API Development Tools
api_id = [some_id]
api_hash = [some_hash]

# use full phone number including + and country code
phone = [some_number]
username = [some_user_name]
```


## Proposed parsing pipeline: 

- Define the seed channels:
  - Make sure you have the correct config setup for `seed_channels_parsing` block
  - We use top-200 popular pages from RU and UA as seed channels: 
    - Go to the [https://telemetr.io/](https://telemetr.io/en/country/ukraine?channelType=public&page=1) and download the html of the page with channels rating
    - Repeat it for as many pages as needed (in our case we used two pages from Ukraine and Russia (~400 seed channels in total))
  - Run the script to parse htmls and collect .csv: ```python modules/get_seed_channels.py```
- Parse the messages from the channels:
  - Make sure you have the correct config setup for `seed_channels_parsing` block
  - Parse the messages from the seed channels to the unified directory: ```python modules/get_seed_channels_data.py```

### ToDo: 
- [ ] Create the script for snowball parsing
- [ ] Create the script for comments parsing
- [ ] Create the script for channel user data parsing
