=========================
RSA Archer Client Library
=========================


.. image:: https://img.shields.io/pypi/v/pyarcher.svg
        :target: https://pypi.python.org/pypi/pyarcher

.. image:: https://img.shields.io/travis/kylecribbs/pyarcher.svg
        :target: https://travis-ci.org/kylecribbs/pyarcher

.. image:: https://readthedocs.org/projects/pyarcher/badge/?version=latest
        :target: https://pyarcher.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/kylecribbs/pyarcher/shield.svg
     :target: https://pyup.io/repos/github/kylecribbs/pyarcher/
     :alt: Updates



Python client library for interfacing with RSA Archer.


* Free software: MIT license
* Documentation: https://pyarcher.readthedocs.io.


Features
--------

* TODO

Install
--------
ArcherDB requires pyodbc for connecting to mssql so you may need to install additional packages.
Ubuntu: Required packages are unixodbc-dev g++ freetds-dev freetds-bin tdsodbc
Centos: Required packages are gcc-c++ python-devel unixODBC-devel freetds
Note: In the future we will have pyarcher.ArcherDB separated from pyarcher.Archer.

You may also need to configure your ODBC ini. For example in /etc/odbcinst.ini you may need the following configure
```ini
[FreeTDS]
Description=FreeTDS Driver
Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
tds_version=8.0
```

FreeTDS python example
```python
from pyarcher import ArcherDB
archer = ArcherDB("user", "password", "host", "database", query={"driver": "FreeTDS", "TDS_VERSION": "8.0"})
table = archer.get_table("tblAsyncJobQueue")
select = table.select()
data = archer.engine.execute(select)
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
