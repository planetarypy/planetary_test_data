#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_planetary_test_data
----------------------------------

Tests for `planetary_test_data` module.
"""

import os
import sys
import json
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

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            missions=['Mars Science Laboratory'],
        )
        assert test_ptd.products == [u'0025ML0001270000100807E01_DRCL.IMG']

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            missions=['Mars Exploration Rover'],
        )
        assert test_ptd.products == [u'1p190678905erp64kcp2600l8c1.img']

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            instruments=['MastCam'],
        )
        assert test_ptd.products == [u'0025ML0001270000100807E01_DRCL.IMG']

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            instruments=['Pancam'],
        )
        assert test_ptd.products == [u'1p190678905erp64kcp2600l8c1.img']

        test_ptd = PlanetaryTestDataProducts(
            data_file=test_data,
            missions=['Mars Science Laboratory'],
            tags=['core'],
        )
        assert sorted(test_ptd.products) == [
            u'0025ML0001270000100807E01_DRCL.IMG',
            u'1p190678905erp64kcp2600l8c1.img',
        ]


class MockArgs(object):

    def __init__(self, _all=False, _dir=None, _file=None, _instruments=None,
                 _missions=None):
        self.all = _all
        self.dir = _dir
        self.file = _file
        self.instruments = _instruments
        self.missions = _missions


def test_get_mission_data1(tempdir):
    args = MockArgs()
    os.mkdir('tests')
    planetary_test_data.get_mission_data(args)
    assert os.path.exists('tests')
    base = os.path.join('tests', 'mission_data')
    assert os.path.exists(base)
    core_products = sorted([
        os.path.join(base, '2p129641989eth0361p2600r8m1.img'),
        os.path.join(base, '1p190678905erp64kcp2600l8c1.img'),
        os.path.join(base, '0047MH0000110010100214C00_DRCL.IMG'),
        os.path.join(base, '1p134482118erp0902p2600r8m1.img'),
        os.path.join(base, 'h58n3118.img'),
        os.path.join(base, 'r01090al.img'),
        os.path.join(base, '2m132591087cfd1800p2977m2f1.img'),
        os.path.join(base, '0047MH0000110010100214C00_DRCL.LBL'),
    ])
    test_products = sorted(glob(os.path.join('tests', 'mission_data', '*')))
    assert test_products == core_products
    planetary_test_data.get_mission_data(args)
    assert test_products == core_products


def test_get_mission_data2(tempdir):
    os.mkdir('tests')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data)
    planetary_test_data.get_mission_data(args)
    product = os.path.join(
        'tests', 'mission_data', '1p190678905erp64kcp2600l8c1.img'
    )
    assert glob(os.path.join('tests', 'mission_data', '*')) == [product]


def test_get_mission_data3(tempdir):
    os.mkdir('foo')
    os.mkdir('tests')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(
        _file=test_data,
        _all=True,
    )
    base = os.path.join('tests', 'mission_data')
    planetary_test_data.get_mission_data(args)
    products = sorted([
        os.path.join(base, '0025ML0001270000100807E01_DRCL.IMG'),
        os.path.join(base, '1p190678905erp64kcp2600l8c1.img'),
    ])
    assert sorted(glob(os.path.join('tests', 'mission_data', '*'))) == products


def test_get_mission_data4(tempdir):
    os.mkdir('store_dir')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(
        _file=test_data,
        _dir='store_dir',
    )
    planetary_test_data.get_mission_data(args)
    product = os.path.join('store_dir', '1p190678905erp64kcp2600l8c1.img')
    assert glob(os.path.join('store_dir', '*')) == [product]


def test_get_mission_data5(tempdir):
    os.mkdir('tests')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data, _missions=['Mars Science Laboratory'])
    planetary_test_data.get_mission_data(args)
    product = os.path.join(
        'tests', 'mission_data', '0025ML0001270000100807E01_DRCL.IMG'
    )
    assert glob(os.path.join('tests', 'mission_data', '*')) == [product]


def test_get_mission_data6(tempdir):
    os.mkdir('tests')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data, _instruments=['MastCam'])
    planetary_test_data.get_mission_data(args)
    product = os.path.join(
        'tests', 'mission_data', '0025ML0001270000100807E01_DRCL.IMG'
    )
    assert glob(os.path.join('tests', 'mission_data', '*')) == [product]


def test_get_mission_json1(tempdir):
    os.mkdir('tests')
    args = MockArgs()
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('tests', 'data.json'))
    expected_json_keys = sorted([
        '2p129641989eth0361p2600r8m1.img',
        '1p190678905erp64kcp2600l8c1.img',
        '0047MH0000110010100214C00_DRCL.IMG',
        '1p134482118erp0902p2600r8m1.img',
        'h58n3118.img',
        'r01090al.img',
        '2m132591087cfd1800p2977m2f1.img',
    ])
    with open(os.path.join('tests', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json2(tempdir):
    os.mkdir('test')
    args = MockArgs()
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '2p129641989eth0361p2600r8m1.img',
        '1p190678905erp64kcp2600l8c1.img',
        '0047MH0000110010100214C00_DRCL.IMG',
        '1p134482118erp0902p2600r8m1.img',
        'h58n3118.img',
        'r01090al.img',
        '2m132591087cfd1800p2977m2f1.img',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json3(tempdir):
    args = MockArgs()
    with pytest.raises(ValueError):
        planetary_test_data.get_mission_json(args)


def test_get_mission_json4(tempdir):
    os.mkdir('diff_dir')
    args = MockArgs(_dir='diff_dir')
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('diff_dir', 'data.json'))
    expected_json_keys = sorted([
        '2p129641989eth0361p2600r8m1.img',
        '1p190678905erp64kcp2600l8c1.img',
        '0047MH0000110010100214C00_DRCL.IMG',
        '1p134482118erp0902p2600r8m1.img',
        'h58n3118.img',
        'r01090al.img',
        '2m132591087cfd1800p2977m2f1.img',
    ])
    with open(os.path.join('diff_dir', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json5(tempdir):
    os.mkdir('test')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data)
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '1p190678905erp64kcp2600l8c1.img',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json6(tempdir):
    os.mkdir('test')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data, _all=True)
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '0025ML0001270000100807E01_DRCL.IMG',
        '1p190678905erp64kcp2600l8c1.img',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json7(tempdir):
    os.mkdir('test')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data, _missions=['Mars Science Laboratory'])
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '0025ML0001270000100807E01_DRCL.IMG',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


def test_get_mission_json8(tempdir):
    os.mkdir('test')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    args = MockArgs(_file=test_data, _instruments=['MastCam'])
    planetary_test_data.get_mission_json(args)
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '0025ML0001270000100807E01_DRCL.IMG',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys


@pytest.mark.parametrize(
    ('test_args, test_all, test_file, test_dir, test_tags, test_instruments,' +
        'test_missions'),
    [
        ([], False, None, None, None, None, None),
        (['-a'], True, None, None, None, None, None),
        (['-f', 'foo.json'], False, 'foo.json', None, None, None, None),
        (['-d', 'foo'], False, None, 'foo', None, None, None),
        ('-t f -t b'.split(), False, None, None, ['f', 'b'], None, None),
        ('-i a -i b'.split(), False, None, None, None, ['a', 'b'], None),
        ('-i c -i d'.split(), False, None, None, None, None, ['c', 'd']),
    ])
def test_cli(test_args, test_all, test_file, test_dir, test_tags,
             test_instruments, test_missions):
    args = planetary_test_data.cli(test_args)
    assert args.all == test_all
    assert args.file == test_file
    assert args.dir == test_dir
    assert args.tags == test_tags


def test__get_mission_data(tempdir):
    os.mkdir('store_dir')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    # args = planetary_test_data.cli(['-f', test_data, '-d', 'store_dir'])
    sys.argv[1:] = ['-f', test_data, '-d', 'store_dir']
    planetary_test_data._get_mission_data()
    product = os.path.join('store_dir', '1p190678905erp64kcp2600l8c1.img')
    assert glob(os.path.join('store_dir', '*')) == [product]


def test__get_mission_json(tempdir):
    os.mkdir('test')
    test_data = os.path.join(
        os.path.abspath(CWD),
        'tests',
        'test_data.json')
    sys.argv[1:] = ['-f', test_data]
    planetary_test_data._get_mission_json()
    assert os.path.exists(os.path.join('test', 'data.json'))
    expected_json_keys = sorted([
        '1p190678905erp64kcp2600l8c1.img',
    ])
    with open(os.path.join('test', 'data.json'), 'r') as stream:
        copied_json = json.load(stream)

    assert sorted(list(copied_json.keys())) == expected_json_keys
