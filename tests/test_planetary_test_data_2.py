# -*- coding: utf-8 -*-

from planetary_test_data import planetary_test_data
import os

data_path_1 = os.path.join('tests', 'mission_data', 'data.json')


def test_planetary_test_data_object():
    """Tests simple PlanetaryTestDataProducts attributes."""
    data = planetary_test_data.PlanetaryTestDataProducts()
    assert data.tags == ['core']
    assert data.data_path == data_path_1
    assert data.directory == os.path.dirname(data_path_1)


def test_planetary_test_core_products():
    """Tests the list of core data products."""
    data = planetary_test_data.PlanetaryTestDataProducts()
    assert data.tags == ['core']
    assert data.products == [
        u'2p129641989eth0361p2600r8m1.img',
        u'1p190678905erp64kcp2600l8c1.img'
    ]
