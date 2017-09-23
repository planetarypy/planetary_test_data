#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import planetary_test_data
import argparse
try:
    import urllib.request as urllib
except ImportError:
    import urllib


class PlanetaryTestDataProducts(object):

    def __init__(self, tags=None, all_products=None, directory=None,
                 data_file=None, missions=[], instruments=[]):
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
        self.missions = missions or []
        self.instruments = instruments or []

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
            if not self.missions and not self.instruments:
                self.tags = ['core']
            else:
                self.tags = []

        with open(self.data_path, 'r') as stream:
            self.mission_data = json.load(stream)

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
            return_list = list(self.mission_data.keys())
        else:
            tags = set(self.tags)
            return_list = []
            for product, data in self.mission_data.items():
                # If the intersection of the set of tags on the data product
                # with the set of tags on self is non null, then there is a
                # match and we should append the product to the returned list
                product_tags = set(data.get('tags', ''))
                tags_match = bool(product_tags & tags)
                if self.missions == []:
                    mission_match = False
                else:
                    product_mission = str(data.get('mission'))
                    mission_match = product_mission in self.missions
                if self.instruments == []:
                    instrument_match = False
                else:
                    product_instrument = str(data.get('instrument'))
                    instrument_match = product_instrument in self.instruments
                if tags_match or mission_match or instrument_match:
                    return_list.append(product)

        return return_list


def get_mission_data(args):
    """Downloads products from data.json

    Side Effects:
        The function uses the returned path from `setup_json_file()`.
        The function will check to see if each product in the data.json file
        exists in the mission_data directory. If the product does not exist,
        the function will download the product to the mission_data directory.

    Keyword Arguments:
        None
    """

    data = PlanetaryTestDataProducts(
        all_products=args.all,
        directory=args.dir,
        data_file=args.file,
        instruments=args.instruments,
        missions=args.missions,
    )

    for product in data.products:
        image = data.mission_data[product]
        if os.path.exists(os.path.join(data.directory, product)):
            print("Exists: %s" % os.path.join(data.directory, product))
        else:
            image_url = image['url']
            print("Retrieving: %s" % image_url)
            urllib.urlretrieve(image_url,
                               os.path.join(data.directory, product))
            if 'url_lbl' in image:
                lbl_url = image['url_lbl']
                print("Retrieving: %s" % lbl_url)
                lbl_name = image['url_lbl'].split('/')[-1]
                urllib.urlretrieve(
                    lbl_url,
                    os.path.join(data.directory, lbl_name),
                )


def get_mission_json(args):
    """Download the a subset of or the entire data.json

    The data.json will download to the tests or test directory by default. If
    a tests or test directory does not exist and a directory is not given, an
    exception will be raised
    """
    if args.dir is None:
        if os.path.isdir('tests'):
            json_dir = 'tests'
        elif os.path.isdir('test'):
            json_dir = 'test'
        else:
            raise ValueError((
                "Either 'tests' or 'test' must be an existing directory or " +
                "a directory must be specified with the '-d' flag")
            )
    else:
        json_dir = args.dir

    data = PlanetaryTestDataProducts(
        all_products=args.all,
        directory=json_dir,
        data_file=args.file,
        instruments=args.instruments,
        missions=args.missions,
    )
    with open(data.data_path, 'r') as data_json:
        original_json = json.load(data_json)
    new_json = dict(
        (product, original_json[product]) for product in data.products
    )

    new_json_path = os.path.join(json_dir, 'data.json')
    with open(new_json_path, 'w') as data_json:
        json.dump(
            new_json,
            data_json,
            indent=4,
            separators=(',', ': '),
            sort_keys=True,
        )


def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', help="Download all products.",
                        action="store_true")
    parser.add_argument('--file', '-f', help="Override default data.json by " +
                        "providing path to custom data.json file.")
    parser.add_argument(
        '--dir', '-d', help="Directory to place test data products in."
    )
    parser.add_argument('--tags', '-t', nargs='?', action='append',
                        help="Retrieve products whose tags match those " +
                        "provided here.")
    parser.add_argument('--instruments', '-i', nargs='?', action='append',
                        help='Get products by instrument')
    parser.add_argument('--missions', '-m', nargs='?', action='append',
                        help='Get products by mission')
    parsed_args = parser.parse_args(args)
    return parsed_args


def _get_mission_data():
    args = cli(sys.argv[1:])
    get_mission_data(args)


def _get_mission_json():
    args = cli(sys.argv[1:])
    get_mission_json(args)
