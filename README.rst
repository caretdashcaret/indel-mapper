Indel Mapper
============

|License: GPL v3|

Running Indel Mapper
---------------

Example:

.. code:: shell

    $ pip3 install indel-mapper
    $ indel-mapper -a ~/Documents/bowtie2_results.sam -r ~/Documents/references.csv -o ~/Documents/results.csv -m

There are three required arguments and one optional argument for generating the metadata:

-  ``-a`` or ``--alignment`` Alignment SAM file
-  ``-r`` or ``--reference`` Reference CSV file
-  ``-o`` or ``--output`` Output file, in CSV
-  ``-m`` or ``--metadata`` Include a metadata JSON in the output
   generation, for visualization

For Development
===============

Set up
------

First, make sure the correct version of ``virtualenv`` is installed:

.. code:: shell

    $ pip3 install virtualenv

Next, ``cd`` into your project and set up the ``virtualenv`` directory:

.. code:: shell

    $ virtualenv --python=python3 .indel-mapper

Activate ``virtualenv``. This adds the ``indel-mapper/bin`` directory to
the start of your ``$PATH``.

.. code:: shell

    $ source .indel-mapper/bin/activate

Install the required libraries:

.. code:: shell

    $ pip3 install -r requirements.txt

Run the tests:
--------------

.. code:: shell

    $ python3 -m pytest

License
-------

Indel Mapper is licensed under Version 3 of the GNU General Public
License.

.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: http://www.gnu.org/licenses/gpl-3.0
