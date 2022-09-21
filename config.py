import os
from nextcord import Intents


class Config:
    ids = [246237889376026624, 613089075250987168]
    prefix = '.'
    intents = Intents.all()
    token = os.environ.get('ISV_TOKEN')
    test_token = os.environ.get('ZEUST_TOKEN')
