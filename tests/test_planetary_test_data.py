#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_planetary_test_data
----------------------------------

Tests for `planetary_test_data` module.
"""
import planetary_test_data as planet
from planetary_test_data import planetary_test_data
import os
import re
import pytest

data_path_1 = os.path.join('tests', 'mission_data', 'data.json')
data_path_2 = os.path.join('mission_data', 'data.json')

if os.path.basename(os.getcwd()) == 'tests':
    pass
else:
    os.chdir('tests')


def test_default_path():
    default_path = os.path.abspath(planet.__file__)
    test_path = os.path.join('planetary_test_data', 'planetary_test_data',
                             '__init__.py')
    assert re.search(test_path, default_path)


def test_default_json():
    default_path = os.path.abspath(planetary_test_data.__file__)
    default_json = os.path.join(os.path.dirname(default_path), 'data.json')
    test_path = os.path.join('planetary_test_data', 'planetary_test_data',
                             'data.json')
    assert re.search(test_path, default_json)


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_1():
    """Test when tests/mission_data/data.json exists"""
    os.chdir('test_1')
    assert os.path.exists(data_path_1)
    assert planetary_test_data.setup_json_file() == data_path_1
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_2():
    """Test when tests/mission_data exists but data.json Does Not Exist(DNE)"""
    os.chdir('test_2')
    assert os.path.exists(os.path.join('tests', 'mission_data'))
    assert planetary_test_data.setup_json_file() == data_path_1
    os.remove(data_path_1)
    assert not(os.path.exists(data_path_1))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_3():
    """Test when tests/ exists but mission_data/data.json DNE"""
    os.chdir('test_3')
    assert os.path.exists('tests')
    assert planetary_test_data.setup_json_file() == data_path_1
    os.remove(data_path_1)
    assert not(os.path.exists(data_path_1))
    os.rmdir(os.path.join('tests', 'mission_data'))
    assert not(os.path.exists(os.path.join('tests', 'mission_data')))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_4():
    """Test when tests/ DNE but mission_data/data.json exist"""
    os.chdir('test_4')
    assert os.path.exists(data_path_2)
    assert planetary_test_data.setup_json_file() == data_path_2
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_5():
    """Test when tests/ DNE, mission_data exists but data.json DNE"""
    os.chdir('test_5')
    assert os.path.exists('mission_data')
    assert planetary_test_data.setup_json_file() == data_path_2
    os.remove(data_path_2)
    assert not(os.path.exists(data_path_2))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_final_path_6():
    """Test when tests, mission_data, and data.json DNE"""
    os.chdir('test_6')
    assert planetary_test_data.setup_json_file() == data_path_2
    os.remove(data_path_2)
    assert not(os.path.exists(data_path_2))
    os.rmdir(os.path.join('mission_data'))
    assert not(os.path.exists('mission_data'))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_get_mission_data_1():
    """Test if the image downloaded correctly in tests/mission_data"""
    os.chdir('test_1')
    image_path = os.path.join('tests', 'mission_data',
                              '1p190678905erp64kcp2600l8c1.img')
    assert not(os.path.exists(image_path))
    planetary_test_data.get_mission_data()
    assert os.path.exists(image_path)
    os.remove(image_path)
    assert not(os.path.exists(image_path))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'


@pytest.mark.skipif(True, reason="Test disabled.")
def test_get_mission_data_2():
    """Test if the image downloaded correctly in mission_data when tests DNE"""
    os.chdir('test_4')
    image_path = os.path.join('mission_data',
                              '1p190678905erp64kcp2600l8c1.img')
    assert not(os.path.exists(image_path))
    planetary_test_data.get_mission_data()
    assert os.path.exists(image_path)
    os.remove(image_path)
    assert not(os.path.exists(image_path))
    os.chdir('..')
    assert os.path.basename(os.getcwd()) == 'tests'
