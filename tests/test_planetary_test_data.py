#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_planetary_test_data
----------------------------------

Tests for `planetary_test_data` module.
"""

import os
import re
import sys
import shutil
import tempfile
from glob import glob


import pytest

from planetary_test_data import planetary_test_data, PlanetaryTestDataProducts

data_path_1 = os.path.join('tests', 'mission_data', 'data.json')
data_path_2 = os.path.join('mission_data', 'data.json')

CWD = os.getcwd()


@pytest.fixture
def tempdir():
    if sys.version_info[0] == 3:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                yield temp_dir
            finally:
                os.chdir(CWD)

    else:
        temp_dir = tempfile.mkdtemp()
        try:
            os.chdir(temp_dir)
            yield temp_dir
        finally:
            os.chdir(CWD)
            shutil.rmtree(temp_dir)


class TestPlanetaryTestDataProducts(object):

    def test_default_args1(self, tempdir):
        test_ptd = PlanetaryTestDataProducts()
        assert not test_ptd.all_products
        assert test_ptd.tags == ['core']
        path, file = os.path.split(test_ptd.data_path)
        assert file == 'data.json'
        assert path.endswith('planetary_test_data')
        assert test_ptd.directory == 'mission_data'
        assert os.path.exists('mission_data')

    def test_default_args2(self, tempdir):
        os.mkdir('tests')
        test_ptd = PlanetaryTestDataProducts()
        path = os.path.join('tests', 'mission_data')
        assert test_ptd.directory == path
        assert os.path.exists(path)

    def test_tags(self, tempdir):
        test_ptd = PlanetaryTestDataProducts(tags=['foo', 'bar'])
        assert test_ptd.tags == ['foo', 'bar']

    def test_all_products(self, tempdir):
        test_ptd = PlanetaryTestDataProducts(all_products=True)
        assert test_ptd.all_products

    def test_directory(self, tempdir):
        test_ptd = PlanetaryTestDataProducts(directory='foo/')
        assert test_ptd.directory == 'foo/'
        assert os.path.exists('foo/')

    def test_mission_data(self, tempdir):
        os.mkdir('foo')
        shutil.copy(
            os.path.join(
                os.path.abspath(CWD),
                'planetary_test_data',
                'data.json'),
            'foo'
        )
        test_ptd = PlanetaryTestDataProducts(
            data_file=os.path.join('foo', 'data.json')
        )
        assert test_ptd.data_path == os.path.join('foo', 'data.json')
        assert isinstance(test_ptd.mission_data, dict)

    def test_products(self, tempdir):
        print(CWD)
        test_data = os.path.join(CWD, 'tests', 'test_data.json')
        test_ptd = PlanetaryTestDataProducts(data_file=test_data)
        core_products = [u'1p190678905erp64kcp2600l8c1.img']
        assert len(test_ptd.products) == len(core_products)
        assert sorted(test_ptd.products) == core_products

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            tags=['TAG_DNE']
        )
        assert not test_ptd.products

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            all_products=True,
        )
        assert sorted(test_ptd.products) == [
            u'0025ML0001270000100807E01_DRCL.IMG',
            u'1p190678905erp64kcp2600l8c1.img',
        ]


class MockArgs(object):

    def __init__(self, _all=False, _dir=None, _file=None):
        self.all = _all
        self.dir = _dir
        self.file = _file


def test_get_mission_data1(tempdir):
    args = MockArgs()
    planetary_test_data.get_mission_data(args)
    assert os.path.exists('tests')
    assert os.path.exists(os.path.join('tests', 'mission_data'))
    core_products = [
        '2p129641989eth0361p2600r8m1.img',
        '1p190678905erp64kcp2600l8c1.img',
        '0047MH0000110010100214C00_DRCL.IMG',
        '1p134482118erp0902p2600r8m1.img',
        'h58n3118.img',
        'r01090al.img',
    ]
    assert glob(os.path.join('tests', 'mission_data', '*')) == core_products
    planetary_test_data.get_mission_data(args)
    assert glob(os.path.join('tests', 'mission_data', '*')) == core_products


def test_get_mission_data2(tempdir):
    os.mkdir('foo')
    shutil.copy(
        os.path.join(
            os.path.abspath(CWD),
            'planetary_test_data',
            'data.json'),
        'foo'
    )
    args = MockArgs(file=os.path.join('foo', 'data.json'))
    planetary_test_data.get_mission_data(args)
    product = '1p190678905erp64kcp2600l8c1.img'
    assert glob(os.path.join('tests', 'mission_data', '*')) == product


def test_get_mission_data3(tempdir):
    os.mkdir('foo')
    shutil.copy(
        os.path.join(
            os.path.abspath(CWD),
            'planetary_test_data',
            'data.json'),
        'foo'
    )
    args = MockArgs(
        file=os.path.join('foo', 'data.json'),
        _all=True,
    )
    planetary_test_data.get_mission_data(args)
    products = [
        '0025ML0001270000100807E01_DRCL.IMG'
        '1p190678905erp64kcp2600l8c1.img'
    ]
    assert glob(os.path.join('tests', 'mission_data', '*')) == products


def test_get_mission_data_4(tempdir):
    os.mkdir('foo')
    os.mkdir('store_dir')
    shutil.copy(
        os.path.join(
            os.path.abspath(CWD),
            'planetary_test_data',
            'data.json'),
        'foo'
    )
    args = MockArgs(
        file=os.path.join('foo', 'data.json'),
        _dir='store_data',
    )
    planetary_test_data.get_mission_data(args)
    product = '1p190678905erp64kcp2600l8c1.img'
    assert glob(os.path.join('store_data', '*')) == product
