from oneloader_runner.modules.one_logging import OneLogger
from oneloader_runner.runner.jumia_handler_selenium import *

import json

# log = myLogger(logfile='jumia.log', logger_name='jumia')
# bot = jumiaBot(action='GetCategoryTree')
# bot_result = bot.run()


# with open('jumia_catgory.json', "a+") as f:
#    f.write(bot_result)

with open('jumia_catgory.json', 'r') as f:
    cat_json_raw = json.load(f)

# print(cat_json_raw['SuccessResponse']['Body']['Categories']['Category'])


def get_zip_value(json_data, current_key=None):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = key if current_key is None else f"{current_key}.{key}"
            if key == 'Name' or key == 'CategoryId':
                print(f"{key}: {value}")
            get_zip_value(value, new_key)
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            new_key = f"{current_key}[{i}]"
            get_zip_value(item, new_key)


get_zip_value(
    json_data=cat_json_raw['SuccessResponse']['Body']['Categories']['Category'])
