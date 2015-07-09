#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import planetary_test_data
import shutil
try:
    import urllib.request as urllib
except:
    import urllib


def setup_json_file():
    """Creates the directories and copies the default data.json to the directory

    Side Effects:
        The function creates the directory 'mission_data' in the 'tests'
        directory if the 'tests' directory exists. If 'tests' directory does
        not exist, then the function will create the 'mission_data' directory
        in the current working directory. Once the directory is set up, the
        function will copy over the default data.json file to the new
        'mission_data' directory. If everything is set up already, then none of
        the directories will be altered.

    Returns:
        The path to the `data.json` file.

    Keyword Arguments:
        None
    """

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


def get_mission_data():
    """Downloads products from data.json

    Side Effects:
        The function uses the returned path from `setup_json_file()`.
        The function will check to see if each product in the data.json file
        exists in the mission_data directory. If the product does not exist,
        the function will download the product to the mission_data directory.

    Keyword Arguments:
        None
    """

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
