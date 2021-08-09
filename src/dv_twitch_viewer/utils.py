from dv_twitch_viewer.constants import FILE
import requests, csv
import pandas as pd


def get_proxies():
    proxies = pd.read_csv(FILE, index_col=False, header=None)
    proxies = proxies[0].to_list()
    return proxies


def get_ua():
    return open('dv_twitch_viewer/proxies/ua.txt').read().splitlines()
