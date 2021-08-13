import random
import time
import requests

from settings import settings
from streamlink import Streamlink
from threading import Thread
from dv_twitch_viewer.logger import get_logger
from dv_twitch_viewer import constants
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
        threads = []

        for i in range(0, len(all_proxies)):
            threaded = Thread(target=self.get_url, args=(all_proxies[i],))
            threads.append(threaded)

        # Start all threads
        for x in threads:
            x.start()

        # Wait for all of them to finish
        for x in threads:
            x.join()

    def get_url(self, proxy_data):

        self._logger.info(f"creating viewer with {proxy_data['proxy']}", )

        timeout = 900  # 15 minutes in seconds
        timeout_start = time.time()

        while time.time() < timeout_start + timeout:

            session = Streamlink()
            session.set_option("http-proxy", proxy_data['proxy'])
            session.set_option("https-proxy", proxy_data['proxy'])
            session.set_option("http-headers",
                               {'User-Agent': proxy_data['user_agent'], 'Client-ID': 'b31o4btkqth5bzbvr9ub2ovr79umhh'})

            streams = session.streams(proxy_data['channel'])
            if streams:
                current_url = streams['worst'].url
                self.open_url(proxy_data=proxy_data, current_url=current_url)

            time.sleep(5)

    def open_url(self, proxy_data, current_url):
        try:
            current_proxy = {"http": proxy_data['proxy'], "https": proxy_data['proxy']}

            r = requests.get(current_url, proxies=current_proxy, headers=proxy_data['headers'])

            self._logger.info(
                f"Sent HEAD request with {current_proxy['http']} | "
                f"{r.status_code}")

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

        self._logger.info('Creating views: {}'.format(len(proxies)))

        lines = get_ua()
        all_proxies = []

        for idx, p in enumerate(proxies):
            user_agent = lines[idx]

            headers = {'User-Agent': user_agent,
                       'Connection': constants.CONNECTION,
                       'referrer': random.choice(constants.REFS),
                       'Accept': constants.ACCEPT,
                       'Accept-Encoding': constants.ENCODING,
                       'Accept-Language': random.choice(constants.LENG),
                       'Pragma': constants.PRAGMA,
                       'Client-ID': constants.CLIENT_ID
                       }

            all_proxies.append({'proxy': p,
                                'time': start_time,
                                'channel': channel_url,
                                'headers': headers,
                                'user_agent': user_agent}
                               )

        self._logger.info("Preparing request to send")
        return all_proxies
