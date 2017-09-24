# -*- coding: utf-8 -*-

from planetary_test_data import PlanetaryTestDataProducts
import os


def test_planetary_test_data_object():
    """Tests simple PlanetaryTestDataProducts attributes."""
    data = PlanetaryTestDataProducts()
    assert data.tags == ['core']
    assert data.all_products is None
    # handle running this test individually versus within a suite
    if os.path.exists('tests'):
        assert data.directory == os.path.join('tests', 'mission_data')
    else:
        assert data.directory == os.path.join('mission_data')
    assert os.path.exists(data.data_path)


def test_planetary_test_core_products():
    """Tests the list of core data products."""
    data = PlanetaryTestDataProducts()
    assert data.tags == ['core']
    assert u'2p129641989eth0361p2600r8m1.img' in data.products
    assert u'1p190678905erp64kcp2600l8c1.img' in data.products
    assert u'0047MH0000110010100214C00_DRCL.IMG' in data.products
    assert u'1p134482118erp0902p2600r8m1.img' in data.products
    assert u'h58n3118.img' in data.products
    assert u'r01090al.img' in data.products


def test_planetary_test_all_products():
    """Tests the list of all data products."""
    data = PlanetaryTestDataProducts(all_products=True)
    assert len(data.products) == 151
    assert data.all_products is True
