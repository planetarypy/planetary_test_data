#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import planetary_test_data
import shutil
import argparse
try:
    import urllib.request as urllib
except:
    import urllib


class PlanetaryTestDataProducts(object):

    def __init__(self, tags=None, all=None):
        """Object contains core data projects or that match specified tags.

        Attributes
        ----------
        tags : list
            Contains tags of desired data products.  Default: ``['core']``.  If
            ['all'] then all data products will be requested.
        data_path : string
            Filesystem path to ``data.json`` file.
        mission_data : dictionary
            Contains the data products and metadata.
        directory : string
            Filesystem path to directory containing the ``data.json`` file.
        """

        if tags:
            self.tags = tags
        else:
            self.tags = ['core']

        self.data_path = setup_json_file()

        with open(self.data_path, 'r') as r:
            self.mission_data = json.load(r)

        self.directory = os.path.dirname(self.data_path)

    @property
    def products(self):
        """Products that match defined tags"""
        if 'all' in self.tags:
            return_list = self.mission_data.keys()
        else:
            return_list = []
            for product in self.mission_data.keys():
                # If the intersection of the set of tags on the data product
                # with the set of tags on self is non null, then there is a
                # match and we should append the product to the returned list
                if set(self.mission_data[product].get('tags', '')) & set(self.tags):
                    return_list.append(product)

            return return_list


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

    data = PlanetaryTestDataProducts()

    for product in data.products:
        if os.path.exists(os.path.join(data.directory, product)):
            pass
        else:
            urllib.urlretrieve(data.mission_data[product]['url'],
                               os.path.join(data.directory, product))


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', help="Download all products.")
    args = parser.parse_args()
    get_mission_data()
