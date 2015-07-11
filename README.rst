===============================
Planetary Test Data
===============================

.. image:: https://img.shields.io/travis/planetarypy/planetary_test_data.svg
        :target: https://travis-ci.org/planetarypy/planetary_test_data

.. image:: https://img.shields.io/pypi/v/planetary_test_data.svg
        :target: https://pypi.python.org/pypi/planetary_test_data


Planetary Test Data contains a list of planetary data for software testing
purposes and utilities to retrieve them.

* Free software: BSD license

Features
--------

* Downloads all sample Planetary test data listed in the ``data.json`` into
  ``./mission_data/`` or if ``./tests/mission_data/`` if ``./tests/`` exists.

TODO
------

* Download to central cache directory and use symbolic links to share data
  between projects or other locations.
* Find smaller example images to reduce download times.
* Command line usage improvements

  * Include a mode that just copies the ``data.json`` file into the local
    directory.
  * Include a mode that allows users to somehow specify subsets of data to
    retrieve.  Perhaps selecting by mission or instrument name.

* Improve label testing.
* Include Mission Names with each product.
* Include product type with each product.

See also the Github issues for this project.

Usage
------

To download the full set of planetary test data install this package with pip
and then run the command ``get_mission_data``::

  pip install planetary_test_data
  get_mission_data

This will take some time since it downloads N GB of planetary data from the
PDS.

Description
------------

Running ``get_mission_data`` will do the following

* If ``tests/mission_data/data.json`` already exists, it just downloads the
  products listed in that directory.
* If ``tests/mission_data`` directory exists, ``data.json`` will be placed in
  that directory and the products listed in ``data.json`` will be downloaded
  and placed in the ``tests/mission_data``.
* If there is no ``tests`` directory, a ``mission_data`` directory will be
  created (if necessary), ``data.json`` placed within that, and the products
  will be downloaded.

Only products which do not exist in the ``mission_data`` directory will be
downloaded.

Mission Data
-------------

The PDS mission data included in the package can be found here::

https://github.com/planetarypy/planetary_test_data/blob/master/planetary_test_data/data.json

If there are products you think should be included or removed from this dataset
please file a Github issue.

data.json Format
-----------------

The ``data.json`` file contains PDS product names, urls and other
metainformation about the product.  This structure will be extended to support
generic testing, for instance the ``label`` key will be changed to a
dictionary that includes product label keys and the values found at those keys.

```
    "1m298459885effa312p2956m2m1.img": {
        "instrument": "MICROSCOPIC IMAGER", 
        "label": "PDS3", 
        "opens": "True", 
        "url": "http://pds-imaging.jpl.nasa.gov/data/mer/opportunity/mer1mo_0xxx/data/sol1918/edr/1m298459885effa312p2956m2m1.img"
    }, 
```
