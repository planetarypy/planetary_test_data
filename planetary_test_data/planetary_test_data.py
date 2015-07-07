# -*- coding: utf-8 -*-
import os
import json
import urllib
import planetary_test_data
import shutil


def setup_json_file():
    default_path = os.path.abspath(planetary_test_data.__file__)
    default_json = os.path.join(os.path.dirname(default_path), 'data.json')
    final_path = os.path.join('tests', 'mission_data', 'data.json')
    if os.path.exists(final_path):
        return os.path.abspath(final_path)
    elif os.path.exists('tests'):
        try:
            os.mkdir(os.path.join('tests', 'mission_data'))
            shutil.copy(default_json, final_path)
            return os.path.normpath(final_path)
        except OSError:
            shutil.copy(default_json, final_path)
            return os.path.normpath(final_path)
    elif os.path.exists('mission_data'):
        final_path = os.path.join('mission_data', 'data.json')
        shutil.copy(default_json, final_path)
        return os.path.normpath(final_path)
    else:
        os.mkdir('mission_data')
        final_path = os.path.join('mission_data', 'data.json')
        shutil.copy(default_json, final_path)
        return os.path.normpath(final_path)


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
