****************************************************
MUIPF: Mutual Information Image Processing Framework
****************************************************

|bsd2 badge|

MUIPF is a minimalistic software package to perform image processing based on
mutual information, written in Python. Currently, only the functionality for
sliding two images on top of each other is implemented.

|MUIPF logo|


Installation
============

Please note, that this package has been tested for **Python 3.X**
support. It additionally needs Numerical Python (the numpy module).

System install
--------------

You can install the script package via the standard 'python setup'
mechanism. If you want to install it system-wide into your normal
python installation, you simply issue::

  python setup.py install

with an appropriate level of permission.

Local install
-------------

Alternatively, you can install it locally in your home space, e.g.::

  python setup.py install --user

If the local python install directory is not in your path, you should
add this. For the bash shell you should include in .bashrc::

  export PATH=$PATH:/home/user/.local/bin


Testing MUIPF
=============

In the root directory, running::

  pushd test
  python -m unittest -v -b
  popd

will validate the source of the package by executing regression tests.

For developers
--------------

To perform pylint static checking from the top level directory of the project, use::

  pylint --rcfile utils/srccheck/pylint/pylintrc-3.ini src/*


Documentation
=============

Consult following resources for the (currently very limited) documentation:

* automatically generated Argparse help page of the corresponding script


License
=======

MUIPF is licensed under the BSD 2-clause license. See the included
`LICENSE <LICENSE>`_ file for the detailed licensing conditions.


.. |MUIPF logo| image:: ./utils/art/logo.svg
    :alt: MUIPF logo
    :width: 150 px
    :scale: 100%

.. |bsd2 badge| image:: ./utils/art/bsd2.svg
    :alt: 2-Clause BSD License
    :scale: 100%
    :target: https://opensource.org/licenses/BSD-2-Clause
