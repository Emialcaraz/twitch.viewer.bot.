from dv_twitch_viewer.constants import FILE
import pandas as pd
from settings import settings


def get_proxies():
    proxies = pd.read_csv(FILE, index_col=False, header=None)
    proxies = proxies[0].to_list()
    return proxies[:int(settings.VIEWERS)]


def get_ua():
    return open('dv_twitch_viewer/proxies/ua.txt').read().splitlines()
