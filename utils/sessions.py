import os

from dotenv import load_dotenv
from utils.requests_helper import BaseSession

load_dotenv()


def main_url() -> BaseSession:
    base_domain = os.getenv('BASE_DOMAIN')
    return BaseSession(base_url=base_domain)

