from dv_twitch_viewer.constants import FILE
from streamlink import Streamlink
import random
import requests
import sys


def get_proxies():
    proxies_lines = [line.rstrip("\n") for line in open(FILE)]
    return proxies_lines


def get_ua():
    return open('dv_twitch_viewer/proxies/ua.txt').read().splitlines()
