import asyncio
from configparser import ConfigParser
import os
import shelve
import logging
import time

# Local Imports
from DarkPool import DarkPool
from RealTime import RealTime
from AlphaAI import AlphaAI
from Image import Image

# Reading data from conf.ini file....
################################################
config = ConfigParser()
config.read("conf.ini")


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)
# logging.disable(logging.WARNING)

purple_channel_name = config["DISCORD"]["channel_name_for_purple_data"]
golden_channel_name = config["DISCORD"]["channel_name_for_golden_data"]
black_channel_name = config["DISCORD"]["channel_name_for_black_data"]
no_color_channel_name = config["DISCORD"]["channel_name_for_no_color_data"]
ta_channel_name = config["DISCORD"]["channel_name_for_ta_bot"]
ai_channel_name = config["DISCORD"]["channel_name_for_ai_data"]
darkpool_channel_name = config["DISCORD"]["channel_name_for_darkpool_data"]
driver_path = config["CHROME"]["chromedriver_path"]
site_username = config["FLOWALGO"]["username"]
site_password = config["FLOWALGO"]["password"]
token = config["DISCORD"]["bot_token"]

url = "https://app.flowalgo.com/users/login"
data_file = shelve.open("./tmps/data")


target_channels_names = {
    "no_color": no_color_channel_name,
    "purple": purple_channel_name,
    "golden": golden_channel_name,
    "black": black_channel_name,
}
if not os.path.exists("./tmps"):
    os.mkdir("./tmps")

data_file = shelve.open("./tmps/data")

alpha_ai = AlphaAI(
    1,
    "alpha_ai",
    driver_path,
    url,
    site_username,
    site_password,
    token,
    ai_channel_name,
    data_file,
)
darkpool = DarkPool(
    10,
    "darkpool",
    driver_path,
    url,
    site_username,
    site_password,
    token,
    darkpool_channel_name,
    data_file,
)
realtime = RealTime(
    20,
    "realtime",
    driver_path,
    url,
    site_username,
    site_password,
    token,
    target_channels_names,
    data_file,
)
image = Image(
    40, "image", driver_path, url, site_username, site_password, token, ta_channel_name,
)


alpha_ai.start()
time.sleep(3)
realtime.start()
time.sleep(3)
darkpool.start()
time.sleep(3)
image.start()
