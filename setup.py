#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

setup(
    name='planetary_test_data',
    version='0.4.0',
    description=(
        "Planetary Test Data contains a list of planetary data for software "
        "testing purposes and utilities to retrieve them."
    ),
    long_description=readme + '\n\n' + history,
    author="PlanetaryPy Developers",
    author_email='contact@planetarypy.com',
    url='https://github.com/planetarypy/planetary_test_data',
    packages=[
        'planetary_test_data',
    ],
    package_dir={'planetary_test_data':
                 'planetary_test_data'},
    package_data={'planetary_test_data': ['planetary_test_data/data.json']},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='planetary_test_data',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'get_mission_data=planetary_test_data.planetary_test_data:cli'
        ],
    }
)
