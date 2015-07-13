#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import planetary_test_data
import argparse
try:
    import urllib.request as urllib
except:
    import urllib


class PlanetaryTestDataProducts(object):

    def __init__(self, tags=None, all_products=None, directory=None,
                 data_file=None):
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

        Side Effects
        ------------
        Instantiating this object creates the directory 'mission_data' in the
        'tests' directory if the 'tests' directory exists.  If 'tests'
        directory does not exist, then the function will create the
        'mission_data' directory in the current working directory.
        """

        self.all_products = all_products

        if data_file:
            self.data_path = data_file
        else:
            self.data_path = os.path.join(
                os.path.dirname(os.path.abspath(planetary_test_data.__file__)),
                'data.json'
            )

        if tags:
            self.tags = tags
        else:
            self.tags = ['core']

        with open(self.data_path, 'r') as r:
            self.mission_data = json.load(r)

        if directory:
            self.directory = directory
        else:
            if os.path.exists('tests'):
                self.directory = os.path.join('tests', 'mission_data')
            else:
                self.directory = 'mission_data'

        if not os.path.exists(self.directory):
            print("Creating output directory: %s" % self.directory)
            os.makedirs(self.directory)

    @property
    def products(self):
        """List of products that match defined tags"""
        if self.all_products:
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


def get_mission_data(args=None):
    """Downloads products from data.json

    Side Effects:
        The function uses the returned path from `setup_json_file()`.
        The function will check to see if each product in the data.json file
        exists in the mission_data directory. If the product does not exist,
        the function will download the product to the mission_data directory.

    Keyword Arguments:
        None
    """

    data = PlanetaryTestDataProducts(all_products=args.all, directory=args.dir,
                                     data_file=args.file)

    for product in data.products:
        if os.path.exists(os.path.join(data.directory, product)):
            print("Exists: %s" % os.path.join(data.directory, product))
        else:
            print("Retrieving: %s" % data.mission_data[product]['url'])
            urllib.urlretrieve(data.mission_data[product]['url'],
                               os.path.join(data.directory, product))


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', help="Download all products.",
                        action="store_true")
    parser.add_argument('--file', '-f', help="Override default data.json by " +
                        "providing path to custom data.json file.")
    parser.add_argument(
        '--dir', '-d', help="Directory to place test data products in."
    )
    parser.add_argument('--tags', '-t', nargs='*', action='store',
                        help="Retrieve products whose tags match those " +
                        "provided here.")
    args = parser.parse_args()
    get_mission_data(args)
