# -*- coding: utf-8 -*-
import os
import json
import urllib
import planetary_test_data
import shutil

"""
To use setup_json_file()::
    This will create the directory mission_data in the tests director if the
    tests directory exists. If tests directory does not, then this will create
    the mission_data directory in the current working directory. Once the
    directory is set up, the program will copy over the default data.json file
    to the new mission_data directory. If everything is set up already, then
    nothing will happen.
"""


def setup_json_file():
    default_path = os.path.abspath(planetary_test_data.__file__)
    default_json = os.path.join(os.path.dirname(default_path), 'data.json')
    final_path = os.path.join('tests', 'mission_data', 'data.json')
    if os.path.exists(final_path):
        return final_path
    elif os.path.exists('tests'):
        try:
            os.mkdir(os.path.join('tests', 'mission_data'))
            shutil.copy(default_json, final_path)
            return final_path
        except OSError:
            shutil.copy(default_json, final_path)
            return final_path
    elif os.path.exists('mission_data'):
        final_path = os.path.join('mission_data', 'data.json')
        if os.path.exists(final_path):
            return final_path
        else:
            shutil.copy(default_json, final_path)
            return final_path
    else:
        os.mkdir('mission_data')
        final_path = os.path.join('mission_data', 'data.json')
        shutil.copy(default_json, final_path)
        return final_path


"""To use get_mission_data()::
    The function will run through setup_json_file() first. Then, the function
    will check to see if each product in the data.json file exists in the
    mission_data directory. If the product does not exist, the function will
    download the product to the mission_data directory.
"""


def get_mission_data():
    data_path = setup_json_file()
    with open(data_path, 'r') as r:
        mission_data = json.load(r)
    products = mission_data.keys()
    directory = os.path.dirname(data_path)
    for product in products:
        if os.path.exists(os.path.join(directory, product)):
            pass
        else:
            urllib.urlretrieve(mission_data[product]['url'],
                               os.path.join(directory, product))
