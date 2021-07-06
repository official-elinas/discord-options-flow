from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as seleniumExceptions
import discord
import asyncio
import logging
import threading
import os


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)
# logging.disable(logging.WARNING)


class Image(threading.Thread):
    def __init__(
        self,
        thread_id,
        thread_name,
        driver_path,
        url,
        username,
        password,
        token,
        target_channel_name,
    ):
        threading.Thread.__init__(self)
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.thread_name = thread_name
        self.url = url
        self.password = password
        self.username = username
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
        self.driver = webdriver.Chrome(driver_path, options=chrome_options)
        self.target_channel_name = target_channel_name
        self.target_channel = None
        self.KILL = False
        self.FLOW_LOGIN = False
        self.SCREEN_CLEAR = False

    async def login(self):
        logging.info("Logging-in to flowalgo!")
        self.driver.get(self.url)
        username_input = self.driver.find_element_by_xpath('//*[@id="login"]/input[1]')
        password_input = self.driver.find_element_by_xpath('//*[@id="login"]/input[2]')
        login_button = self.driver.find_element_by_xpath('//*[@id="login"]/input[3]')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="optionflow"]/div[2]/div[1]')
                )
            )
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="close-aai"]'))
            )
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app-controls"]/div/i')
                )
            )
        except seleniumExceptions.TimeoutException:
            pass
        self.FLOW_LOGIN = True

    async def send(self, desc, signal_type):
        if signal_type == "long":
            clr = discord.Color.blue()
        else:
            clr = discord.Color.red()
        embd = discord.Embed(title="Golden Harvest AI", type="rich", description=desc, color=clr)
        if not self.target_channel:
            self.target_channel = discord.utils.find(
                lambda m: m.name == self.target_channel_name,
                self.client.guilds[0].text_channels,
            )
        await self.target_channel.send(embed=embd)

    async def wait_until_login(self):
        while not self.FLOW_LOGIN:
            await asyncio.sleep(1)

    async def get_screenshot(self, location, search_str):
        if not self.FLOW_LOGIN:
            await self.login()
            await self.wait_until_login()
        if not self.SCREEN_CLEAR:
            try:
                logging.info("Waiting for element...")
                popup = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="data-agreement-notice"]/button')
                    )
                )
                chat_btn = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="chat"]/div[1]/div/i[2]')
                    )
                )
                ai_btn = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="close-aai"]'))
                )
                darkpool_btn = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="darkflow"]/div[1]/div[1]/i[2]')
                    )
                )

                fullscreen_btn = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app-controls"]/div/i')
                    )
                )
                search_box = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="filter-flow"]/div/input')
                    )
                )
            finally:
                logging.info("Creating the image ...")
                try:
                    popup.click()
                except seleniumExceptions.ElementNotInteractableException:
                    pass
                try:
                    chat_btn.click()
                    ai_btn.click()
                    darkpool_btn.click()
                    fullscreen_btn.click()
                    self.SCREEN_CLEAR = True
                except seleniumExceptions.ElementNotInteractableException:
                    await self.get_screenshot(location, search_str)
                    return location

        search_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="filter-flow"]/div/input')
            )
        )
        search_box.clear()
        search_box.send_keys(search_str)
        await asyncio.sleep(1)
        self.driver.get_screenshot_as_file(location)
        return location

    async def start_bot(self):
        client = discord.Client()
        self.client = client

        @staticmethod
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            if message.content.startswith(".h "):
                logging.info("Command Received!")
                content = message.content
                content = content.split(" ")
                to_search = content[1]
                channel_name = message.channel.name
                logging.info(
                    f"received: {channel_name} | have : {self.target_channel_name}"
                )
                if channel_name == self.target_channel_name:
                    logging.info("Image requested !")
                    await message.channel.send(
                        "Please wait while processing your request!"
                    )
                    ss = await self.get_screenshot("./tmps/ss.png", to_search)
                    await message.channel.send(file=discord.File(ss))
                    if os.path.exists(ss):
                        os.remove(ss)
                    logging.info("Image Sent!")

        client.loop.create_task(self.login())
        await client.start(self.token)

    def run(self):
        self.loop.create_task(self.start_bot())
        try:
            self.loop.run_forever()
        except RuntimeError:
            pass
