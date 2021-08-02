import random
import time
import requests

from settings import settings
from threading import Timer
from random import shuffle
from fake_useragent import UserAgent
from streamlink import Streamlink

from dv_twitch_viewer.logger import get_logger
from dv_twitch_viewer import constants
from collections import Counter
from typing import List
from dv_twitch_viewer.utils import get_proxies, get_ua


class Orchestrator:
    def __init__(self):
        """Class Constructor"""
        self._logger = get_logger(self.__class__.__name__)

    def start(self):
        """Start orchestrator and submodules"""
        self._logger.info("Starting orchestrator...")

    def stop(self):
        """Stop orchestrator and submodules"""
        self._logger.info("Stopping orchestrator...")

    def run(self):
        """Run orchestrator process"""
        self._logger.info("Running orchestrator...")
        twitch = TwitchOrchestrator()
        all_proxies = twitch.start()
        for i in range(0, len(all_proxies)):
            threaded = Timer(1, self.get_url, args=(all_proxies[i],))
            threaded.start()

    def get_url(self, proxy_data):
        session = Streamlink()
        session.set_option("http-proxy", proxy_data['proxy'])
        session.set_option("https-proxy", proxy_data['proxy'])
        session.set_option("http-headers",
                           {'User-Agent': proxy_data['user_agent'], "Client-ID": "ewvlchtxgqq88ru9gmfp1gmyt6h2b93"})

        streams = session.streams(proxy_data['channel'])
        current_url = streams['worst'].url
        self._logger.info(f"creating viewer with {proxy_data['proxy']}", )
        return self.run_viewer(proxy_data, current_url)

    def run_viewer(self, proxy_data, current_url):

        timeout = 500  # [seconds]
        timeout_start = time.time()

        while time.time() < timeout_start + timeout:
            time.sleep(2)
            self.open_url(proxy_data=proxy_data, current_url=current_url)
        else:
            self._logger.info(f"Stopping viewer with {proxy_data['proxy']}", )
            self.get_url(proxy_data)

    def open_url(self, proxy_data, current_url):
        try:
            current_proxy = {"http": proxy_data['proxy'], "https": proxy_data['proxy']}

            with requests.Session() as s:
                response = s.head(current_url, proxies=current_proxy, headers=proxy_data['headers'])
                self._logger.info(
                    f"Sent HEAD request with {current_proxy['http']} | "
                    f"{response.status_code}")
        except BaseException as error:
            self._logger.error('An exception occurred: {}'.format(error))


class TwitchOrchestrator:
    def __init__(self):
        """Class Constructor"""
        self._logger = get_logger(self.__class__.__name__)

    def start(self):
        """Start twitch viewer and submodules"""

        channel_url = settings.TWITCH_URL
        self._logger.info('channel url: {}'.format(channel_url))

        start_time = time.time()
        proxies = get_proxies()
        lines = get_ua()
        all_proxies = []

        for p in proxies:
            user_agent = random.choice(lines)

            headers = {'User-Agent': user_agent, 'Connection': 'Keep-Alive', 'referrer': random.choice(constants.REFS),
                       'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': random.choice(constants.LENG),
                       'Pragma': 'no-cache'
                       }

            all_proxies.append({'proxy': p, 'time': start_time, 'url': '', 'channel': channel_url, 'headers': headers,
                                'user_agent': user_agent})

        self._logger.info("Preparing request to send")
        return all_proxies
